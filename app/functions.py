import requests


def send_to_telegram(bottoken: str, chatid: str, message: str):
    url = f"https://api.telegram.org/bot{bottoken}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chatid, "text": message})
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"ok": False, "error": f"HTTP error: {http_err}"}
    except Exception as err:
        return {"ok": False, "error": f"Error: {err}"}
    return response.json()