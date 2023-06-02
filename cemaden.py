import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import math

def CEMADENDataHora2datetime(string):
    padrao = r"[// ::]"
    dia,mes,ano,hora,minuto,segundo = re.split(padrao, string)
    dia,mes,ano,hora,minuto,segundo = int(dia),int(mes),int(ano),int(hora),int(minuto),int(segundo)
    return datetime(day=dia,month=mes,year=ano,hour=hora,minute=minuto,second=segundo)

def getRisco(alagamentoOuDeslizamento):
    '''0 para alagamento e 1 pra deslizamento ;  retorna JSON contendo chave
municipios, e cada municipio retorna uma lista com ultimo status e datetime do ultimmo status'''    
    J={}
    # Fazer uma requisição GET para a página
    if alagamentoOuDeslizamento :
        url = 'https://monitoramentocemadenrj.com.br/monitoramento/v2/municipio/?action=geo'
    else :
        url = 'https://monitoramentocemadenrj.com.br/monitoramento/v2/municipio/?action=hidro'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Criar um objeto BeautifulSoup com o conteúdo da página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar a tabela na página
        tabela = soup.find('table', id="dataTable")

        # Verificar se a tabela foi encontrada
        if tabela:
            # Iterar pelas linhas da tabela
            for linha in tabela.find_all('tr'):
                # Iterar pelas colunas da linha
                linhaz=[]
                for coluna in linha.find_all('td'):
                    # Extrair o conteúdo da coluna
                    conteudo = coluna.text.strip()
                    linhaz.append(conteudo)
                if len(linhaz)==6:
                    J[linhaz[0]] = [linhaz[2],CEMADENDataHora2datetime(linhaz[3])]
               # print(linhaz,len(linhaz))
                    # Imprimir o conteúdo ou fazer o que desejar com ele
                    #print(conteudo)
        else:
            print("Nenhuma tabela encontrada na página.")
    else:
        print("Falha ao fazer a requisição.")
    return J

def tem_string(a,b):
    #print(a,b)
    if type(a) == type(None):
        return False
    a=str(a)
    return a.lower().find(b)>=0

def converte_numeros(n):
    if n=='-':
        return math.nan
    return float(n)

def getRiscoRios():
    ''';  retorna JSON contendo chave
municipiosxcurso de água, e cada municipio retorna uma lista com ultimo status e datetime do ultimmo status'''    
    J={}
    # Fazer uma requisição GET para a página
    bacias = 'baia_de_guanabara,guandu,baixo_paraiba_do_sul_e_itabapoana,piabanha,medio_paraiba_do_sul,macae_e_das_ostras,baia_da_ilha_grande,lagos_sao_joao,rio_dois_rios'.split(',')
    for bacia in bacias :
        url = 'http://alertadecheias.inea.rj.gov.br/dados/'+bacia+'.php'

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Criar um objeto BeautifulSoup com o conteúdo da página
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar a tabela na página
            tabela = soup.find('table', id="Table")

            # Verificar se a tabela foi encontrada
            if tabela:
                # Iterar pelas linhas da tabela
                for linha in tabela.find_all('tr'):
                    # Iterar pelas colunas da linha
                    linhaz=[]
                    for coluna in linha.find_all('td'):
                        # Extrair o conteúdo da coluna
                        a=coluna.find_all('img')
                        if len(a)> 0 :
                            if not tem_string(a[0],'icone_dados'):
                                if tem_string(a[0],'estavel') :
                                    linhaz.append('[=]ESTAVEL')
                                elif tem_string(a[0],'subindo') :
                                    linhaz.append('[↑]SUBINDO')
                                elif tem_string(a[0],'descendo') :
                                    linhaz.append('[↓]DESCEDO')
                                elif tem_string(a[0],'pluviométrica'):
                                    linhaz.append('[?]ESTACAO PLUVIOMETRICA')
                        else:
                            conteudo = coluna.text.strip()
                            linhaz.append(conteudo)
                            
                    ###if len(linhaz)==6:
                    ###    J[linhaz[0]] = [linhaz[2],CEMADENDataHora2datetime(linhaz[3])]
                    if len(linhaz) == 16:
                        #print(linhaz)
                        local=linhaz[0]+'-'+linhaz[1]+'-'+linhaz[2]
                        status_rio=linhaz[3]
                        status=linhaz[5]
                        U=linhaz
                        mmChuva,mmUlt1h,mmUlt4h,mmUlt24h,mmUlt96h,mmUltMes=converte_numeros(U[6]),converte_numeros(U[7]),converte_numeros(U[8]),converte_numeros(U[9]),converte_numeros(U[10]),converte_numeros(U[11])
                        mRio,mRio15min,mRio30min,mRio45min=converte_numeros(U[12]),converte_numeros(U[13]),converte_numeros(U[14]),converte_numeros(U[15])
                        dhtOcorr=CEMADENDataHora2datetime(linhaz[4]+':00')
                        print(local,dhtOcorr,status_rio,status,mmChuva,mmUlt1h,mmUlt4h,mmUlt24h,mmUlt96h,mmUltMes,mRio,mRio15min,mRio30min,mRio45min)
                        # Imprimir o conteúdo ou fazer o que desejar com ele
                        #print(conteudo)
                        J[local]={'dht':dhtOcorr , 'status_rio':status_rio,'status':status,
                                  'mmChuva':mmChuva , 'mmUlt1h':mmUlt1h,'mmUlt4h':mmUlt4h,'mmUlt24h':mmUlt24h,'mmUlt96h':mmUlt96h,'mmUltMes':mmUltMes,
                                  'mRio':mRio,'mRio15min':mRio15min,'mRio30min':mRio30min,'mRio45min':mRio45min}
            else:
                print("Nenhuma tabela encontrada na página.")
        else:
            print("Falha ao fazer a requisição.")
    return J


#print(getRisco(0))
#print(getRisco(1))
print(getRiscoRios())
