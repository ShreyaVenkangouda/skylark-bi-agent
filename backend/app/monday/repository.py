from app.monday.client import MondayClient


class MondayRepository:

    def __init__(self):

        self.client = MondayClient()


    def get_board(self, board_id):

        query = """
        query ($board_id: ID!) {

            boards(ids: [$board_id]) {

                id
                name

                columns {
                    id
                    title
                    type
                }
            }
        }
        """

        result = self.client.query(
            query,
            {
                "board_id": str(
                    board_id
                )
            }
        )

        boards = result.get(
            "boards",
            []
        )

        if not boards:

            raise ValueError(
                f"Board {board_id} not found."
            )

        return boards[0]


    def get_all_items(
        self,
        board_id
    ):

        query = """
        query (
            $board_id: ID!,
            $cursor: String
        ) {

            boards(ids: [$board_id]) {

                items_page(
                    limit: 500,
                    cursor: $cursor
                ) {

                    cursor

                    items {

                        id
                        name

                        column_values {

                            id
                            text
                            value
                            type
                        }
                    }
                }
            }
        }
        """

        items = []

        cursor = None

        while True:

            result = self.client.query(
                query,
                {
                    "board_id":
                        str(board_id),

                    "cursor":
                        cursor
                }
            )

            boards = result.get(
                "boards",
                []
            )

            if not boards:
                break

            page = boards[0][
                "items_page"
            ]

            items.extend(
                page.get(
                    "items",
                    []
                )
            )

            cursor = page.get(
                "cursor"
            )

            if not cursor:
                break

        return items


    def get_board_data(
        self,
        board_id
    ):

        board = self.get_board(
            board_id
        )

        items = self.get_all_items(
            board_id
        )

        return {
            "board": board,
            "items": items
        }