import requests
import json
import base64
import time

class RagflowApi:
    def __init__(self, address: str, api_key: str):
        self.base_url = f"http://{address}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.api_key = api_key

    def create_dataset(self, name: str, avatar_path: str = None, description: str = None, 
                       language: str = "English", embedding_model: str = None, 
                       permission: str = "me", chunk_method: str = "naive", 
                       parser_config: dict = None):
        
        url = f"{self.base_url}/datasets"
        
        
        # Настройки по умолчанию для parser_config
        if not parser_config:
            parser_config = {
                "chunk_token_count": 128,
                "layout_recognize": True,
                "html4excel": False,
                "delimiter": "\n!?。；！？",
                "task_page_size": 12,
                "raptor": {"use_raptor": False}
            }

        data = {
            "name": name,
            "description": description,
            "language": language,
            "embedding_model": embedding_model,
            "permission": permission,
            "chunk_method": chunk_method,
            "parser_config": parser_config
        }

        # Удаляем None значения из тела запроса
        data = {key: value for key, value in data.items() if value is not None}
        
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return response.json()


    def parse_files(self, dataset_id: str, document_ids: list):
        """
        Создает чанки (фрагменты) для загруженных документов.
        """
        url = f"{self.base_url}/datasets/{dataset_id}/chunks"
        data = {
            "document_ids": document_ids
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            print(f"Документы успешно обработаны и разбиты на чанки.")
            return response.json()
        else:
            print(f"Ошибка обработки документов: {response.status_code} - {response.text}")
            return None
        

    def upload_document(self, file_path: str, dataset_id: str):
        url = f"{self.base_url}/datasets/{dataset_id}/documents"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        # Открываем файл в бинарном режиме
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file, 'application/octet-stream')}
            
            # Отправляем файл с использованием параметра `files`
            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            print("Документ успешно загружен.")
            return response.json()
        else:
            print(f"Ошибка загрузки документа: {response.status_code} - {response.text}")
            return None
        


    def create_chat_assistent(self, name: str, dataset_ids: list):
        """
        Создает чат-помощника с заданными параметрами.
        """
        url = f"{self.base_url}/chats"
        data = {
            "name": name,
            "dataset_ids": dataset_ids
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Чат успешно создан.")
            return response.json()
        else:
            print(f"Ошибка создания чата: {response.status_code} - {response.text}")
            return None
        
    def create_session(self, chat_id: str, session_name: str):
        """
        Создает сессию для указанного чата.
        """
        url = f"{self.base_url}/chats/{chat_id}/sessions"
        data = {
            "name": session_name
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Сессия успешно создана.")
            return response.json()
        else:
            print(f"Ошибка создания сессии: {response.status_code} - {response.text}")
            return None

    def ask_question(self, chat_id: str, question: str, session_id: str = None, stream: bool = False):
        """
        Отправляет вопрос в чат для начала диалога с AI.

        :param chat_id: str - Идентификатор чата.
        :param question: str - Вопрос, который будет задан AI.
        :param session_id: str (опционально) - Идентификатор сессии. Если не указан, будет создана новая сессия.
        :param stream: bool - Флаг для включения потоковой передачи ответа.
        :return: dict - Ответ от API с результатом вопроса.
        """
        url = f"{self.base_url}/chats/{chat_id}/completions"
        data = {
            "question": question,
            "stream": stream
        }

        # Добавляем session_id, если он указан
        if session_id:
            data["session_id"] = session_id

        # Отправляем POST-запрос
        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        # Обрабатываем ответ
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка запроса: {response.status_code} - {response.text}")
            return None

con = RagflowApi('localhost:9380','ragflow-JhZDM0MmM3OWU1NTExZWY5NGQzMDI0Mm')

path_files = ['backend/src/ks/2.docx', 'backend/src/ks/3.pdf']


def get_name_buys(path_files):
    con = RagflowApi('localhost:9380','ragflow-JhZDM0MmM3OWU1NTExZWY5NGQzMDI0Mm')
    dataset_id = con.create_dataset('dddadaadadвada')['data']['id']
    files_ids = []

    for path in path_files:
        files_ids.append(con.upload_document(path, dataset_id)['data'][0]['id'])
    
    con.parse_files(dataset_id, files_ids)
    
    time.sleep(200)

    chat_id = con.create_chat_assistent('search_bot', [dataset_id,])['data']['id']

print(con.ask_question('995d848d9e8111efa96d0242ac120006', 'Выпиши мне Главную суть документа, будь что "поставка товаров", "закупка товаров" выпиши именно как в доументе написано это одна фраза. Давай пример введу'))


#get_name_buys(path_files)


