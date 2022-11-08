import re
from pathlib import Path
from db.mysql import MysqlConnection, Imovel
import asyncio
import pandas as pd
from pandas import DataFrame
from loguru import logger

from dtos.iptu import InfoDebitoDto

path_planilha = Path("/home/vinicius/Downloads/planilha.xlsx")


def str_to_float(value):
    try:
        return float(value.replace(".", "").replace(",", "."))
    except:
        return value


def str_to_date(value):
    try:
        return re.sub(r"(\d{2})/(\d{2})/(\d{4}).*", r"\3-\2-\1", value)
    except:
        return value


def _abrir_planilha(path: Path) -> DataFrame:
    df_planilha = pd.read_excel(path, sheet_name="LINHAS DIGITÁVEIS - COTAS UNICA")
    df_filtrado = df_planilha[(df_planilha['DEVOLUTIVA'] == 'SUCESSO')]  # filtra apenas os debitos q obtiveram sucesso
    df_filtrado.filter(
        items=[" CIDADE", "UF", "INSCRIÇÃO", "CPF/CNPJ", "CONTRIBUINTE", "VALOR ORIGINAL", "VALOR COM DESCONTO",
               "VENCIMENTO", "CÓDIGO DE BARRAS"])  # coleta apenas os dados necessarios

    return df_filtrado


def _montar_debito(dados: tuple) -> InfoDebitoDto:
    return InfoDebitoDto(
        valor_inicial=dados[9],
        valor_final=dados[10],
        vencimento=str_to_date(str(dados[11])),
        linha_digitavel=re.sub("\D", "", dados[12]),
    )


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mysql = MysqlConnection()

    df = _abrir_planilha(path_planilha)
    file = open("erros2.txt", "w")
    for row in df.itertuples():
        try:
            imovel = loop.run_until_complete(mysql.buscar_imovel(row[6], row[2].strip(), row[3].strip()))

            spider = loop.run_until_complete(mysql.buscar_spider(imovel.id_cidade))
            debito = _montar_debito(row)
            loop.run_until_complete(mysql.update_proprietario(imovel, -1, row[8].strip(), row[7].strip()))
            loop.run_until_complete(mysql.update_debitos(imovel, spider, debito))
        except Exception:
            file.write(f"{row}\n")

    file.close()

