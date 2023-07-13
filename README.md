## Como executar o trabalho?

1. É necessário ter o docker instalado.

2. Abra o terminal do windows em duas janelas.

3. Vá até a raíz do projeto e execute o comando:
```bash
docker-compose up -d
```

4. No primeiro terminal realize o comando para listar os ids dos containeres:
```bash
docker ps
```

5. uma saída semelhante a saída abaixo será impressa:
```bash
CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS          PORTS
           NAMES
89c1f577daa0   cemadenapi_extractionscript        "tail -f /dev/null"      42 seconds ago   Up 38 seconds
           cemadenapi_extractionscript_1
6c236a18ec0d   cemadenapi_spark-master            "/bin/bash /start-sp…"   42 seconds ago   Up 38 seconds   6066/tcp, 0.0.0.0:7077->7077/tcp, 0.0.0.0:9000->8080/tcp   cemadenapi_spark-master_1
dbb670ba96e9   confluentinc/cp-kafka:latest       "/etc/confluent/dock…"   42 seconds ago   Up 38 seconds   0.0.0.0:9092->9092/tcp
           cemadenapi_kafka_1
36b297e230b1   mysql:5.7                          "docker-entrypoint.s…"   45 seconds ago   Up 42 seconds   33060/tcp, 0.0.0.0:32001->3306/tcp
           mydb
3907c3c2fecd   confluentinc/cp-zookeeper:latest   "/etc/confluent/dock…"   45 seconds ago   Up 42 seconds   2888/tcp, 0.0.0.0:2181->2181/tcp, 3888/tcp                 cemadenapi_zookeeper_1
```

6. No primeiro terminal, copie o CONTAINER ID da imagem: cemadenapi_spark-master. E execute o comando: 
```bash
docker exec -it 6c236a18ec0d spark-submit /opt/spark-apps/example.py
```

7. No segundo terminal, copie o CONTAINER ID da imagem: cemadenapi_extractionscript. E execute o comando:
```bash
docker exec -it 89c1f577daa0 python cemadem_app/app/driver_.py
```

8. Agora você terá o programa executando corretamente.
