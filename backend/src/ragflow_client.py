import aiohttp
import json
import asyncio
import base64

from constants import RAGFLOW_API_KEY, RAGFLOW_URL


class RAGFlowAPIClient:
    def __init__(self):
        self.session = None
        self.api_key = RAGFLOW_API_KEY
        self.base_url = RAGFLOW_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    async def create_chat_assistant(
        self,
        name,
        dataset_ids=None,
        llm_settings=None,
        prompt_settings=None,
    ):
        url = f"{self.base_url}/api/v1/chats"

        payload = {
            "name": name,
            "avatar": "",
            "dataset_ids": dataset_ids if dataset_ids else [],
            "llm": (
                llm_settings
                if llm_settings
                else {
                    "model_name": "llama3.2",
                    "temperature": 0.1,
                    "top_p": 0.3,
                    "presence_penalty": 0.2,
                    "frequency_penalty": 0.7,
                    "max_token": 512,
                }
            ),
            "prompt": (
                prompt_settings
                if prompt_settings
                else {
                    "similarity_threshold": 0.2,
                    "keywords_similarity_weight": 0.7,
                    "top_n": 8,
                    "variables": [{"key": "knowledge", "optional": True}],
                    # "rerank_model": "vector",
                    "empty_response": "",
                    "opener": "Hi! I am your assistant, can I help you?",
                    "show_quote": True,
                    "prompt": "Please provide helpful responses.",
                }
            ),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return {
                        "error": f"Failed to create chat assistant: {response.status}"
                    }

    async def create_session(
        self, chat_id, name="New Session", ttl=None, metadata=None
    ):
        url = f"{self.base_url}/api/v1/chats/{chat_id}/sessions"
        payload = {"name": name}
        if ttl:
            payload["ttl"] = ttl
        if metadata:
            payload["metadata"] = metadata

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return {"error": f"Failed to create session: {response.status}"}

    async def ask_question(self, chat_id, session_id, question, stream=False):
        url = f"{self.base_url}/api/v1/chats/{chat_id}/completions"
        payload = {"question": question, "stream": stream, "session_id": session_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return {"error": f"Failed to ask question: {response.status}"}

    def upload_document(self, file_path, description=None, metadata=None):
        with open(file_path, "rb") as file:
            document = self.client.upload_document(
                file, description=description, metadata=metadata
            )
        return document

    def create_dataset(self, name, description=None, metadata=None):
        try:
            dataset = self.client.create_dataset(
                name=name, description=description, metadata=metadata
            )
            print("Dataset created successfully.")
            return dataset
        except Exception as e:
            print(f"Error creating dataset: {e}")

    def upload_dataset(self, file_path, description=None, metadata=None):
        with open(file_path, "rb") as file:
            dataset = self.client.upload_dataset(
                file, description=description, metadata=metadata
            )
        return dataset


if __name__ == "__main__":
    test = RAGFlowAPIClient()
    func = asyncio.run(
        test.create_chat_assistant(
            name="test", dataset_ids=["d3f778a59e2d11efa828f5d311f1eeef"]
        )
    )
    print(func)
