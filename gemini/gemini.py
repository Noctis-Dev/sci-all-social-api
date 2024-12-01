import requests

from exeption.gemini import ResponseError
from google.oauth2 import service_account
from google.auth.transport.requests import Request


API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
access_token = None


def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        "gemini/auth.json",
        scopes=["https://www.googleapis.com/auth/generative-language"],
    )

    credentials.refresh(Request())
    return credentials.token


async def send_message(message, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "contents": [
            {"parts": [{"text": message}]}
        ]
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (IndexError, KeyError, TypeError):
            return "Unexpected content"

    elif response.status_code == 401:
        token = get_access_token()
        return await send_message(message, token)

    elif response.status_code == 403:
        token = get_access_token()
        return await send_message(message, token)

    else:
        raise ResponseError(response.status_code, response.text)
