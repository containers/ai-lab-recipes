import asyncio
import sqlite3
from collections.abc import AsyncIterator
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Any, Callable, Literal
import os

import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

# Example from https://ai.pydantic.dev/examples/chat-app/

model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"

# Initialize the OpenAI-compatible model for your Llama.cpp server
model = OpenAIModel(
    'llama',
    base_url=model_service,  # Llama.cpp server endpoint
    api_key='dummy',  # No API key needed unless configured
)

# Initialize Pydantic AI Agent with the custom model
agent = Agent(model)

THIS_DIR = Path(__file__).parent

@dataclass
class Database:
    """Rudimentary database to store chat messages in SQLite."""
    con: sqlite3.Connection
    _loop: asyncio.AbstractEventLoop
    _executor: ThreadPoolExecutor

    @classmethod
    @asynccontextmanager
    async def connect(
        cls, file: Path = THIS_DIR / '.chat_app_messages.sqlite'
    ) -> AsyncIterator['Database']:  # use forward reference here
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        con = await loop.run_in_executor(executor, cls._connect, file)
        slf = cls(con, loop, executor)
        try:
            yield slf
        finally:
            await slf._asyncify(con.close)

    @staticmethod
    def _connect(file: Path) -> sqlite3.Connection:
        con = sqlite3.connect(str(file))
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, message_list TEXT);'
        )
        con.commit()
        return con

    async def add_messages(self, messages: bytes):
        await self._asyncify(
            self._execute,
            'INSERT INTO messages (message_list) VALUES (?);',
            messages,
            commit=True,
        )
        await self._asyncify(self.con.commit)

    async def get_messages(self) -> list[ModelMessage]:
        c = await self._asyncify(
            self._execute, 'SELECT message_list FROM messages order by id'
        )
        rows = await self._asyncify(c.fetchall)
        messages: list[ModelMessage] = []
        for row in rows:
            messages.extend(ModelMessagesTypeAdapter.validate_json(row[0]))
        return messages

    async def delete_all_messages(self):
        """Delete all chat messages from the database."""
        await self._asyncify(self._execute, 'DELETE FROM messages;', commit=True)

    def _execute(
        self, sql: str, *args: Any, commit: bool = False
    ) -> sqlite3.Cursor:
        cur = self.con.cursor()
        cur.execute(sql, args)
        if commit:
            self.con.commit()
        return cur

    async def _asyncify(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        return await self._loop.run_in_executor(  # type: ignore
            self._executor,
            partial(func, **kwargs),
            *args,  # type: ignore
        )

def to_chat_message(m: ModelMessage) -> dict:
    first_part = m.parts[0]
    if isinstance(m, ModelRequest):
        if isinstance(first_part, UserPromptPart):
            return {
                'role': 'user',
                'timestamp': first_part.timestamp.isoformat(),
                'content': first_part.content,
            }
    elif isinstance(m, ModelResponse):
        if isinstance(first_part, TextPart):
            return {
                'role': 'model',
                'timestamp': m.timestamp.isoformat(),
                'content': first_part.content,
            }
    raise ValueError(f'Unexpected message type for chat app: {m}')

async def main():
    st.title("Chatbot Pydantic-AI")

    async with Database.connect() as db:
        # Add a button to delete chat history
        if st.button("Delete Chat History"):
            await db.delete_all_messages()  # Delete the messages
            st.success("Chat history deleted.")

        # Load chat history
        messages = await db.get_messages()

        # Display chat history
        for message in messages:
            chat_message = to_chat_message(message)
            with st.chat_message(chat_message['role']):
                st.markdown(chat_message['content'])

        # User input
        prompt = st.chat_input("You: ")

        if prompt:
            # Add user message to the chat history
            user_message = ModelRequest(
                parts=[UserPromptPart(content=prompt, timestamp=datetime.now(tz=timezone.utc))]
            )
            await db.add_messages(ModelMessagesTypeAdapter.dump_json([user_message]))

            # Display user message in the chat
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get the chat history so far to pass as context to the agent
            messages = await db.get_messages()

            # Create a placeholder for the model's response
            response_placeholder = st.empty()

            # Run the agent with the user prompt and the chat history
            async with agent.run_stream(prompt, message_history=messages) as result:
                response_text = ""
                async for text in result.stream(debounce_by=0.01):
                    response_text = text
                    # Update the placeholder with the new content as it's streamed
                    response_placeholder.markdown(f"model: {response_text}")

                # Add model response to the chat history
                model_response = ModelResponse(
                    parts=[TextPart(content=response_text)], timestamp=result.timestamp()
                )
                await db.add_messages(ModelMessagesTypeAdapter.dump_json([model_response]))

if __name__ == '__main__':
    asyncio.run(main())