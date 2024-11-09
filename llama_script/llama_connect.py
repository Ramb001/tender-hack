import requests


class LlamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def send_query(self, prompt):
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            # response.raise_for_status()
            
            return response.json()["response"]
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к модели: {str(e)}")
            return None


if __name__ == "__main__":
	# Создаем экземпляр клиента
	client = LlamaClient()

	# prompt = f"Найди в предложенном ниже тексте наименование закупки. В тексте оно может быть размещено на нескольких строках, между строками могут быть разрывы. Необходимо, чтобы наименование закупки в твоём ответе в точности соответствовало наименованию закупки в тексте. Ответ должен быть полностью на русском языке, написанный русскими буквами (кирилицей).\n {text_data}"
	# response = client.send_query(prompt)
	# print("Ответ модели:", response)

