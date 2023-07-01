from typing import Any, List, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, ChatResult


# 实现多个OpenAI API Key 轮询使用，避免触碰 limit
def round_robin(keys):
    while True:
        for key in keys:
            yield key


class MultiChatOpenAI(ChatOpenAI):
    keys: List[str] = []

    def __init__(self, **kwargs):
        keys = kwargs.pop('keys', [])
        super().__init__(**kwargs)
        self.__dict__['keys'] = keys
        self.__dict__['robin'] = round_robin(self.keys)

    def _generate_with_cache(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        self.openai_api_key = next(self.__dict__['robin'])
        return super()._generate_with_cache(messages, stop, run_manager, **kwargs)

    async def _agenerate_with_cache(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        self.openai_api_key = next(self.__dict__['robin'])
        return await super()._agenerate_with_cache(messages, stop, run_manager, **kwargs)
