# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import logging
from collections.abc import AsyncGenerator

from llama_stack.apis.inference import (
    CompletionResponse,
    InferenceProvider,
    InterleavedContent,
    LogProbConfig,
    Message,
    ResponseFormat,
    SamplingParams,
    ToolChoice,
    ToolConfig,
    ToolDefinition,
    ToolPromptFormat,
)
from llama_stack.apis.models import ModelType
from llama_stack.providers.datatypes import Model, ModelsProtocolPrivate
from llama_stack.providers.utils.inference.embedding_mixin import (
    SentenceTransformerEmbeddingMixin,
)
from llama_stack.providers.utils.inference.openai_compat import (
    OpenAIChatCompletionToLlamaStackMixin,
    OpenAICompletionToLlamaStackMixin,
)

from .config import SentenceTransformersInferenceConfig

log = logging.getLogger(__name__)


class SentenceTransformersInferenceImpl(
    OpenAIChatCompletionToLlamaStackMixin,
    OpenAICompletionToLlamaStackMixin,
    SentenceTransformerEmbeddingMixin,
    InferenceProvider,
    ModelsProtocolPrivate,
):
    __provider_id__: str

    def __init__(self, config: SentenceTransformersInferenceConfig) -> None:
        self.config = config

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def should_refresh_models(self) -> bool:
        return False

    async def list_models(self) -> list[Model] | None:
        return [
            Model(
                identifier="all-MiniLM-L6-v2",
                provider_resource_id="all-MiniLM-L6-v2",
                provider_id=self.__provider_id__,
                metadata={
                    "embedding_dimension": 384,
                },
                model_type=ModelType.embedding,
            ),
        ]

    async def register_model(self, model: Model) -> Model:
        return model

    async def unregister_model(self, model_id: str) -> None:
        pass

    async def completion(
        self,
        model_id: str,
        content: str,
        sampling_params: SamplingParams | None = None,
        response_format: ResponseFormat | None = None,
        stream: bool | None = False,
        logprobs: LogProbConfig | None = None,
    ) -> CompletionResponse | AsyncGenerator:
        raise ValueError("Sentence transformers don't support completion")

    async def chat_completion(
        self,
        model_id: str,
        messages: list[Message],
        sampling_params: SamplingParams | None = None,
        response_format: ResponseFormat | None = None,
        tools: list[ToolDefinition] | None = None,
        tool_choice: ToolChoice | None = ToolChoice.auto,
        tool_prompt_format: ToolPromptFormat | None = None,
        stream: bool | None = False,
        logprobs: LogProbConfig | None = None,
        tool_config: ToolConfig | None = None,
    ) -> AsyncGenerator:
        raise ValueError("Sentence transformers don't support chat completion")

    async def batch_completion(
        self,
        model_id: str,
        content_batch: list[InterleavedContent],
        sampling_params: SamplingParams | None = None,
        response_format: ResponseFormat | None = None,
        logprobs: LogProbConfig | None = None,
    ):
        raise NotImplementedError("Batch completion is not supported for Sentence Transformers")

    async def batch_chat_completion(
        self,
        model_id: str,
        messages_batch: list[list[Message]],
        sampling_params: SamplingParams | None = None,
        tools: list[ToolDefinition] | None = None,
        tool_config: ToolConfig | None = None,
        response_format: ResponseFormat | None = None,
        logprobs: LogProbConfig | None = None,
    ):
        raise NotImplementedError("Batch chat completion is not supported for Sentence Transformers")
