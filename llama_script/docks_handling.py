from docx import Document
import json

class DocxHandler:
    def __init__(self, file_path):
        doc = Document(file_path)
        text_data = []
    
        # Последовательно обрабатываем все элементы документа
        for element in doc.element.body:
            if element.tag.endswith('p'):  # Если это параграф
                paragraph = element.xpath('.//w:t')
                text = ''.join(node.text for node in paragraph if node.text)
                if text.strip():
                    text_data.append(text.strip())
                    
            elif element.tag.endswith('tbl'):  # Если это таблица
                table_data = []
                for row in element.xpath('.//w:tr'):
                    row_data = []
                    for cell in row.xpath('.//w:t'):
                        if cell.text and cell.text.strip():
                            row_data.append(cell.text.strip())
                    if row_data:
                        table_data.append('\t'.join(row_data))
                if table_data:
                    text_data.append('\n'.join(table_data))
    
        # Применяем очистку текста
        self.result_text = self.ClearText(text_data)
    
    def ClearText(self, text_data):
        """
        Очищает текст от пустых строк и лишних пробелов
        """
        cleaned_text = []
        for text in text_data:
            if text.strip():
                # Заменяем множественные пробелы на один
                cleaned_line = ' '.join(text.split())
                cleaned_text.append(cleaned_line)
        
        return "\n".join(filter(None, cleaned_text))
    
    
    def AddToDataSet(self, input_text, output_text, output_file="training_data.jsonl"):
        """
        Сохраняет пару input-output в JSONL файл
        Args:
            input_text (str): Исходный текст для обучения
            output_file (str): Путь к файлу для сохранения данных
        """
        data = {
            "input": input_text + "\n" + self.result_text,
            "output": output_text
        }
        
        # Открываем файл в режиме добавления (append)
        with open(output_file, 'a', encoding='utf-8') as f:
            # Записываем одну JSON строку и добавляем перенос строки
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')

# Пример использования
if __name__ == "__main__":
    handler = DocxHandler("example_1.docx")
    
    input_text = "Найди в тексте ниже наименование закупки. В тексте оно может быть размещено на нескольких строках, между строками могут быть разрывы. Необходимо, чтобы наименование закупки в твоём ответе в точности соответствовало наименованию закупки в тексте. Ответ должен быть полностью на русском языке, написанный русскими буквами (кириллицей)"
    output_text = "Бутилированная питьевая вода «Фарватер Люкс», 19 л"
    
    # Сохраняем в JSONL
    handler.AddToDataSet(input_text, output_text)
    print("Данные успешно сохранены в training_data.jsonl")
