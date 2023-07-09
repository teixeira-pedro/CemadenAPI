#import pycep_correios
#import consulta_correios IMPORTED AND CORRECTED TO HERE
#https://towardsdatascience.com/work-with-geospatial-data-and-create-interactive-maps-using-geopy-and-plotly-28178d2868f1
import re
from geopy.geocoders import Nominatim
from geopy.distance import distance
import math
import backoff
import folium


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

@backoff.on_exception(backoff.expo,
                      Exception,
                      max_time=300)
def get_lugar_coordenadas(x,y,geo):
    lugar=geo.reverse(str(x)+', '+str(y))
    return lugar


def dist_lugar(a,b,geo):
    return distance.distance(get_coordenadas_nome(a,geo),get_coordenadas_nome(b,geo)).m

def dist_coordenadas(xa,ya,xb,yb,geo):
    return distance.distance((xa,ya),(xb,yb)).m

def dist_graus_x(d):
    #R=distance.EARTH_RADIUS
    return d/111320

def dist_graus_y(d):
    #R=distance.EARTH_RADIUS
    return dist_graus_x(d)

def metros_para_graus_latitude_y(distancia_metros):
    return distancia_metros / 111320

def metros_para_graus_longitude_x(distancia_metros, latitude):
    return distancia_metros / (111320 * math.cos(math.radians(latitude)))

def intervalo_ultimos_segundos(t):
    #t em segundos
    return datetime.now()-timedelta(seconds=t)

def get_perimetro(P,d,granularidade,granularidade_angular):
    if granularidade <= 0 or granularidade>d or granularidade_angular <=0 or granularidade_angular >=360 :
        return None
    x = P[0]
    y = P[1]
    #dist em metros
    pontos = [ [x,y] ]#, [x,y+theta],[x,y-theta],[x+phi,y],[x-phi,y] ]
    if granularidade == d:
        return pontos
    partes=int(d/granularidade)
    setores=int(360/granularidade_angular)
    for i in range(setores):
        angulo=granularidade_angular*i
        for i in range(partes):
            d_=i*granularidade
            Pnew = get_point_at_distance(lat1=x, lon1=y, d=d_, bearing=angulo)  # DELTA(x,y,d,angulo)
            pontos.append(Pnew)
    return pontos


def get_perimetro_old(P,d,granularidade):
    if granularidade <= 0 or granularidade>d :
        return none
    x = P[0]
    y = P[1]
    #dist em metros
    theta=metros_para_graus_latitude_y(d)
    phi=metros_para_graus_longitude_x(d,y)
    pontos = [ [x,y] , [x,y+theta],[x,y-theta],[x+phi,y],[x-phi,y] ]
    if granularidade == d:
        return pontos
    partes=int(d/granularidade)
    incr_theta=theta/partes
    incr_phi=phi/partes
    for i in range(partes):
        pontos.append([x,y+(i*incr_theta)])
        pontos.append([x,y-(i*incr_theta)])
        pontos.append([x+(i*incr_phi),y])
        pontos.append([x-(i*incr_phi),y])
    return pontos






def cemaden_coordenadas_2_GEOPY(s):
    '''Função que converte coordenadas em graus minutos e segundos em decimais,
    pois o CEMADEN Informa as coordenadas em Graus Minutos e Segundos (ex.:-21° 59' 47")
    porém, o geoPy só aceita em decimal, (ex.:-48.85614465)'''
    padrao = re.compile(r'-?\d+')
    numeros = padrao.findall(s)
    graus, minutos,segundos=int(numeros[0]),int(numeros[1]),int(numeros[2])
    #convertendo latitudes para decimal, pois o geoPy só aceita assim Latitude = 48.85614465, Longitude = 2.29782039332223
    return (graus/abs(graus)) * (abs(graus)+ (minutos/60) + (segundos/3600)) #a latitude em decimal

def mapeia(centralizado_em,zoom):
    mapa=None
    if (not zoom) or zoom <= 0 :
        mapa =folium.Map(location=centralizado_em)
    else:
        mapa =folium.Map(location=centralizado_em,zoom_start=zoom)
    return mapa

def add_circulo_mapa(mapa,P,d):
    x=P[0]
    y=P[1]
    mapa.add_child(folium.Circle(
        location=(x, y),
        radius=d,
        popup=" ",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ))
    #return mapa

def add_pontos_mapa(mapa,Ps):
    cor = 'green'
    for i in range(len(Ps)):
        P=Ps[i]
        if i==0:
            mapa.add_child(folium.Marker(location=P, icon=folium.Icon(color='green')))
        else:
            mapa.add_child(folium.Marker(location=P, icon=folium.Icon(color='red')))
    return mapa


def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    d=d/1000
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}m from initial, in degrees
    """
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    a = math.radians(bearing)
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(a))
    lon2 = lon1 + math.atan2(
        math.sin(a) * math.sin(d/R) * math.cos(lat1),
        math.cos(d/R) - math.sin(lat1) * math.sin(lat2)
    )
    return [math.degrees(lat2), math.degrees(lon2)]

def mostra_mapa(mapa,nome_mapa_salvar):
    mapa.save(nome_mapa_salvar)
    return nome_mapa_salvar



# P2=get_lugar_nome('carrefour manilha',geo())
# P2=[P2.latitude,P2.longitude]
# #print()
# #P=[0,0]
# P=P2
# #P=[1,1]
# #P=[40.7128, -74.0060]
# #print(get_perimetro_novo(P, 1000, 100,45))
# #print('mapeia([],0)=',mapeia([],0),'|','mapeia([40.7128, -74.0060],0)=',mapeia([40.7128, -74.0060],0),'|')
# mapa=mapeia(P,0)
# #Ps=get_perimetro_novo([40.7128, -74.0060], 1000, 250,90)
# Ps=get_perimetro(P,1000,250,10)
# mapa=add_pontos_mapa(mapa,Ps)
# add_circulo_mapa(mapa,P,1000)
# a=mostra_mapa(mapa,'teste2.html')
# for P in Ps:
#    print(get_lugar_coordenadas(P[0],P[1],geo()))


