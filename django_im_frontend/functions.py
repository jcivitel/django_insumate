from datetime import datetime

import requests


def get_product_info(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == 1:
            product = data["product"]
            carbs = product.get("nutriments", {}).get("carbohydrates_100g")
            return {
                "code": product.get("code"),
                "name": product.get("product_name"),
                "carbs": carbs,
            }
    return None


def get_current_factor(profile):
    current_time = datetime.now().time()

    if current_time < datetime.strptime("11:00", "%H:%M").time():
        return "morning", profile.morning_factor
    elif current_time < datetime.strptime("17:00", "%H:%M").time():
        return "noon", profile.noon_factor
    else:
        return "evening", profile.evening_factor
