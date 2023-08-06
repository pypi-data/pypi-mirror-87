import requests


def set_cosmosdb_rus(url: str, api_token: str, rus: int = 4000, mode: str = "automatic") -> None:
    headers = {"x-functions-key": api_token}
    response = requests.post(url,
                             params={
                                 "mode": mode,
                                 "maxThroughput": rus
                             },
                             headers=headers)

    response.raise_for_status()


def get_cosmosdb_rus(url: str, api_token: str, account_name: str) -> dict:
    headers = {"x-functions-key": api_token}
    response = requests.get(url,
                            params={
                                "accountName": account_name,
                            },
                            headers=headers)

    response.raise_for_status()

    return response.json()
