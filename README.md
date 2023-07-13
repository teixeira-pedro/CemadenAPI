## Como executar o trabalho?

1. É necessário ter o docker instalado.

2. Faça a execução do arquivo, na raíz com o seguinte comando:

```bash
docker-compose up -d
```

3. Com o docker executando na sua máquina e os conteiners executando também. Abra o vscode.

4. No ícone de extensões, faça a instalação da extensão "Remote Development".

5. Após a instalação, matenha o vscode aberto com o projeto. Selecione o atalho Ctrl + Shift + P e selecione a opção: "Remote-Containers: Attach to Running Container ..."


6. Selecione o container "cemadenapi_extractionscript_1", ele será aberto em um novo vscode.

7. Selecione novamente no vscode anterior a opção ""Remote-Containers: Attach to Running Container ..." e escolha o container "cemadenapi_spark-master_1".

8. Com o vscode do script extrator e do script spark abertos, faça os seguintes passos.

```bash
spark-submit example.py
```

10. Após a execução do spark, vá até o vscode e execute o projeto clicando no botão "Run and Debug", botão ao lado esquerdo com o sinal de "Play". Selecione a opção Python. E execute o projeto.




