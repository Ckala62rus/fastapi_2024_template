class HelloService:

    @staticmethod
    async def hello(self) -> dict:
        return {
            "id": 1,
            "name": "some name",
            "age": "some age",
            "phone": "88005553535",
        }
