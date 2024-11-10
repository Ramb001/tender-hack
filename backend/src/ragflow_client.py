import os
import json
import asyncio
import urllib.parse
import time

import aiohttp
from aiohttp import FormData

from constants import RAGFLOW_API_KEY, RAGFLOW_URL


class RAGFlowAPIClient:
    def __init__(self, auction_id):
        self.session_id = None
        self.api_key = RAGFLOW_API_KEY
        self.base_url = RAGFLOW_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.auction_id = auction_id
        self.dataset_ids = []
        self.document_ids = []
        self.chat_id = None

    async def create_dataset(self):
        # check_url = f"{self.base_url}/api/v1/datasets?name={self.auction_id}"

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(check_url, headers=self.headers) as response:
        #         if response.status == 200:
        #             data = await response.json()
        #             if len(data["data"]) != 0:
        #                 self.dataset_ids = [item["id"] for item in data["data"]]
        #                 return
        #         else:
        #             return {
        #                 "error": f"Failed to create chat assistant: {response.status}"
        #             }

        url = f"{self.base_url}/api/v1/datasets"
        payload = {
            "name": self.auction_id,
            "avatar": "",
            "description": "",
            "language": "English",
            "embedding_model": "mxbai-embed-large:latest",
            "permission": "me",
            "chunk_method": "naive",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.dataset_ids.append(data["data"]["id"])
                else:
                    return {
                        "error": f"Failed to create chat assistant: {response.status}"
                    }

    async def upload_documents(self):
        url = f"{self.base_url}/api/v1/datasets/{self.dataset_ids[0]}/documents"
        folder_path = os.path.join(
            os.path.dirname(__file__), "..", "data", self.auction_id
        )

        if not os.path.isdir(folder_path):
            print(f"Папка {folder_path} не найдена.")
            return

        async with aiohttp.ClientSession() as session:
            form = FormData()

            # check_url = (
            #     f"{self.base_url}/api/v1/datasets/{self.dataset_ids[0]}/documents"
            # )

            # async with aiohttp.ClientSession() as session:
            #     async with session.get(check_url, headers=self.headers) as response:
            #         if response.status == 200:
            #             data = await response.json()
            #             if len(data["data"]["docs"]) != 0:
            #                 documents_available = []
            #                 for filename in os.listdir(folder_path):
            #                     documents_available.append(
            #                         True
            #                         if urllib.parse.quote(filename)
            #                         in data["data"]["docs"]
            #                         else False
            #                     )
            #                 if False not in documents_available:
            #                     return
            #         else:
            #             return {
            #                 "error": f"Failed to create chat assistant: {response.status}"
            #             }

            # if len(documents_available) == os.listdir(folder_path):
            #     return

            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                if os.path.isfile(file_path) and not filename.endswith(".json"):
                    form.add_field(
                        "file",
                        open(file_path, "rb"),
                        filename=filename,
                        content_type="application/octet-stream",
                    )

            async with session.post(
                url, headers={"Authorization": f"Bearer {self.api_key}"}, data=form
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.document_ids = [item["id"] for item in data["data"]]
                    print("All files uploaded successfully.")
                else:
                    print(
                        f"Error uploading files: {response.status} - {await response.text()}"
                    )

    async def parse_documents(self):
        url = f"{self.base_url}/api/v1/datasets/{self.dataset_ids[0]}/chunks"
        payload = {"document_ids": self.document_ids}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print("Parsing started!")
                else:
                    return {
                        "error": f"Failed to create chat assistant: {response.status}"
                    }

    async def check_parse(self):
        status = False
        while status != True:
            result = []
            for document_id in self.document_ids:
                url = f"{self.base_url}/api/v1/datasets/{self.dataset_ids[0]}/documents/{document_id}/chunks"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data["data"]["doc"]["progress"] == 1:
                                result.append(data["data"]["doc"]["progress"])
                        else:
                            return {
                                "error": f"Failed to create chat assistant: {response.status}"
                            }
            if len(result) == len(self.document_ids):
                status = True
                return
            else:
                print("...parsing")
            time.sleep(5)

    async def create_chat_assistant(self, iteration):
        url = f"{self.base_url}/api/v1/chats"

        payload = {
            "name": self.auction_id + f" iteration - {iteration}",
            "avatar": "",
            "dataset_ids": self.dataset_ids,
            "llm": (
                {
                    "model_name": "llama3.2",
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "presence_penalty": 0.2,
                    "frequency_penalty": 0.2,
                    "max_token": 1024,
                }
            ),
            "prompt": (
                {
                    "similarity_threshold": 0.75,
                    "keywords_similarity_weight": 1,
                    "top_n": 3,
                    "variables": [{"key": "knowledge", "optional": True}],
                    "empty_response": "",
                    "opener": "Hi! I am your assistant, can I help you?",
                    "show_quote": True,
                    "prompt": """You are an expert document reviewer specializing in procurement. You will be presented with documents from a knowledge base, where each document is a purchase requisition for a specific item. Your task is to thoroughly extract key details from each requisition document and organize them in a structured list format. 
Instructions:
1. Extract Relevant Information: Identify and extract all critical information for each purchase requisition. Focus on details that may be named differently across documents but convey the same semantic meaning as specified in the knowledge base. Use information only from files that stored in {knowledge}.
2. Parameter Matching: Map parameters from the document to their equivalent terms in the knowledge base. Use synonyms, similar expressions, or translations where necessary to recognize corresponding terms, even if phrasing varies.
3. Output Format: Provide the extracted information in JSON format, with each key representing a parameter and its associated value extracted from the document.
4. Knowledge Base: Here is the knowledge base for reference:
   {knowledge}
Use this information to guide the extraction process.
Please respond with the JSON format only.""",
                }
            ),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.chat_id = data["data"]["id"]
                else:
                    return {
                        "error": f"Failed to create chat assistant: {response.status}"
                    }

    async def ask_question(self, question):
        url = f"{self.base_url}/api/v1/chats/{self.chat_id}/completions"
        payload = {"question": question, "stream": False}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data["data"]["answer"])
                    return data
                else:
                    return {"error": f"Failed to ask question: {response.status}"}


if __name__ == "__main__":
    test = RAGFlowAPIClient("9869982")
    asyncio.run(test.create_dataset())
    asyncio.run(test.upload_documents())
    asyncio.run(test.parse_documents())
    asyncio.run(test.check_parse())
    asyncio.run(test.create_chat_assistant(1))
    asyncio.run(
        test.ask_question(
            """Оцените соответствие характеристик товара на основе запроса, используя только данные, содержащиеся в документе. Не делайте догадок и не предполагаете информацию, которой нет в тексте, а также не бери данные из запроса. Для каждой характеристики предоставьте процент соответствия от 0% до 100%, а также объяснение причины оценки, ссылаясь на документ. Запрос требует следующие характеристики для товара: 'Игровой набор бадминтон Start Up R-206 (2 ракетки, волан, чехол) ч/кр 159598'. Характеристики для оценки следующие: 1. 'Цвет' с ожидаемым значением 'черный/красный'. 2. 'Тип' с ожидаемым значением 'бадминтон'. 3. 'Материал' с ожидаемым значением 'металл/пластик'. Проверьте каждую характеристику в документе, исходя исключительно из упоминаний в нем. Верните результат в следующем формате:  [ {\"characteristic\": \"Характеристика\", \"match_percent\": \"Процент соответствия\", \"message\": \"Причина оценки\"} ]"""
        )
    )
