
import boto3
import csv
import io
import getpass
import os
import subprocess
import tempfile

# Configuracoes do projeto
REGIAO = os.getenv("AWS_REGION", "us-east-2")
BUCKET = os.getenv("S3_BUCKET")
CHAVE = os.getenv("S3_KEY", "silver/vendas_tratadas.csv")

HOST = os.getenv("RDS_HOST")
BANCO = os.getenv("RDS_DATABASE", "lakehouse_vendas")
USUARIO = os.getenv("RDS_USER", "postgres")

if not BUCKET or not HOST:
    raise SystemExit(
        "Configure as variaveis S3_BUCKET e RDS_HOST."
    )

print("Lendo arquivo do Amazon S3...")

s3 = boto3.client("s3", region_name=REGIAO)
resposta = s3.get_object(Bucket=BUCKET, Key=CHAVE)
conteudo = resposta["Body"].read().decode("utf-8-sig")

vendas = list(csv.DictReader(io.StringIO(conteudo)))
print(f"Vendas encontradas: {len(vendas)}")

senha = getpass.getpass("Senha do PostgreSQL: ")

ambiente = os.environ.copy()
ambiente["PGPASSWORD"] = senha
ambiente["PGSSLMODE"] = "require"

with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".csv",
    encoding="utf-8",
    delete=False
) as arquivo:
    arquivo.write(conteudo)
    caminho = arquivo.name

try:
    sql = f"""
BEGIN;

CREATE TEMP TABLE vendas_importacao (
    id_venda INTEGER,
    cliente VARCHAR(100),
    produto VARCHAR(100),
    valor NUMERIC(10,2)
);

\\copy vendas_importacao FROM '{caminho}' WITH (FORMAT csv, HEADER true)

INSERT INTO vendas (
    id_venda, cliente, produto, valor, id_cliente
)
SELECT
    v.id_venda,
    v.cliente,
    v.produto,
    v.valor,
    c.id_cliente
FROM vendas_importacao v
JOIN clientes c ON c.nome = v.cliente
ON CONFLICT (id_venda)
DO UPDATE SET
    cliente = EXCLUDED.cliente,
    produto = EXCLUDED.produto,
    valor = EXCLUDED.valor,
    id_cliente = EXCLUDED.id_cliente;

COMMIT;
"""

    resultado = subprocess.run(
        [
            "psql", "-X",
            "-v", "ON_ERROR_STOP=1",
            "-h", HOST,
            "-p", "5432",
            "-U", USUARIO,
            "-d", BANCO,
            "-f", "-"
        ],
        input=sql,
        env=ambiente,
        capture_output=True,
        text=True
    )

    print(resultado.stdout)

    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr)

    print("Integracao S3 -> RDS concluida!")

finally:
    os.remove(caminho)
