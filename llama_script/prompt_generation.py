import json

def generate_prompts(file_path):
    # Load data from the provided JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract relevant fields
    name = data['name']
    is_contract_guarantee_required = data['isContractGuaranteeRequired']
    is_license_production = data['isLicenseProduction']
    delivery_stages = data['deliveryStage']
    contract_cost = data['contractCost']
    start_cost = data['startCost']
    items = data['items']
    
    # Start building the list of prompts
    prompts = {}
    
    # Prompt for "name"
    prompts['name'] = f"Документ должен содержать упоминание об объекте закупки: '{name}', часто обозначенных как 'объект закупки'."
    
    # Prompt for "isContractGuaranteeRequired"
    if is_contract_guarantee_required:
        prompts['is_contract_guarantee_required'] = "Документ должен включать указание о необходимости исполнения контракта или аналогичную формулировку."
    else:
        prompts['is_contract_guarantee_required'] = "В документе не должно быть информации о необходимости исполнения контракта или должно быть указано, что такой необходимости нет."
    
    # Prompt for "isLicenseProduction"
    if is_license_production:
        prompts['is_license_production'] = "Документ должен содержать указание о необходимости наличия лицензий или сертификатов или информацию с аналогичной формулировкой."
    else:
        prompts['is_license_production'] = "В документе не должно быть информации о необходимости лицензий или сертификатов, либо должно быть указано, что они не требуются."
    
    prompts['delivery_stages'] = []
    
    # Prompts for "deliveryStage"
    for stage in delivery_stages:
        delivery_place = stage['deliveryPlace']
        period_from = stage['periodDateFrom']
        period_to = stage['periodDateTo']
        prompts['delivery_stages'].append(f"Документ должен содержать информацию о месте доставки: '{delivery_place}', с указанием начальной даты: '{period_from}' и конечной даты: '{period_to}'.")
    
    # Prompts for "contractCost" and "startCost"
    if contract_cost is not None:
        prompts["contract_cost"] = f"Документ должен содержать явное указание цены контракта: {contract_cost}."
    if start_cost is not None:
        prompts["contract_cost"] = f"Документ должен содержать явное указание стартовой цены: {start_cost}."
    
    prompts['items'] = []
    # Prompts for "items"
    for idx, item in enumerate(items):
        item_name = item['name']
        
        item_characteristics = []
        for characteristic in item['characteristics']:
            char_name = characteristic['name']
            char_value = characteristic['value']
            item_characteristics.append(f"- Характеристика '{char_name}' с значением '{char_value}'.")
        
        prompts['items'].append({item_name: f"Документ должен содержать упоминание о товаре '{item_name}' с перечислением характеристик:", "characteristics": item_characteristics})
    
    return prompts

# Пример использования
if __name__ == '__main__':
    file_path = 'data_unpacked.json'
    result = generate_prompts(file_path)
    print(result)