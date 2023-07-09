from local__ import *
from cemaden import *
import os
import pandas as pd
from db_connection import *

def processar_dados_iniciais():
    J=getRiscoRios('./cemadem_app/app/CEMADEN_Estacoes_localiz.dat')
    LocaisEmVoltaEstacoes={}
    lista_resultados = []
    #print(J)

    for estacao in J:
        print(f"============= {estacao} =============")
        dados_estacao=J[estacao]
        locais_em_volta=[]
        P=[dados_estacao['x'],dados_estacao['y']]
        Ps=get_perimetro(P,1000,250,45)
        for item_ps in Ps:
            locais_em_volta.append(get_lugar_coordenadas(item_ps[0],item_ps[1],geo()))
        print(estacao,locais_em_volta)
        dados = [{  "pk": f"{item.latitude}|{item.longitude}",
                    "fk": f"{P[0]}|{P[1]}",
                    "endereco": item.address,
                    "altitude": item.altitude,
                    "longitude": item.longitude,
                    "latitude": item.latitude
                } for item in locais_em_volta ]
        df = pd.DataFrame(dados).drop_duplicates(subset=["latitude", "longitude"])
        read_df = pd.read_sql(f'SELECT * FROM locais_em_volta where pk in {tuple(df["pk"])}', con=engine)
        result = pd.concat([df,read_df]).drop_duplicates(keep=False, subset=['pk'])
        
        if not result.empty:
            df.to_sql('locais_em_volta', con=engine, if_exists='append', index=False)
        produzir_mensagem(J[estacao])
    
    print('Fim execucao script.')


if __name__ == "__main__":
    processar_dados_iniciais()