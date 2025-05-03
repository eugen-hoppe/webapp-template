class UserCRUD:
    def __init__(self) -> None:
        self._db = {}

    async def get_by_id(self, user_id: str) -> dict[str, str]:
        return self._db.get(user_id)

    async def create(self, user: dict[str, str]) -> None:
        self._db[user.get("id")] = user

    async def delete(self, user_id):
        del self._db[user_id]
