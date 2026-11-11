
import logging
import boto3
import csv
import io

from botocore.exceptions import ClientError

# Configurar logs
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logging.info("Iniciando pipeline ETL")

# Criar o cliente S3
s3 = boto3.client("s3", region_name="us-east-2")

# Configurar o bucket
bucket = "projeto-lakehouse-vendas-352333568808-us-east-2-an"

# Ler os dados brutos da Bronze
try:
    resposta = s3.get_object(
        Bucket=bucket,
        Key="bronze/vendas.csv"
    )

except ClientError as erro:
    logging.error("Erro ao acessar o arquivo no S3: %s", erro)
    raise

dados = resposta["Body"].read().decode("utf-8-sig")

logging.info("Arquivo Bronze lido com sucesso.")

# Transformar o texto CSV em registros
registros = list(csv.reader(io.StringIO(dados)))

# Verificar se o arquivo possui cabecalho
if not registros:
    raise ValueError("O arquivo CSV esta vazio.")

# Separar cabecalho e vendas
cabecalho = registros[0]
vendas = registros[1:]

# Verificar se existe a coluna id_venda
if "id_venda" not in cabecalho:
    raise ValueError(
        "A coluna id_venda nao foi encontrada no CSV."
    )

indice_id = cabecalho.index("id_venda")

# Validar duplicidades pelo id_venda
vendas_sem_duplicidade = []
vendas_por_id = {}

for numero_linha, venda in enumerate(vendas, start=2):

    # Verificar a quantidade de colunas
    if len(venda) != len(cabecalho):
        raise ValueError(
            f"Linha {numero_linha}: quantidade de colunas invalida."
        )

    id_venda = venda[indice_id].strip()

    # Verificar se o ID esta preenchido
    if not id_venda:
        raise ValueError(
            f"Linha {numero_linha}: id_venda vazio."
        )

    # Verificar se o ID e um numero inteiro valido
    try:
        id_venda_numero = int(id_venda)
    except ValueError:
        raise ValueError(
            f"Linha {numero_linha}: id_venda invalido: {id_venda}"
        )

    if id_venda_numero <= 0:
        raise ValueError(
            f"Linha {numero_linha}: id_venda deve ser positivo."
        )

    # Normalizar o ID para comparacao
    venda_normalizada = venda.copy()
    venda_normalizada[indice_id] = str(id_venda_numero)

    # Verificar se o ID ja apareceu
    if id_venda_numero in vendas_por_id:

        # Mesmo ID com informacoes diferentes
        if vendas_por_id[id_venda_numero] != venda_normalizada:
            raise ValueError(
                f"Conflito encontrado no id_venda {id_venda_numero}: "
                "registros com informacoes diferentes."
            )

        # Mesmo ID com informacoes iguais
        logging.warning(
            "Registro duplicado identico ignorado: %s",
            id_venda_numero
        )
        continue

    # Registrar a primeira ocorrencia do ID
    vendas_por_id[id_venda_numero] = venda_normalizada

    vendas_sem_duplicidade.append(venda_normalizada)

logging.info(
    "Vendas encontradas: %s",
    len(vendas)
)

logging.info(
    "Vendas apos remover duplicidades: %s",
    len(vendas_sem_duplicidade)
)

print("Vendas apos tratamento:")

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
try:
    s3.put_object(
        Bucket=bucket,
        Key="silver/vendas_tratadas.csv",
        Body=csv_tratado.encode("utf-8"),
        ContentType="text/csv"
    )

except ClientError as erro:
    logging.error(
        "Erro ao gravar o arquivo na Silver: %s",
        erro
    )
    raise

logging.info("Pipeline ETL concluido com sucesso!")
