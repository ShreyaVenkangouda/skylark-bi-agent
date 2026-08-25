import requests

from app.config import settings


class MondayAPIError(Exception):
    pass


class MondayClient:

    URL = "https://api.monday.com/v2"

    def __init__(self):

        if not settings.MONDAY_API_TOKEN:

            raise MondayAPIError(
                "MONDAY_API_TOKEN is missing."
            )

        self.headers = {
            "Authorization":
                settings.MONDAY_API_TOKEN,

            "Content-Type":
                "application/json"
        }


    def query(
        self,
        query,
        variables=None
    ):

        payload = {
            "query": query
        }

        if variables:
            payload["variables"] = variables

        try:

            response = requests.post(
                self.URL,
                json=payload,
                headers=self.headers,
                timeout=30
            )

            response.raise_for_status()

        except requests.RequestException as exc:

            raise MondayAPIError(
                f"Monday API request failed: {exc}"
            )

        data = response.json()

        if "errors" in data:

            raise MondayAPIError(
                str(data["errors"])
            )

        return data.get(
            "data",
            {}
        )