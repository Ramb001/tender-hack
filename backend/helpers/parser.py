import aiohttp
import json
import os
from typing import Any, Dict


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
            async with client.get(url) as response:
                response.raise_for_status()
                auction_data = await response.json()
                print(f"Auction data {auction_id} fetched successfully.")

                for item in auction_data.get("items", []):
                    item_id = item.get("id")
                    if item_id:
                        additional_info = await get_item_additional_info(item_id)
                        item["additionalInfo"] = additional_info

                os.makedirs("data", exist_ok=True)

                file_path = os.path.join("data", f"{auction_id}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(auction_data, f, ensure_ascii=False, indent=4)

                print(f"Data written to {file_path}.")
                return auction_data
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
        except aiohttp.ContentTypeError:
            print("Invalid response format; expected JSON.")
        return {}
