import pycep_correios
#import consulta_correios IMPORTED AND CORRECTED TO HERE

import re
from geopy.geocoders import Nominatim
from geopy import distance



#from FogoCruzado import *
#from FogoCruzado import login_FC
#from conexao import *
#from JSON_SQL import *
import requests
from datetime import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
import unidecode
import re
#from Sonar import *
#from Tesseract_ import *
#from FogoCruzado import *
import re
#VOC_LOGR=get_vocabulario('\\_data\\logradouros.VOC')

#========================================IMPORTED AND CORRECTED OF CORREIOS_API==============================


def chunks(l, n):
    n = max(1, n)
    return list(l[i:i+n] for i in range(0, len(l), n))


def busca_cep(data_info):

    # Getting data
    data_info = normalize('NFKD', data_info).encode(
        'ASCII', 'ignore').decode('ASCII')
    session = requests.session()
    data = {'relaxation': data_info,
            'TipoCep': 'ALL',
            'semelhante': 'N',
            }

    r = session.post(
        "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm", data)

    content = r.content

    # Parsing
    soup = BeautifulSoup(content, features="html.parser")
    content = soup.find_all('table')

    if content:
        data = []
        items = content[0].find_all('td')
        for info in chunks(items, 4):
            data.append({
                'address': unidecode.unidecode(re.sub(' - .*', '', str(info[0].string)).strip()),
                'neighborhood': unidecode.unidecode(info[1].string.strip()),
                'city/state': unidecode.unidecode(info[2].string.strip()),
                'zipcode': unidecode.unidecode(info[3].string.strip()),
            })

    else:
        data = {'error': 'Address not found'}

    # Returning data
    return data

#============================================================================================================
def geo():
    return Nominatim(user_agent="smy-application")



def key_campo_indice_cosine(e):
    return e['nota']

def lugar_geo_2_JSON(n):
    lugar=get_lugar_nome(n,geo())
    #print(lugar)
    print(lugar.address)
    WW=lugar.address.split(',')

#    for i in lugar:
#        print('₢',i)
    addresses = busca_cep(n)
    print(addresses,'£')
    #print(busca_cep('one world trade center'),'8888')
#    print(addresses)
    outside_BR=False
    try:
        if addresses['error'] :
            outside_BR=True
    except:
        None

    if not lugar :
        return lugar
    lugar_fields=str(lugar).split(', ')
    print(lugar_fields)
    #daqui

    #['Universidade Federal Fluminense', 'Rua 15 de Novembro', 'Morro do Arroz',
    # 'Morro do Estado', 'Niterói', 'Região Geográfica Imediata do Rio de Janeiro',
    # 'Região Metropolitana do Rio de Janeiro', 'Região Geográfica Intermediária do Rio de Janeiro',
    # 'Rio de Janeiro', 'Região Sudeste', '24020125', 'Brasil']

    #quero apenas ('Universidade Federal Fluminense', 'Rua 15 de Novembro' , 'Morro do Estado', 'Niterói',
    # '24020125', 'Brasil')
    # VERIFICAR SE É BR, NO ULTIMO NOME, SE É PEGUEI **O PAIS**
    # DICA PROCURAR POR NOMES COMUNS DE LOGRADOURO SE COINCIDE, **É RUA**
    #       **SE TEM ANTES, É NOME DE LUGAR E A RUA TA NO PROXIMO**
    # PROCURAR SE UM DOS NOMES, É DE CIDADE (BASE FOGO CRUZADO) **É CIDADE** , e logo **TEMOS O ESTADO**
    # SE O ANTERIOR DA CIDADE NÃO É A RUA, ENTÃO, **TEMOS O BAIRRO**
    # COM NOME DO LUGAR, RUA, BAIRRO E CIDADE, PODE-SE ENCONTRAR **O CEP**



    #print(lugar_fields)
#    coincids=0
    possible_results=[]
#    campo=str(lugar)
#    print(addresses)
#    for address in addresses:
#            if contem_string(campo,address['neighborhood']) and contem_string(campo,address['city/state'].split('/')[0]):
#                possible_results.append({'nota':get_cosine(minusculo_sem_acento(address['address']),minusculo_sem_acento(campo.split(', ')[0])),'end':address})
            #print(address['neighborhood'],campo,address['city/state'].split('/')[0])
    #possible_results.sort(key=key_campo_indice_cosine,reverse=True)
    #print(possible_results)
    #cid_FC = get_data_FC(gera_consulta_local_FC(local['cidade'], login_FC()[0]))[0]
#    campeao=possible_results[0]['end']
    #print(campeao,campo)
    return


def get_lugar_nome(n,geo):
    lugar=geo.geocode(n)
    return lugar

def parser_address_geopy_brazil(l, rua_bairro_textual):
    l2 = rua_bairro_textual
    bairro2 = ''
    if not l2:
        None
    else:
        try:
            end, lugar, pais = l2.split(', ')
            cidade, estado = lugar.split(' - ')
            rua, bairro2 = end.split(' - ')
        except:
            bairro2 = ''
    l = l.address.split(', ')
    local = None
    for i in l:
        try:
            local = pycep_correios.get_address_from_cep(str(int(i)))
        except:
            None
    if not local:
        return None
    # print(gera_consulta_local_FC(local['cidade'], login_FC()[0]))
    cid_FC = get_data_FC(gera_consulta_local_FC(local['cidade'], login_FC()[0]))[0]
    #print(local, cid_FC, l)

    try:
        comuna = l[l.index(local['cidade']) + 1]
    except:
        comuna = ''
    estado = local['uf']
    bairro = local['bairro']
    cep = local['cep']
    rua = local['logradouro']
    nome = l[0]
    #print(bairro2)
    if not bairro2:
        try:
            bairro2 = l[l.index(local['cidade']) - 1]
        except:
            bairro2 = ''
            rua = nome
    cidade = cid_FC['Cidade']
    pais = l[len(l) - 1]
    nota = 0.0
    area_cidade = cid_FC['Area']
    cidade_id_FC = cid_FC['CidadeId']
    cidade_IBGE_id = cid_FC['CodigoIBGE']
    pop_cidade = cid_FC['Populacao']
    #print(nome, rua, bairro, bairro2, cidade, comuna, estado, pais, cep, area_cidade, cidade_id_FC, cidade_IBGE_id,
     #     pop_cidade, nota)
    ####CONSERTAR ERRO

    # {'bairro': 'Centro', 'cep': '24030-085', 'cidade': 'Niterói', 'logradouro': 'Rua Almirante Teffe', 'uf': 'RJ',
    # 'complemento': ''}
    # {'CidadeId': 3641, 'EstadoI
    #   d': 19, 'Cidade': 'Niterói', 'CodigoIBGE': 3303302, 'Gentilico': 'niteroiense', 'Populacao': 487562, 'Area
    # ': 13392, 'DensidadeDemografica': '3.64', 'PIBPreco
    # Corrente': None} ['Avenida Visconde do Rio Branco', 'Centro', 'Niterói', 'Região Geográfica Imediata do Rio de
    # Janeiro', 'Região Metropolitana do Rio de Jane
#  iro', 'Região Geográfica Intermediária do Rio de Janeiro', 'Rio de Janeiro', 'Região Sudeste', '24030085', 'Brasil
#   ']

#        Avenida Visconde do Rio Branco Rua Almirante Teffe Centro Centro Niterói Região Geográfica Imediata do Rio de
#     Janeiro RJ Brasil 24030 - 085 13392 3641 3303302
# https://viacep.com.br/
# https://pypi.org/project/Consulta-Correios/

#

def get_coordenadas_nome(n,geo):
    l=get_lugar_nome(n,geo)
    if not l:
        return None
    else:
        return (l.latitude,l.longitude)

def coordenadas_lugar(l):
    return (l.latitude,l.longitude)
#LATITUDE =X LONGITUDE = Y

def get_lugar_coordenadas(x,y,geo):
    lugar=geo.reverse(str(x)+', '+str(y))
    return lugar


def dist_lugar(a,b,geo):
    return distance.distance(get_coordenadas_nome(a,geo),get_coordenadas_nome(b,geo)).m

def dist_coordenadas(xa,ya,xb,yb,geo):
    return distance.distance((xa,ya),(xb,yb)).m

def dist_graus_x(d):
    #R=distance.EARTH_RADIUS
    return d/111.32

def dist_graus_y(d):
    #R=distance.EARTH_RADIUS
    return dist_graus_x(d)

def intervalo_ultimos_segundos(t):
    #t em segundos
    return datetime.now()-timedelta(seconds=t)


def get_perimetro(P,d):
    x = P[0]
    y = P[1]
    #dist em metros
    theta=dist_graus_y(d/1000)
    phi=dist_graus_x(d/1000)
    return [ [x+phi,x-phi] , [y+theta,y-theta] ]

def cemaden_coordenadas_2_GEOPY(s):
    '''Função que converte coordenadas em graus minutos e segundos em decimais,
    pois o CEMADEN Informa as coordenadas em Graus Minutos e Segundos (ex.:-21° 59' 47")
    porém, o geoPy só aceita em decimal, (ex.:-48.85614465)'''
    padrao = re.compile(r'-?\d+')
    numeros = padrao.findall(s)
    graus, minutos,segundos=int(numeros[0]),int(numeros[1]),int(numeros[2])
    #convertendo latitudes para decimal, pois o geoPy só aceita assim Latitude = 48.85614465, Longitude = 2.29782039332223
    return (graus/abs(graus)) * (abs(graus)+ (minutos/60) + (segundos/3600)) #a latitude em decimal




