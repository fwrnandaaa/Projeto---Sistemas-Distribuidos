import pika


def criar_conexao():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )