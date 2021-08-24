import motor.motor_asyncio


class SingletonClient:
    client = None
    db = None

    @staticmethod
    def get_client():
        if SingletonClient.client is None:
            MONGODB_HOSTNAME = 'localhost'
            MONGODB_PORT = '27017'

            SingletonClient.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://{}:{}".format(
                MONGODB_HOSTNAME, str(MONGODB_PORT)))

        return SingletonClient.client

    @staticmethod
    def get_data_base():
        if SingletonClient.db is None:
            client = SingletonClient.get_client()
            MONGODB_DATABASE = 'eshop'
            SingletonClient.db = client[MONGODB_DATABASE]

        return SingletonClient.db