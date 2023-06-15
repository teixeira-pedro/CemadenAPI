import re
import json
import Levenshtein
from unidecode import unidecode

ADDD={"Cachoeiras de Macacu*rio Macacu*Japuíba" : [],
"Marica*rio Mumbuca*Mumbuca" : [],
"Duque de Caxias*rio Saracuruna*Santa Cruz da Serra" : [],
"Magé*rio Inhomirim*Ponte de Ferro Piabeta" : [],
"Duque de Caxias*rio Capivari*Ponte de Ferro Capivari" : [],
"Nova Iguaçu*rio da Bota*GBM Nova Iguaçu" : [],
"São João de Meriti*rio Pavuna*CET Meriti" : [],
"Niterói*rio Engenhoca*Niterói / Engenhoca" : [],
"São Gonçalo*rio da Aldeia*Ipiíba" : [],
"Rio de Janeiro*rio Maracanã*São Cristóvão" : [],
"Niterói*-*Niterói / BPRV" : [],
"Cachoeiras de Macacu*rio Macacu*Cachoeiras de Macacu" : [],
"Guapimirim*-*Escola União" : [],
"Magé*-*Andorinhas" : [],
"Guapimirim*rio Iconha*Orindí" : [],
"Guapimirim*Guapimirim*Guapimirim" : [],
"Rio de Janeiro*-*Realengo" : [],
"Magé*rio Surui*Estrada da Conceição" : [],
"Magé*-*Raiz da Serra" : [],
"Duque de Caxias*-*Xerém - Mantiquira" : [],
"Tanguá*rio Tanguá*BR101" : [],
"Tanguá*rio Caceribu*Tanguá" : [],
"Tanguá*rio Caceribu*Ponte Tanguá" : [],
"Tanguá*rio Duques*Duques" : [],
"Tanguá*-*Haras MZC" : [],
"Tanguá*rio Iguá*Haras Vitória" : [],
"São Gonçalo*-*Largo da Ideia" : [],
"Rio de Janeiro*-*Eletrobrás" : [],
"Rio de Janeiro*-*Campo Grande" : [],
"Marica*-*Barra de Marica" : [],
"Cachoeiras de Macacu*rio Tatu*Tatu" : [],
"Cachoeiras de Macacu*Soarinho*Soarinho" : [],
"Itaboraí*rio Canal de Imunana*Barragem da CEDAE" : [],
"Cachoeiras de Macacu*rio Guapiaçu*Duas Barras" : [],
"Paracambi*rio dos Macacos*Paracambi" : [],
"Queimados*rio Guandu*Guandu Dutra" : [],
"Seropédica*rio Guandu*Guandu Seropédica" : [],
"Santo Antônio de Pádua*rio Pomba*Santo Antônio de Pádua" : [],
"Itaperuna*rio Muriaé*Itaperuna" : [],
"Italva*rio Muriaé*Italva" : [],
"Bom Jesus do Itabapoana*rio Itabapoana*Bom Jesus do Itabapoana" : [],
"Laje do Muriaé*rio Muriaé*Laje do Muriaé" : [],
"Santo Antônio de Pádua*rio Pomba*Ponte Paraoquena" : [],
"São Fidelis*rio Paraíba do Sul*São Fidelis" : [],
"Teresópolis*rio Paquequer*Comari" : [],
"Teresópolis*rio Meudon*Unifeso" : [],
"Teresópolis*rio Príncipe*Posse - São Sebastião" : [],
"Teresópolis*rio Quebra Frascos*Quebra Frascos" : [],
"Petrópolis*rio Quitandinha*Centro" : [],
"Petrópolis*rio Palatinado*Alto da Serra" : [],
"Petrópolis*rio Piabanha*Bingen" : [],
"Petrópolis*rio Quitandinha*Cel Veiga" : [],
"Petrópolis*rio Santo Antônio*Itaipava" : [],
"Petrópolis*rio Cuiabá*Cuiabá" : [],
"Petrópolis*rio Piabanha*Corrêas Igreja" : [],
"Petrópolis*rio Piabanha*Nogueira" : [],
"Petrópolis*-*Itamarati" : [],
"Petrópolis*-*Independência" : [],
"Petrópolis*-*Araras" : [],
"Petrópolis*-*Barão do Rio Branco" : [],
"Petrópolis*-*Posse" : [],
"Petrópolis*-*Bonfim" : [],
"Petrópolis*-*Samambaia" : [],
"Petrópolis*-*LNCC" : [],
"Petrópolis*-*Capim Roxo" : [],
"Petrópolis*-*Quitandinha" : [],
"Petrópolis*-*Morin" : [],
"Teresópolis*rio Paquequer*Paquequer" : [],
"Rio das Flores*rio Ribeirão Manoel Pereira*Rio das Flores" : [],
"Resende*rio Preto*Visconde de Mauá" : [],
"Barra Mansa*rio Bananal*Rialto" : [],
"Barra Mansa*rio Barra Mansa*Fazenda Escola UBM" : [],
"Paraíba do Sul*rio Paraíba do Sul*Paraíba do Sul" : [],
"Belmiro Braga*rio Paraibuna*Sobraji" : [],
"Macaé*rio São Pedro*Glicério" : [],
"Macaé*rio São Pedro*São Pedro" : [],
"Rio das Ostras*rio Jundiá*Jundiá" : [],
"Nova Friburgo*rio Macaé*Macaé de Cima" : [],
"Nova Friburgo*rio Bonito*Piller" : [],
"Paraty*rio Pereque Açu*Parati" : [],
"natividade*rio carangola*natividade" : [],
"Silva Jardim*rio Capivari*Portal Silva Jardim" : [],
"Silva Jardim*rio Bacaxá*Sítio Beira Rio" : [],
"Nova Friburgo*rio Bengala*Suspiro" : [],
"Nova Friburgo*rio Santo Antônio*Ypu" : [],
"Nova Friburgo*rio Cônego*Olaria" : [],
"Bom Jardim*ribeirão São José*São José do Ribeirão" : [],
"Nova Friburgo*rio Córrego Dantas*Venda das Pedras" : [],
"Nova Friburgo*rio Bengala*Conselheiro Paulino" : [],
"Bom Jardim*rio Grande*Banquete" : [],
"Nova Friburgo*rio Grande*Ponte Estrada Dona Mariana" : [],
"Cantagalo*-*Cantagalo" : [],
"Nova Friburgo*-*Pico Caledônia" : [],
"São Sebastião do Alto*rio Grande*Manuel de Morais" : [],
}
#FONTE = 'http://www.inea.rj.gov.br/cs/groups/public/documents/document/zwff/mdi3/~edisp/inea_027687.pdf'
LOCS={"Nova Friburgo*Rio Macaé*Macaé de Cima":['''-22° 22' 20""''','''-42° 27' 44""'''],
"Nova Friburgo*Rio Bonito*Piller":['''-22° 24' 32"''','''-42° 20' 09"'''],
"Macaé*Rio Macaé*Ponte do Baião":['''-22° 23' 17"''','''-42° 04' 56"'''],
"Macaé*-*Praia Campista":[''' -22° 23' 30""''',''' -41° 46' 56""'''],
"Macaé*Rio São Pedro*São Pedro":['''-22° 16' 34""''','''-41° 52' 31""'''],
"Macaé*Rio Macaé*São Romão":['''-22° 21' 34"''','''-42° 13' 38"'''],
"Macaé*Rio Macaé*Severina":['''-22° 17' 43"''','''-41° 52' 40"'''],
"Bom Jesus do Itabapoana*Rio Itabapoana*Bom Jesus do Itabapoana":['''-21° 07' 59""''',''''-41° 40' 44""'''],
"Campos dos Goytacazes*Rio Paraíba do Sul*Campos dos Goytacazes":['''-21° 44' 07""''','''-41° 20' 55""'''],
"Cardoso Moreira*Rio Muriaé*Cardoso Moreira":['''-21° 29' 22""''','''-41° 37' 58""'''],
"Italva*Rio Muriaé*Italva":['''-21° 24' 30"''','''-41° 41' 30"'''],
"Itaperuna*Rio Muriaé*Itaperuna":[''' -21° 12' 36""''',''' -41° 54' 49""'''],
"Laje do Muriaé*Rio Muriaé*Laje do Muriaé":['''-21° 12' 15""''','''-42° 07' 28""'''],
"Natividade*Rio Carangola*Natividade":['''-21° 01' 58""''','''-41° 59' 40""'''],
"Sto. Antônio de Pádua*Rio Pomba*Ponte Paraoquena":['''-21° 30' 20""''','''-42° 15' 25""'''],
"Porciúncula*Rio Carangola*Porciúncula":['''-20° 57' 42""''','''-42° 02' 17""'''],
"Sto. Antônio de Pádua*Rio Pomba*Sto. Antônio de Pádua":['''-21° 29' 22""''','''-41° 37' 58""'''],
"Bom Jardim*Rio Grande*Banquete":['''-22° 10' 39"''','''-42° 28' 23"'''],
"Bom Jardim*Rio Grande*São José do Ribeirão":['''-22° 12' 26""''','''-42° 24' 00""'''],
"Cantagalo*-*Cantagalo":['''-21° 59' 47"''','''-42° 21' 51"'''],
"Petrópolis*Rio Palatinado*Alto da Serra":['''-22° 30' 45""''','''-43° 10' 20""'''],
"Petrópolis*-*Araras":['''-22° 26' 02"''','''-43° 15' 19"'''],
"Petrópolis*-*Barão do Rio Branco":['''-22° 29' 25""''','''-43° 11' 07""'''],
"Petrópolis*Rio Piabanha*Bingen":['''-22° 30' 44""''','''-43° 10' 47""'''],
"Petrópolis*-*Bonfim":['''-22° 27' 41"''','''-43° 05' 42"'''],
"Petrópolis*-*Capim Roxo":['''-22° 21' 02"''','''-43° 11' 27"'''],
"Petrópolis*Rio Quitandinha*Centro":['''-22° 30' 34""''','''-43° 11' 46""'''],
"Petrópolis*Rio Piabanha*Corrêas":['''-22° 26' 42""''','''-43° 08' 33""'''],
"Petrópolis*-*Cuiabá":['''-22° 22' 46"''','''-43° 04' 05"'''],
"Petrópolis*-*Independência":['''-22° 32' 52"''','''-43° 12' 32"'''],
"Petrópolis*Rio Santo Antônio*Itaipava":['''-22° 24' 20""''','''-43° 06' 10""'''],
"Petrópolis*-*Itamarati":['''-22° 29' 06"''','''-43° 09' 00"'''],
"Petrópolis*-*LNCC":['''-22° 31' 49"''','''-43° 13' 02"'''],
"Petrópolis*-*Morin":['''-22° 29' 25"''','''-43° 11' 07"'''],
"Petrópolis*-*Pedro do Rio":['''-22° 20' 07"''','''-43° 07' 59"'''],
"Petrópolis*-*Posse":['''-22° 15' 29"''','''-43° 04' 35"'''],
"Petrópolis*-*Quitandinha":['''-22° 31' 11"''','''-43° 12 '46"'''],
"Petrópolis*-*Samambaia":['''-22° 27' 28"''','''-43° 08' 24"'''],
"Teresópolis*Rio Imbuí*Caleme":['''-22° 24' 06"''','''-43° 00' 45"'''],
"Teresópolis*Rio Paquequer*Comari":['''-22° 26' 45""''','''-42° 58' 33""'''],
"Teresópolis*Rio Príncipe*Posse":['''-22° 22' 18"''','''-43° 00' 14"'''],
"Teresópolis*Rio Quebra Frascos*Quebra Frascos":['''-22° 25' 01""''','''-43° 00' 27""'''],
"Teresópolis*Rio Fisher*Quinta do Lebrão":['''-22° 24' 03""''','''-42° 57' 11""'''],
"Teresópolis*Rio Meudon*Unifeso":['''-22° 25' 09"''','''-42° 58' 01"'''],
"Macaé*Rio Macaé*Barra do Sana":['''-22° 22' 18"''','''-42° 12' 21"'''],
"Macaé*Rio Macaé*Fazenda Airis":['''-22° 19' 47"''','''-41° 59' 04"'''],
"Macaé*-*Frade":['''-22° 22' 18"''','''-41° 47' 08"'''],
"Macaé*Rio Macaé*Galdinópolis":['''-22° 22' 08"''','''-42° 22' 46"'''],
"Macaé*Rio São Pedro*Glicério":['''-22° 13' 50""''','''-42° 03' 03""'''],
"Angra*-*Angra":['''-23° 00' 04"''','''-44° 18' 56"'''],
"Paraty*Rio Mambucaba*Fazenda Fortaleza":['''-22° 57' 23"''','''-44° 33' 39"'''],
"Barra Mansa*Rio Barra Mansa*Fazenda Escola UBM":['''-22° 35' 50"''','''-44° 10' 09"'''],
"Paracambi*Rio dos Macacos*Paracambi":['''-22° 36' 36""''','''-43° 42' 39""'''],
"Barra Mansa*Rio Bananal*Rialto":[''' -22° 35' 08""''','''-44° 16' 08""'''],
"Resende*Rio Preto*Visconde de Mauá":['''-22° 19’ 47”''','''-44° 32’ 20”'''],
"São João de Meriti*Rio Pavuna*CET Meriti":['''-22° 48' 23"''','''-43° 22' 16"'''],
"Mesquita*Rio Sarapuí*Clube XV":['''-22° 48' 31"''','''-43° 26' 12"'''],
"Nova Iguaçu*Rio Iguaçu*Catavento":['''-22°39' 00"''','''-43° 25' 06"'''],
"Nova Iguaçu*Rio da Bota*GBM Nova Iguaçu":['''-22° 44' 55""''','''-43° 27' 25""'''],
"Rio de Janeiro*Rio Acari*Guadalupe":['''-22° 50' 55""''','''-43° 22' 13""'''],
"Duque de Caxias*Rio Capivari*Ponte de Ferro Capivari":['''-22° 40' 04""''','''-43° 20' 16""'''],
"Magé*Rio Inhomirim*Ponte de Ferro Piabetá":['''-22° 37' 27""''','''-43° 09' 17""'''],
"Magé*-*Raiz da Serra":['''-22° 34' 48"''','''-43° 11' 17"'''],
"Duque de Caxias*Rio Saracuruna*Santa Cruz da Serra":['''-22° 38' 29""''','''-43° 17' 14""'''],
"Duque de Caxias*-*Xerém - Mantiquira":['''-22° 32' 58""''','''-43° 18' 04""'''],
"Niterói*-*Niterói/BPRV":['''-22° 52' 45"''','''-43° 04' 39"'''],
"Niterói*Rio Engenhoca*Niterói / Engenhoca":['''-22° 52' 15""''','''-43° 05' 57""'''],
"São Gonçalo*Rio Colubandê*Colubandê":['''-22° 52' 07""''','''-42° 58' 58""'''],
"Nova Friburgo*Rio Bengala*Conselheiro Paulino":['''-22° 13' 42""''','''-42° 31' 12""'''],
"Nova Friburgo*Rio Cônego*Olaria":['''-22° 18' 31""''','''-42° 32' 31""'''],
"Nova Friburgo*-*Pico Caledônia":['''-22° 21' 33""''','''-42° 34' 02""'''],
"Nova Friburgo*Rio Grande*Ponte Estrada Dona Mariana":['''-22° 12' 57""''','''-42° 34' 14""'''],
"Nova Friburgo*Rio Bengala*Suspiro":['''-22° 16' 46""''','''-42° 32' 05""'''],
"Nova Friburgo*Córrego d´Antas*Venda das Pedras":['''-22° 16' 42""''','''-42° 34' 53""'''],
"Nova Friburgo*Rio Santo Antônio*Ypu":['''-22° 17' 45""''','''-42° 31' 35""'''],
"Tanguá*-*Haras MZC":['''-22° 45' 25''''','''-42° 43' 06"'''],
"Tanguá*Rio Tanguá*Haras Vitória":['''-22° 47' 27''','''-42° 49' 57'''''],
"São Gonçalo*Rio Aldeia*Ipiíba":['''-22° 52' 17"''','''-42° 58' 31'''''],
"São Gonçalo*-*Lagoa da Areia":['''-22° 49' 20"''','''-42° 54' 51'''''],
"São Gonçalo*-*Serra do Lagarto":['''-22° 50' 37"''','''-42° 45' 57'''''],
"Rio Bonito*Rio Caceribu*Tanguá":['''-22° 42' 30"''','''-42° 42' 14'''''],
"Itaboraí*Rio Caceribu*Reta Nova":['''-22° 42' 45"''','''-42° 48' 24"'''],
"Maricá*Lagoa de Maricá*Barra de Maricá":['''-22° 57' 19"''','''-42° 48' 32"'''],
"Rio de Janeiro*Rio Tindiba*Av. dos Industriários":['''-22o 55' 48""''','''-43° 21' 51""'''],
"Rio de Janeiro*Rio Faria*Estrada Velha da Pavuna":['''-22° 52' 20""''','''-43° 16' 03""'''],
"Rio de Janeiro*Lagoa de Jacarepaguá*Via 11":['''-23° 00' 00""''','''-43° 21' 59""'''],
"Rio de Janeiro*Rio Guandu*Campo Grande":['''-22° 53' 03"''','''-43° 32' 39"'''],
"Rio de Janeiro*Rio Guandu*Mendanha":['''-22° 51' 45"''','''-43° 32' 36"'''],
"Queimados*Rio Guandu*Via Dutra":['''-22° 43' 52"''','''-43° 38' 30"'''],
"São Pedro da Aldeia*Lagoa de Araruama*Ponte RJ101":['''-22° 51' 52""''','''-42° 02' 58""'''],
"São Pedro da Aldeira*Lagoa de Araruama*Salina Boa Vista":['''-22° 50' 58""''','''-42° 11' 04""'''],
"Silva Jardim*Rio Capivari*Portal Silva Jardim":['''-22° 38' 32""''','''-42° 24' 04""'''],
"Silva Jardim*Rio Bacaxá*Sitio Beira Rio":['''-22° 42' 45''''','''-42° 21' 37'''''],
"Silva Jardim*-*Juturnaíba":['''-22° 35' 10''''','''-42° 16' 04"'''],
"Saquarema*Rio Mole *Rio Mole":['''-22° 51' 11"''','''-42° 33' 07"'''],
"Rio das Flores*Rib Manuel Pereira*Rio das Flores":['''-22° 10' 06""''','''-43° 35' 13""'''],
"Miguel Pereira*Rio do Saco*Miguel Pereira":['''-22° 26' 40"''','''-43° 26' 48"'''],
"Teresópolis*Rio Piabanha*Paquequer":['''-22° 25' 48"''','''-42º 58' 34"'''],
"Cachoeiras de Macacu*Rio Macacu*Duas Barras":['''-22° 27' 27"''','''-42° 46' 37"'''],
"Cachoeiras de Macacu*Rio Macacu*Japuíba":['''-22° 33' 41""''','''-42° 41' 37""'''],
"Cachoeiras de Macacu*Rio GuapiAçu *Quizanga I":['''-22° 33' 50""''','''-42° 50' 52""'''],
"Cachoeiras de Macacu*Rio Macacu*Cachoeiras de Macacu":['''-22°28' 45""''','''-42° 39' 28""'''],
"GuapiMirim*Rio GuapiMirim*Escola União":['''-22° 35' 09"''','''-42° 56' 41"'''],
"GuapiMirim*Rio Iconha*Orindi":['''-22° 32' 54"''','''-42° 53' 50"'''],
"Itaboraí*Canal do Imunana*Barragem da Cedae":['''-22° 39' 25""''','''-42° 55' 54""'''],
"Magé*-*Andorinhas":['''-22o 32' 35"''','''-43° 02' 33"'''],
"Magé*Rio Suruí*Estrada da Conceição":['''-22° 36' 35""''','''-43° 06' 08""'''],
"Magé*Rio Roncador*Parque São Miguel":['''-22° 38' 50""''','''-43° 02' 18""'''],
"Rio de Janeiro*Rio Cachoeira *Capela Mayrink":['''-22° 57' 28"''','''-43° 16' 40"'''],
"Rio de Janeiro*Rio Grande*Eletrobrás":['''-22° 55' 18"''','''-43° 25' 12"'''],
"Rio de Janeiro*Rio Maracanã*Quartel PE":['''-22° 55' 17"''','''-43° 14' 08"'''],
"Rio de Janeiro*Baía de Guanabara*Realengo":['''-22° 51' 57""''','''-43° 25' 23""'''],
"Saquarema*Lagoa de Saquarema*Rua Getúlio Vargas":['''-22° 55' 18""''','''-42° 30' 48""'''],
"Tanguá*Rio Caceribu*Ponte de Tanguá":['''-22° 43' 38"''','''-42° 43' 35"'''],
"Rio de Janeiro*Rio Maracanã*São Cristovão":['''-22° 54' 38''''','''-43°13' 27"'''],
"Niterói*-*Ampla Rio d'Ouro":['''-22° 53' 31''''','''-42° 59' 14'''''],
"Tanguá*Rio Tanguá*BR101":['''-22° 43' 49''''','''-42° 41' 55'''''],
"Tanguá*Rio dos Duques*Duques":['''-22° 44' 27''''','''-42° 47' 11"'''],
"Cachoeiras de Macacu*-*Guapiaçu Cascataí":['''-22° 24' 53''''','''-42° 43' 41''''']
}
def cemaden_coordenadas_2_GEOPY(s):
    '''Função que converte coordenadas em graus minutos e segundos em decimais,
    pois o CEMADEN Informa as coordenadas em Graus Minutos e Segundos (ex.:-21° 59' 47")
    porém, o geoPy só aceita em decimal, (ex.:-48.85614465)'''
    padrao = re.compile(r'-?\d+')
    numeros = padrao.findall(s)
    graus, minutos,segundos=int(numeros[0]),int(numeros[1]),int(numeros[2])
    #convertendo latitudes para decimal, pois o geoPy só aceita assim Latitude = 48.85614465, Longitude = 2.29782039332223
    return (graus/abs(graus)) * (abs(graus)+ (minutos/60) + (segundos/3600)) #a latitude em decimal

def compara_similaridade_nomes_locais(aAdicionar,baseComLocais):
    BCL = list(baseComLocais)
    aAdicionarNew={}
    for chave_cand in list(aAdicionar):
        chave_cand = chave_cand.lower()
        #try:
        chC_a,chC_b,chC_c = chave_cand.split('*')
            #print(chC_a,chC_b,chC_c)
        #except:
            #print(chave_cand.split('*'),'**********')
        valores=[]
        for chave_loc in BCL :
            chave_loc=chave_loc.lower()
    #        try:
            chL_a,chL_b,chL_c = chave_loc.split('*')
            RATIO = ((5*Levenshtein.ratio(chC_a,chL_a))+(2.5*Levenshtein.ratio(chC_b,chL_b))+(2.5*Levenshtein.ratio(chC_c,chL_c)))/10
            valores.append(RATIO)
        maior_valor = max(valores)
        indice_maior_valor = valores.index(maior_valor)
        if maior_valor > .73 :
            coord = baseComLocais[BCL[indice_maior_valor]]
            aAdicionarNew[unidecode(chave_cand)] = [cemaden_coordenadas_2_GEOPY(coord[0]),cemaden_coordenadas_2_GEOPY(coord[1])]
            #print(chave_cand,' $ ',maior_valor,' $ ',BCL[indice_maior_valor],'>',
            #[cemaden_coordenadas_2_GEOPY(coord[0]),cemaden_coordenadas_2_GEOPY(coord[1])])
        else :
            #print(chave_cand,' $ ',maior_valor,' $ ',BCL[indice_maior_valor],'$','[REVER]')
            if chave_cand == 'belmiro braga*rio paraibuna*sobraji' :
                aAdicionarNew[unidecode(chave_cand)] = [-21.9667, -43.3744]
            elif chave_cand == 'são fidelis*rio paraíba do sul*são fidelis' :
                aAdicionarNew[unidecode(chave_cand)] =[-21.6442,-41.8589]
            elif chave_cand == 'seropédica*rio guandu*guandu seropédica' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.611944,-42.673889]
            elif chave_cand == 'paraíba do sul*rio paraíba do sul*paraíba do sul' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.1628,-43.2864]
            elif chave_cand == 'rio das ostras*rio jundiá*jundiá' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.4719,-41.9203]
            elif chave_cand == 'são sebastião do alto*rio grande*manuel de morais' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.241,-42.1344]
            elif chave_cand == 'marica*rio mumbuca*mumbuca' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.906667,-42.814583]
            elif chave_cand == 'cachoeiras de macacu*soarinho*soarinho' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.611944,-42.673889]
            elif chave_cand == 'paraty*rio pereque açu*parati' :
                aAdicionarNew[unidecode(chave_cand)] = [-23.22,-44.727]
            elif chave_cand == 'marica*-*barra de marica' :
                aAdicionarNew[unidecode(chave_cand)] = [-22.955694,-42.809389]
    return aAdicionarNew

                



ADDD2 = compara_similaridade_nomes_locais(ADDD,LOCS)
for key in ADDD2:
    print(key,ADDD2[key])
with open('CEMADEN_Estacoes_localiz.dat', "w") as arquivo:
    json.dump(ADDD2, arquivo)
print(len(ADDD2),len(ADDD))
