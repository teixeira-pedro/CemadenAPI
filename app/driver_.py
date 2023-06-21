from local__ import *
from cemaden import *

J=getRiscoRios('CEMADEN_Estacoes_localiz.dat')
LocaisEmVoltaEstacoes={}
#print(J)
for estacao in J:
    dados_estacao=J[estacao]
    locais_em_volta=[]
    P=[dados_estacao['x'],dados_estacao['y']]
    Ps=get_perimetro(P,1000,250,45)
    #mapa=add_pontos_mapa(mapa,Ps)
    #add_circulo_mapa(mapa,P,1000)
    #a=mostra_mapa(mapa,'teste2.html')
    for P in Ps:
        locais_em_volta.append(get_lugar_coordenadas(P[0],P[1],geo()))
    print(estacao,locais_em_volta)
    LocaisEmVoltaEstacoes[estacao]=locais_em_volta
