import json

def get_data_from_json(input_file):
    try:
        # Открываем исходный JSON файл и загружаем данные
        with open(f"{input_file}.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        extracted_data = {}

        extracted_data["name"] = data["name"]
        extracted_data["isContractGuaranteeRequired"] = data["isContractGuaranteeRequired"]
        extracted_data["isLicenseProduction"] = data["isLicenseProduction"]
        extracted_data["deliveryStage"] = []
        
        for delivery in data["deliveries"]:
            extracted_data["deliveryStage"].append({
                "deliveryPlace": delivery["deliveryPlace"],	
                "periodDateFrom": delivery["periodDateFrom"],
                "periodDateTo": delivery["periodDateTo"]
            })

        extracted_data["contractCost"] = data["contractCost"]
        extracted_data["startCost"] = data["startCost"]
        extracted_data["items"] = []

        for item in data["items"]:
            extracted_data["items"].append({
                "name": item["name"],
                "characteristics": item["additionalInfo"]["characteristics"]
            })

        # Записываем извлечённые данные в новый JSON файл
        with open(f"{input_file}_unpacked.json", 'w', encoding='utf-8') as file:
            json.dump(extracted_data, file, ensure_ascii=False, indent=4)
        
        print(f"Данные успешно сохранены в {input_file}_unpacked.json")
    
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON файла.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    get_data_from_json('9864708')