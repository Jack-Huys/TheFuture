import os
import re
import httpx
from app.core.config import MINIMAX_API_KEY, MINIMAX_BASE_URL, MODEL_NAME, SKILL_FILE_PATH, AI_SDK_TYPE

# 根据配置选择SDK
if AI_SDK_TYPE == "anthropic":
    import anthropic
else:
    from openai import OpenAI


def load_skill():
    """加载zhangxuefeng-skill内容"""
    with open(SKILL_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def get_ai_client():
    """获取AI客户端"""
    if AI_SDK_TYPE == "anthropic":
        return anthropic.Anthropic(
            api_key=MINIMAX_API_KEY,
            base_url=MINIMAX_BASE_URL
        )
    else:
        return OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url=MINIMAX_BASE_URL
        )


def web_search(query: str) -> str:
    """执行网页搜索"""
    try:
        encoded_query = query.replace(' ', '%20')
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = httpx.get(url, headers=headers, timeout=30)

        for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                response.encoding = encoding
                html = response.text
                break
            except:
                continue

        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        text = ''.join(c for c in text if ord(c) < 0x10000 or c in '\n\r')

        return text[:3000]
    except Exception as e:
        return f"搜索失败: {str(e)}"


def needs_research(message: str) -> bool:
    """判断是否需要搜索数据"""
    keywords = ['学校', '分数', '录取', '就业', '薪资', '专业', '排名', '考研', '高考']
    return any(kw in message for kw in keywords)


def research_and_append_context(message: str) -> str:
    """如果需要搜索，追加搜索结果到消息"""
    if not needs_research(message):
        return ""

    search_queries = [
        message,
        f"{message} 2026 高考",
    ]

    context = "\n\n【最新搜索结果】\n"
    for sq in search_queries:
        result = web_search(sq)
        context += f"【{sq}】\n{result}\n"

    return context


def clean_tool_calls(text: str) -> str:
    """过滤掉工具调用语法"""
    # 匹配 [TOOL_CALL] ... [/TOOL_CALL] 格式
    text = re.sub(r'\[TOOL_CALL\].*?\[/TOOL_CALL\]', '', text, flags=re.DOTALL)
    # 匹配 ```tool_call ... ``` 格式
    text = re.sub(r'```tool_call.*?```', '', text, flags=re.DOTALL)
    # 匹配各种工具调用标记
    text = re.sub(r'\{[\s\n]*"tool"\s*:\s*"[^"]+"[\s\n]*"args"\s*:\s*\{[^}]+\}[\s\n]*\}', '', text)
    # 清理残留的空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def create_chat_stream(message: str, history: list = None):
    """创建对话流"""
    client = get_ai_client()
    skill_content = load_skill()

    # 如果需要研究，追加搜索结果
    research_context = research_and_append_context(message)
    if research_context:
        message += research_context

    # 构造消息列表
    messages = []

    if history:
        for role, content in history:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    if AI_SDK_TYPE == "anthropic":
        with client.messages.stream(
            model=MODEL_NAME,
            system=skill_content,
            messages=messages,
            max_tokens=2048
        ) as stream:
            for text in stream.text_stream:
                cleaned = clean_tool_calls(text)
                if cleaned:
                    yield cleaned
    else:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": skill_content},
                *messages
            ],
            stream=True
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                cleaned = clean_tool_calls(text)
                if cleaned:
                    yield cleaned


if __name__ == "__main__":
    print("直接运行此模块无效，请通过API调用")
