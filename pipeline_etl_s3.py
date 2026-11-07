import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logging.info("Iniciando pipeline ETL")

import boto3

# Criar o cliente S3
s3 = boto3.client("s3")

# Configurar o bucket
bucket = "projeto-lakehouse-vendas-352333568808-us-east-2-an"

# Ler os dados brutos da Bronze
from botocore.exceptions import ClientError

try:
    resposta = s3.get_object(
        Bucket=bucket,
        Key="bronze/vendas.csv"
    )
except ClientError as erro:
    print("Erro ao acessar o arquivo no S3:", erro)
    raise

dados = resposta["Body"].read().decode("utf-8")

print(dados)

import csv
import io

# Transformar o texto CSV em registros
registros = list(csv.reader(io.StringIO(dados)))

# Separar cabeçalho e vendas
cabecalho = registros[0]
vendas = registros[1:]

# Remover registros duplicados
vendas_sem_duplicidade = list(dict.fromkeys(tuple(venda) for venda in vendas))

print("Vendas após tratamento:")
for venda in vendas_sem_duplicidade:
    print(venda)

# Preparar o CSV tratado
saida = io.StringIO()
escritor = csv.writer(saida)

escritor.writerow(cabecalho)
escritor.writerows(vendas_sem_duplicidade)

csv_tratado = saida.getvalue()

print("CSV pronto para carregar:")
print(csv_tratado)

# Carregar os dados tratados na camada Silver
s3.put_object(
    Bucket=bucket,
    Key="silver/vendas_tratadas.csv",
    Body=csv_tratado.encode("utf-8"),
    ContentType="text/csv"
)

logging.info("Pipeline ETL concluído com sucesso!")