import os
import json


def generate_prompts(auction_id: str):
    request_keys = [
        "name",
        "is_contract_guarantee_required",
        "is_license_production",
        "delivery_stages",
        "cost",
        "items",
    ]

    try:
        folder_path = os.path.join("../data", auction_id)
        file_path = os.path.join(folder_path, "data.json")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        prompts = {}

        prompts["name"] = (
            f"Документ должен содержать упоминание об объекте закупки: *{data['name']}*, часто обозначенных как 'объект закупки'."
        )

        is_contract_guarantee_required = data["isContractGuaranteeRequired"]
        if is_contract_guarantee_required:
            prompts["is_contract_guarantee_required"] = (
                "Документ должен включать указание о необходимости исполнения контракта или аналогичную формулировку."
            )
        else:
            prompts["is_contract_guarantee_required"] = (
                "В документе не должно быть информации о необходимости исполнения контракта или должно быть указано, что такой необходимости нет."
            )

        is_license_production = data["isLicenseProduction"]
        if is_license_production:
            prompts["is_license_production"] = (
                "Документ должен содержать указание о необходимости наличия лицензий или сертификатов или информацию с аналогичной формулировкой."
            )
        else:
            prompts["is_license_production"] = (
                "В документе не должно быть информации о необходимости лицензий или сертификатов, либо должно быть указано, что они не требуются."
            )

        contract_cost = data["contractCost"]
        start_cost = data["startCost"]
        if contract_cost is not None:
            prompts["cost"] = (
                f"Документ должен содержать явное указание цены контракта: *{contract_cost}*."
            )
        if start_cost is not None:
            prompts["cost"] = (
                f"Документ должен содержать явное указание стартовой цены: *{start_cost}*."
            )

        prompts["delivery_stages"] = []

        for delivery in data["deliveries"]:
            delivery_place = delivery["deliveryPlace"]
            period_from = delivery["periodDateFrom"]
            period_to = delivery["periodDateTo"]
            prompts["delivery_stages"].append(
                f"Документ должен содержать информацию о месте доставки: *{delivery_place}*, с указанием начальной даты: *{period_from}* и конечной даты: *{period_to}*."
            )

        prompts["items"] = []
        for item in data["items"]:
            item_name = item["name"]

            characteristics = []
            for characteristic in item["additionalInfo"]["characteristics"]:
                char_name = characteristic["name"]
                char_value = characteristic["value"]
                characteristics.append(
                    f"- Характеристика *{char_name}* с значением *{char_value}*."
                )

            prompts["items"].append(
                {
                    "item_name": f"Документ должен содержать упоминание о товаре *{item_name}* с перечислением характеристик:",
                    "characteristics": characteristics,
                }
            )

        requested_prompts = []
        for key in request_keys:
            if type(prompts[key]) is list:
                for prompt in prompts[key]:
                    requested_prompts.append(prompt)
            else:
                requested_prompts.append(prompts[key])

        return requested_prompts

    except Exception as e:
        print(f"Error generating prompts: {e}")
        return []


# Пример использования
if __name__ == "__main__":
    generate_prompts("9869982")
