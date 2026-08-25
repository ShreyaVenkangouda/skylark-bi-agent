import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    MONDAY_API_TOKEN = os.getenv(
        "MONDAY_API_TOKEN"
    )

    DEALS_BOARD_ID = os.getenv(
        "DEALS_BOARD_ID"
    )

    WORK_ORDERS_BOARD_ID = os.getenv(
        "WORK_ORDERS_BOARD_ID"
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )


settings = Settings()