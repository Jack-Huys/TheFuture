from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from app.services.ai_service import create_chat_stream

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    history: list = []


class ResetRequest(BaseModel):
    pass


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    对话接口 - 流式返回AI回复
    """
    def generate():
        try:
            for text in create_chat_stream(
                message=request.message,
                history=request.history
            ):
                # 使用标准JSON编码
                data = {"content": text}
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/reset")
async def reset(request: ResetRequest):
    """
    重置对话
    """
    return {"success": True, "message": "对话已重置"}


@router.get("/health")
async def health():
    """
    健康检查
    """
    return {"status": "ok"}
