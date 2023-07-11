import asyncio
from typing import AsyncIterable, Awaitable

import uvicorn
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage

from learning_langchain.multi_key_chat_open_ai import MultiKeyChatOpenAI

load_dotenv(find_dotenv())


async def wait_done(fn: Awaitable, event: asyncio.Event):
    try:
        await fn
    except Exception as e:
        print(e)
        event.set()
    finally:
        event.set()


async def call_openai(question: str) -> AsyncIterable[str]:
    handler = AsyncIteratorCallbackHandler()
    llm = MultiKeyChatOpenAI(streaming=True, callbacks=[handler], temperature=0)

    coroutine = wait_done(llm.agenerate(messages=[[HumanMessage(content=question)]]), handler.done)
    task = asyncio.create_task(coroutine)

    async for token in handler.aiter():
        yield f"{token}"

    await task


app = FastAPI()


@app.post("/ask")
def ask(body: dict):
    return StreamingResponse(call_openai(body['question']), media_type="text/event-stream")


@app.get("/")
async def homepage():
    return FileResponse('statics/index.html')


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8888, app=app)
