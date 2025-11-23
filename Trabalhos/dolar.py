import requests
from datetime import datetime, timedelta

def gerar_datas_mes(ano, mes):
    data = datetime(ano, mes, 1)
    datas = []

    while data.month == mes:
        datas.append(data.strftime("%m-%d-%Y"))
        data += timedelta(days=1)

    return datas

def cotacao(data):
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$top=1&$format=json"
    )
    res = requests.get(url)

    try:
        dados = res.json()
    except:
        return None

    if "value" in dados and len(dados["value"]) > 0:
        return dados["value"][0]["cotacaoVenda"]
    else:
        return None

datas_outubro = gerar_datas_mes(2011, 2)

for d in datas_outubro:
    valor = cotacao(d)
    if valor:
        print(d, "=>", valor)
    else:
        print(d, "=> sem cotação, pois não é um dia útil")