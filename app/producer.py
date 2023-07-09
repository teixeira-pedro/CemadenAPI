from kafka import KafkaProducer as kp
from time import sleep
from json import dumps
from json_resolver import json_serial

class ProdutorTopico():

    def __init__(self):
        self.producer = self.__iniciar_producer()
        pass

    def __iniciar_producer(self) -> kp:
        """
        Funcao que retorna um producer de topico kafka
        """
        producer = kp(bootstrap_servers=['kafka:9093'], value_serializer=lambda x: dumps(x, default=json_serial).encode('utf-8'))
        return producer

    def enviar_mensagem(self, conteudo: dict, producer: kp):
        """
        Envio de mensagem para o kafka
        """
        producer.send('topic-test', value=conteudo)
        sleep(0.2)