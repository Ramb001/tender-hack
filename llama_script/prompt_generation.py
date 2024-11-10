import json

def GeneratePrompts(file_path, request_keys):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    all_prompts = {}
    
    all_prompts['name'] = f"Документ должен содержать упоминание об объекте закупки: *{data['name']}*, часто обозначенных как 'объект закупки'."

    is_contract_guarantee_required = data['isContractGuaranteeRequired']
    if is_contract_guarantee_required:
        all_prompts['is_contract_guarantee_required'] = "Документ должен включать указание о необходимости исполнения контракта или аналогичную формулировку."
    else:
        all_prompts['is_contract_guarantee_required'] = "В документе не должно быть информации о необходимости исполнения контракта или должно быть указано, что такой необходимости нет."

    
    is_license_production = data['isLicenseProduction']
    if is_license_production:
        all_prompts['is_license_production'] = "Документ должен содержать указание о необходимости наличия лицензий или сертификатов или информацию с аналогичной формулировкой."
    else:
        all_prompts['is_license_production'] = "В документе не должно быть информации о необходимости лицензий или сертификатов, либо должно быть указано, что они не требуются."

    contract_cost = data['contractCost']
    start_cost = data['startCost']
    if contract_cost is not None:
        all_prompts['cost'] = f"Документ должен содержать явное указание цены контракта: *{contract_cost}*."
    if start_cost is not None:
        all_prompts['cost'] = f"Документ должен содержать явное указание стартовой цены: *{start_cost}*."


    all_prompts['delivery_stages'] = []
    
    for delivery in data["deliveries"]:
        delivery_place = delivery['deliveryPlace']
        period_from = delivery['periodDateFrom']
        period_to = delivery['periodDateTo']
        all_prompts['delivery_stages'].append(f"Документ должен содержать информацию о месте доставки: *{delivery_place}*, с указанием начальной даты: *{period_from}* и конечной даты: *{period_to}*.")

    all_prompts['items'] = []
    for item in data["items"]:
        item_name = item['name']

        characteristics = []
        for characteristic in item["additionalInfo"]['characteristics']:
            char_name = characteristic['name']
            char_value = characteristic['value']
            characteristics.append(f"- Характеристика *{char_name}* с значением *{char_value}*.")

        all_prompts['items'].append({"item_name": f"Документ должен содержать упоминание о товаре *{item_name}* с перечислением характеристик:", "characteristics": characteristics})
  
    prompts_list = []
    for key in request_keys:
        if type(all_prompts[key]) is list:
            for prompt in all_prompts[key]:
                prompts_list.append(prompt)
        else:
            prompts_list.append(all_prompts[key])

    return prompts_list

# Пример использования
if __name__ == '__main__':
    file_path = 'data.json'

    request_keys = ['name', 'is_contract_guarantee_required', 'is_license_production', 'delivery_stages', 'cost', 'items']
    result = GeneratePrompts(file_path, request_keys)

    with open("prompts.json", 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    print(result)