import requests
import json
import base64

class RagflowApi:
    def __init__(self, address: str, api_key: str):
        self.base_url = f"http://{address}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

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

    #def upload_file(self, path_to_file: str, id_dataset: str):


con = RagflowApi('localhost:9380','ragflow-JhZDM0MmM3OWU1NTExZWY5NGQzMDI0Mm')

print(con.create_dataset('test_4'))
