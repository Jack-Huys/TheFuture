# "未来" 技术架构文档

> 版本：V1.0
> 日期：2026-04-22

---

## 1. 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                           │
│                   (Vue 3 单页应用)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      云服务器                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Nginx (反向代理)                    │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        │                                     │
│  ┌─────────────────────┴───────────────────────────────┐   │
│  │                  FastAPI (Python)                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │ /api/chat   │  │ /api/reset  │  │ /api/health │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        │                                     │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              MiniMax API (OpenAI兼容)                 │   │
│  │   + zhangxuefeng-skill (System Prompt)              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 技术选型明细

### 2.1 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.x | 核心框架 |
| Vite | 5.x | 构建工具 |
| Vue Router | 4.x | 路由管理 |
| Axios | 1.x | HTTP客户端 |
| CSS | 原生CSS/变量 | 样式 |

**为什么选Vue 3 + Vite：**
- 开发体验好，热更新快
- 生态成熟，文档完善
- 适合快速开发MVP

### 2.2 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 运行环境 |
| FastAPI | 0.110+ | Web框架 |
| Uvicorn | 0.29+ | ASGI服务器 |
| SSE | 原生支持 | 流式响应 |
| openai | 1.x | MiniMax API客户端 |

**为什么选FastAPI：**
- 异步支持好，适合流式输出
- 自动生成API文档
- 类型安全，开发效率高

### 2.3 部署技术栈

| 技术 | 用途 |
|------|------|
| Docker | 容器化 |
| Nginx | 反向代理/静态文件 |
| Docker Compose | 多容器编排 |

---

## 3. 目录结构

```
TheFuture/
├── docs/                      # 文档
│   ├── PRD.md                 # 产品需求文档
│   └── ARCHITECTURE.md        # 本文档
│
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI入口
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── chat.py       # 对话API
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py     # 配置
│   │   └── services/
│   │       ├── __init__.py
│   │       └── ai_service.py # AI服务
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── Home.vue      # 首页
│   │   │   └── Consult.vue   # 咨询页
│   │   ├── components/
│   │   │   ├── ChatBubble.vue    # 对话气泡
│   │   │   └── InputBox.vue      # 输入框
│   │   └── assets/
│   │       └── styles.css
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
│
└── zhangxuefeng-skill/         # AI Skill（已有）
    └── SKILL.md
```

---

## 4. API设计

### 4.1 POST /api/chat

**功能**：发送消息，获取AI流式回复

**请求**：
```json
{
  "message": "我孩子560分河南，想学金融",
  "history": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好，你想问什么？"}
  ]
}
```

**响应**（SSE流式）：
```
Content-Type: text/event-stream

data: {"content": "停"}

data: {"content": "停停"}

data: {"content": "金融这个行业，"}
...
data: {"content": "你别碰。", "done": true}
```

### 4.2 POST /api/reset

**功能**：重置对话

**请求**：空对象 `{}`

**响应**：
```json
{
  "success": true,
  "message": "对话已重置"
}
```

### 4.3 GET /api/health

**功能**：健康检查

**响应**：
```json
{
  "status": "ok",
  "timestamp": "2026-04-22T12:00:00Z"
}
```

---

## 5. AI服务设计

### 5.1 MiniMax API调用

```python
from openai import OpenAI

client = OpenAI(
    api_key=config.MINIMAX_API_KEY,
    base_url="https://api.minimax.chat/v"  # MiniMax endpoint
)

def chat_with_zhangxuefeng(messages, history):
    # 加载skill作为system prompt
    system_prompt = load_skill("zhangxuefeng-skill/SKILL.md")

    # 构造完整消息列表
    full_messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": message}
    ]

    # 流式调用
    stream = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=full_messages,
        stream=True
    )

    return stream
```

### 5.2 System Prompt注入

zhangxuefeng-skill的完整内容作为`system`角色注入，确保AI以张雪峰身份回答。

---

## 6. 前端设计

### 6.1 Vue组件结构

```
App.vue
  ├── Home.vue (首页)
  └── Consult.vue (咨询页)
        ├── Header
        ├── ChatArea
        │     └── ChatBubble[] (对话气泡列表)
        └── InputBox (输入框 + 发送按钮)
```

### 6.2 状态管理

使用Vue 3 Composition API + `ref`/`reactive`，无需额外状态管理库。

**Consult.vue 核心状态**：
```javascript
const messages = ref([])           // 对话历史
const inputText = ref('')          // 输入框文字
const isLoading = ref(false)        // 加载状态
```

### 6.3 流式响应处理

```javascript
async function sendMessage() {
  isLoading.value = true

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      message: inputText.value,
      history: messages.value
    })
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const {done, value} = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    const data = JSON.parse(chunk)
    messages.value.push({role: 'assistant', content: data.content})
  }

  isLoading.value = false
}
```

---

## 7. 安全考虑

### 7.1 API限流

- 每个IP每分钟最多30次请求
- 使用Nginx或FastAPI中间件实现

### 7.2 输入校验

- 消息长度限制：最多2000字符
- 敏感词过滤

### 7.3 跨域配置

- 生产环境Nginx配置CORS
- 开发环境Vite代理

---

## 8. 性能优化

### 8.1 后端
- 使用异步IO（FastAPI + uvicorn）
- MiniMax API调用本身支持流式，减少等待时间

### 8.2 前端
- Vue 3 + Vite构建优化
- 组件懒加载
- CSS变量实现主题切换

### 8.3 部署
- Docker多阶段构建，减小镜像体积
- Nginx静态资源缓存

---

## 9. 环境变量

### 9.1 后端 (.env)

```
MINIMAX_API_KEY=your-api-key
MINIMAX_BASE_URL=https://api.minimax.chat/v
MODEL_NAME=your-model-name
PORT=8000
```

### 9.2 前端 (.env)

```
VITE_API_BASE_URL=http://localhost:8000
```

---

## 10. 部署流程

### 10.1 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 前端
cd frontend
npm install
npm run dev
```

### 10.2 Docker部署

```bash
# 构建并启动
docker-compose up --build

# 查看日志
docker-compose logs -f
```

### 10.3 云服务器部署

1. 安装Docker和Docker Compose
2. 克隆代码
3. 配置环境变量
4. 执行`docker-compose up -d`
5. 配置Nginx反向代理
6. 配置域名和SSL证书
