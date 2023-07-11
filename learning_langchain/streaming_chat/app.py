import asyncio
import sys

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage

from learning_langchain.multi_key_chat_open_ai import MultiKeyChatOpenAI

handler = AsyncIteratorCallbackHandler()
llm = MultiKeyChatOpenAI(streaming=True, callbacks=[handler], temperature=0, verbose=True)


async def consumer():
    iterator = handler.aiter()
    async for item in iterator:
        sys.stdout.write(item)
        sys.stdout.flush()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    message = '什么是AI？'
    agenerate = llm.agenerate(messages=[[HumanMessage(content=message)]])
    loop.create_task(agenerate)
    loop.create_task(consumer())
    loop.run_forever()
    loop.close()
