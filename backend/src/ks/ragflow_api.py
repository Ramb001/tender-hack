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
        

    def list_chunks(self, dataset_id: str, document_id: str, keywords: str = '', page: int = 1, page_size: int = 1024):
        """
        List all chunks of a specific document.
        """
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}/chunks"
        params = {
            "keywords": keywords,
            "page": page,
            "page_size": page_size
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching chunks: {response.status_code} - {response.text}")
            return None


    def create_chat_assistent(self, name: str, dataset_ids: list):
        """
        Создает чат-помощника с заданными параметрами.
        """
        url = f"{self.base_url}/chats"
        data = {
            "name": name,
            "dataset_ids": dataset_ids,
            'prompt':{
                'empty_response': '0'
            }
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Чат успешно создан.")
            return response.json()
        else:
            print(f"Ошибка создания чата: {response.status_code} - {response.text}")
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
            return response.json()['data']['answer']
        else:
            print(f"Ошибка запроса: {response.status_code} - {response.text}")
            return None
    

    def delete_chunks(self, dataset_id: str, document_id: str, chunk_ids: list):
        """
        Delete chunks by their IDs.
        """
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}/chunks"
        data = {
            "chunk_ids": chunk_ids
        }
        response = requests.delete(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error deleting chunks: {response.status_code} - {response.text}")
            return None
        

    def delete_all_chunks(self, dataset_id: str, document_id: str):
        """
        List and delete all chunks of a given document.
        """
        # Step 1: List all chunks
        chunks_response = self.list_chunks(dataset_id, document_id)
        
        if chunks_response and chunks_response.get('data', {}).get('chunks'):
            # Step 2: Get all chunk IDs
            chunk_ids = [chunk['id'] for chunk in chunks_response['data']['chunks']]
            
            # Step 3: Delete all chunks
            return self.delete_chunks(dataset_id, document_id, chunk_ids)
        else:
            print("No chunks found to delete.")
            return None


    def delete_chat_assistent(self, chat_id: list):
        """
        Удаляет чат-помощника с заданными параметрами.
        """
        url = f"{self.base_url}/chats"
        data = {
            "ids": chat_id
        }

        response = requests.delete(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Чат успешно удален.")
            return response.json()
        else:
            print(f"Ошибка создания чата: {response.status_code} - {response.text}")
            return None
    

    def delete_dataset(self, dataset_ids: list):
        """
        Удаляет dataset.
        """
        url = f"{self.base_url}/datasets"
        data = {
            "ids": dataset_ids
        }

        response = requests.delete(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Датасет успешно удален.")
            return response.json()
        else:
            print(f"Ошибка создания чата: {response.status_code} - {response.text}")
            return None

    def check_document(self, dataset_id):
        url = f"{self.base_url}/document/list?kb_id{dataset_id}"
        data = {

        }
        response = requests.get(url, headers=self.headers, data=json.dumps(data))

        for status in response['data']['docs']:
            if int(status['progress']) != 1:
                return False
            
        return True


def check_status(path_files: list, promts: list, con: RagflowApi, sleep: int=70):
    dataset_id = con.create_dataset('124daвыфsf1d24')['data']['id']
    files_ids = []

    for path in path_files:
        files_ids.append(con.upload_document(path, dataset_id)['data'][0]['id'])
    
    con.parse_files(dataset_id, files_ids)
    
    while(not con.check_document()):
        time.sleep(20)

    chat_id = con.create_chat_assistent('124dвыфdsa12f4', [dataset_id,])['data']['id']
    response = ''
    msg = ''

    for i in range(len(promts)):
        msg += promts[i]
        print(i)

        if i%5==0:
            msg = f"""найди данные, но они не обязательно должны: {msg}
                    Оценивай И ДАЙ ОТВЕТ ТОЛЬКО ЧИСЛОМ соответствия для каждого пункта для данных запроса и данных из документа в процентах от 0 до 100"""
            
            response = f'{response};{con.ask_question(chat_id, msg)}' #Бери вывод какой нужно под 

    if msg != 0:
        msg = f"""найди данные, но они не обязательно должны: {msg}
                    Оценивай И ДАЙ ОТВЕТ ТОЛЬКО ЧИСЛОМ соответствия для каждого пункта для данных запроса и данных из документа в процентах от 0 до 100"""
            
        response = f'{response};{con.ask_question(chat_id, msg)}' #Бери вывод какой нужно под 
        
    con.delete_chat_assistent(chat_id)
    con.delete_dataset(files_ids)

    for document_id in files_ids:
        con.delete_all_chunks(dataset_id, document_id)

    try:
        return sum(map(response.split(';'),int))/ len(prompts)
    except Exception as e:
        return response








# Example  from from ragflow_api import check_status, RagflowApi
con = RagflowApi('localhost:9380','ragflow-JhZDM0MmM3OWU1NTExZWY5NGQzMDI0Mm')

prompts = ["Документ должен содержать упоминание об объекте закупки: *СПОРТИВНОЕ ОБОРУДОВАНИЕ И ИНВЕНТАРЬ*, часто обозначенных как 'объект закупки'.", 'В документе не должно быть информации о необходимости исполнения контракта или должно быть указано, что такой необходимости нет.', 'В документе не должно быть информации о необходимости лицензий или сертификатов, либо должно быть указано, что они не требуются.', 'Документ должен содержать информацию о месте доставки: *г г Москва, Город Москва, улица Профсоюзная, дом 9А*, с указанием начальной даты: *None* и конечной даты: *None*.', 'Документ должен содержать явное указание стартовой цены: *58400.0*.', 'Документ должен содержать упоминание о товаре *Скакалка 2,85 м SKA-285 полнотелый резиновый шнур d-5 мм ручки пластик* с перечислением характеристик:', '- Характеристика *Вес* с значением *50 г*.', '- Характеристика *Длина* с значением *285 см*.', '- Характеристика *Материал* с значением *Резина/пластик*.', '- Характеристика *Материал ручек* с значением *Пластик*.', '- Характеристика *Страна производитель* с значением *Россия*.', '- Характеристика *Цвет* с значением *черный с желтым*.', 'Документ должен содержать упоминание о товаре *Игровой набор бадминтон Start Up R-206 (2 ракетки,волан,чехол) ч/кр 159598* с перечислением характеристик:', '- Характеристика *Цвет* с значением *черный/красный*.', '- Характеристика *Тип* с значением *бадминтон*.', '- Характеристика *Материал* с значением *металл/пластик*.', '- Характеристика *Размер изделия* с значением *625 мм*.', 'Документ должен содержать упоминание о товаре *Мяч футбольный Classic (размер 5)* с перечислением характеристик:', '- Характеристика *Размер мяча* с значением *5*.', '- Характеристика *Способ соединения панелей* с значением *Машинная сшивка*.', '- Характеристика *Уровень игры* с значением *Любительский*.', '- Характеристика *Количество подкладочных слоев* с значением *3 шт*.', '- Характеристика *Количество панелей* с значением *32 шт*.', '- Характеристика *Материал камеры* с значением *Резина*.', '- Характеристика *Материал покрышки* с значением *ПВХ*.', 'Документ должен содержать упоминание о товаре *Мяч волейбольный Mikasa mva 200, размер 5* с перечислением характеристик:', '- Характеристика *Официальный размер мяча (fivb)* с значением *5*.', '- Характеристика *Окружность мяча* с значением *67 см*.', '- Характеристика *Вес* с значением *280 г*.', '- Характеристика *Количество панелей* с значением *8 шт*.', '- Характеристика *Материал камеры* с значением *бутил*.', '- Характеристика *Материал мяча* с значением *искусственная кожа*.', '- Характеристика *Назначение* с значением *для зала*.', '- Характеристика *Тип соединения панелей* с значением *Термосшивка*.', '- Характеристика *Уровень игры* с значением *профессиональный*.', 'Документ должен содержать упоминание о товаре *Мяч волейбольный пляжный Mikasa FIVB VLS 300, размер 5* с перечислением характеристик:', '- Характеристика *Материал покрышки* с значением *композитная кожа*.', '- Характеристика *Размер* с значением *5*.', '- Характеристика *Сертификат* с значением *FIVB*.', '- Характеристика *Технология сшивки* с значением *машинная сшивка*.', '- Характеристика *Уровень игры* с значением *профессиональный*.', '- Характеристика *Цвет* с значением *жёлтый*.', '- Характеристика *Цвет дополнительный* с значением *синий белый*.', '- Характеристика *Количество панелей* с значением *10 шт*.', 'Документ должен содержать упоминание о товаре *Набор воланов TORRES (6 штук) ПВХ* с перечислением характеристик:', '- Характеристика *Вес* с значением *120 г*.', '- Характеристика *Материал* с значением *ПВХ*.', '- Характеристика *Тип* с значением *набор воланов*.', '- Характеристика *Цвет* с значением *белый*.', '- Характеристика *Вид продукции* с значением *Товары*.', '- Характеристика *Виды товаров спортивных* с значением *Спортивное оборудование и инвентарь*.', '- Характеристика *Виды спортивного оборудования и инвентаря* с значением *Оборудование и инвентарь для бадминтона*.', '- Характеристика *Виды оборудования и инвентаря для бадминтона* с значением *Воланы для бадминтона*.','- Характеристика *Длина* с значением *700 мм*.', '- Характеристика *Ширина* с значением *70 мм*.']

path_files = ['backend/src/ks/2.pdf', 'backend/src/ks/1.docx']

print(check_status(path_files=path_files, promts=prompts ,con=RagflowApi('localhost:9380','ragflow-JhZDM0MmM3OWU1NTExZWY5NGQzMDI0Mm'),  sleep=400))




