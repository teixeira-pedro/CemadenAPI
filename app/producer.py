from kafka import KafkaProducer 
from time import sleep
from json import dumps

class KafkaProducer():

    def __init__(self):
        self.producer = self.__iniciar_producer()
        pass

    def __iniciar_producer(self) -> KafkaProducer:
        """
        Funcao que retorna um producer de topico kafka
        """
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9093'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
        return producer

    def enviar_mensagem(self, conteudo: dict, producer: KafkaProducer):
        """
        Envio de mensagem para o kafka
        """
        producer.send('topic-test', value=conteudo)
        sleep(0.5)