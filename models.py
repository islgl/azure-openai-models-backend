# Fetch available Azure OpenAI models from the API

import requests


def fetch_available_models(base_url: str, api_version: str, api_key: str):
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    url = f"{base_url}/models?api-version={api_version}"
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    result = response.json()
    data = result.get('data', [])
    return data
