from pycaprio import Pycaprio


class InceptionClient:
    @staticmethod
    def create_client(host, username, password):
        return Pycaprio(
            inception_host=host,
            authentication=(username, password)
        )
