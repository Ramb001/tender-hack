import json

# Load data from the provided JSON file
file_path = '9864708_unpacked.json'
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
prompts = []

# Prompt for "name"
prompts.append(f"Документ должен содержать упоминание об объекте закупки: '{name}', часто обозначенном как 'объект закупки'.")

# Prompt for "isContractGuaranteeRequired"
if is_contract_guarantee_required:
    prompts.append("Документ должен включать указание о необходимости исполнения контракта или аналогичную формулировку.")
else:
    prompts.append("В документе не должно быть информации о необходимости исполнения контракта или должно быть указано, что такой необходимости нет.")

# Prompt for "isLicenseProduction"
if is_license_production:
    prompts.append("Документ должен содержать указание о необходимости наличия лицензий или сертификатов или информацию с аналогичной формулировкой.")
else:
    prompts.append("В документе не должно быть информации о необходимости лицензий или сертификатов, либо должно быть указано, что они не требуются.")

# Prompts for "deliveryStage"
for stage in delivery_stages:
    delivery_place = stage['deliveryPlace']
    period_from = stage['periodDateFrom']
    period_to = stage['periodDateTo']
    prompts.append(f"Документ должен содержать информацию о месте доставки: '{delivery_place}', с указанием начальной даты: '{period_from}' и конечной даты: '{period_to}'.")

# Prompts for "contractCost" and "startCost"
if contract_cost is not None:
    prompts.append(f"Документ должен содержать явное указание цены контракта: {contract_cost}.")
if start_cost is not None:
    prompts.append(f"Документ должен содержать явное указание стартовой цены: {start_cost}.")

# Prompts for "items"
for item in items:
    item_name = item['name']
    prompts.append(f"Документ должен содержать упоминание о товаре '{item_name}' с перечислением характеристик:")
    for characteristic in item['characteristics']:
        char_name = characteristic['name']
        char_value = characteristic['value']
        prompts.append(f"- Характеристика '{char_name}' с значением '{char_value}'.")

# Print the generated prompts
for i, prompt in enumerate(prompts, 1):
    print(f"{i}. {prompt}")