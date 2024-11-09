import os
import json
import time

import aiohttp
import urllib.parse

from typing import Any, Dict


async def get_file(auction_id: str, file_id: str):
    url = f"https://zakupki.mos.ru/newapi/api/FileStorage/Download?id={file_id}"
    dir_path = f"data/{auction_id}"
    os.makedirs(dir_path, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Попробуем получить имя файла из заголовков ответа, если доступно
                content_disposition = response.headers.get("Content-Disposition", "")
                filename = None
                # Проверяем, содержит ли заголовок параметр filename*
                if "filename*=" in content_disposition:
                    # Извлекаем закодированное имя файла после 'filename*='
                    encoded_filename = content_disposition.split("filename*=")[
                        -1
                    ].split("''")[-1]
                    # Декодируем UTF-8
                    filename = urllib.parse.unquote(encoded_filename)
                elif "filename=" in content_disposition:
                    # Если обычное имя файла (для простых случаев)
                    filename = content_disposition.split("filename=")[-1].strip('"')

                # Если filename не найден, используем auction_id как имя файла
                if not filename:
                    filename = f"{auction_id}.file"

                # Сохраняем файл в указанную директорию
                file_path = os.path.join(dir_path, filename)
                with open(file_path, "wb") as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"File saved as {file_path}")
            else:
                print(f"Failed to download file. HTTP status: {response.status}")


async def get_item_additional_info(item_id: int) -> Dict[str, Any]:
    url = f"https://zakupki.mos.ru/newapi/api/Auction/GetAuctionItemAdditionalInfo?itemId={item_id}"

    async with aiohttp.ClientSession() as client:
        try:
            async with client.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Request error for item {item_id}: {e}")
        except aiohttp.ContentTypeError:
            print(f"Invalid response format for item {item_id}; expected JSON.")
        return {}


async def get_documents(auction_id: str) -> Dict[str, Any]:
    url = f"https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={auction_id}"

    async with aiohttp.ClientSession() as client:
        try:
            # Fetch auction data
            async with client.get(url) as response:
                response.raise_for_status()
                auction_data = await response.json()
                print(f"Auction data {auction_id} fetched successfully.")

                # Fetch additional info for each item in the auction
                for item in auction_data.get("items", []):
                    item_id = item.get("id")
                    if item_id:
                        additional_info = await get_item_additional_info(item_id)
                        item["additionalInfo"] = additional_info
                        time.sleep(5)

                folder_path = os.path.join("data", auction_id)
                os.makedirs(folder_path, exist_ok=True)

                file_path = os.path.join(folder_path, "data.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(auction_data, f, ensure_ascii=False, indent=4)

                print(f"Data written to {file_path}.")

                for file_id in [item["id"] for item in auction_data["files"]]:
                    await get_file(
                        file_id=file_id,
                        auction_id=auction_id,
                    )
                    time.sleep(5)

                return auction_data
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
        except aiohttp.ContentTypeError:
            print("Invalid response format; expected JSON.")
        return {}
