
# Integração AWS S3 com PostgreSQL RDS usando Python

## Sobre o projeto

Projeto prático de Engenharia de Dados desenvolvido
para integrar dados armazenados no Amazon S3 a um
banco PostgreSQL hospedado no Amazon RDS.

A integração foi implementada com Python e boto3,
utilizando o psql para carregar os dados.

## Arquitetura

Amazon S3 (Silver)
       |
       v
Python + boto3
       |
       v
PostgreSQL (Amazon RDS)

## Tecnologias

- Python
- Amazon S3
- Amazon RDS
- PostgreSQL
- boto3
- SQL
- Git e GitHub

## Funcionamento

1. Leitura do arquivo CSV na camada Silver do S3.
2. Extração dos dados utilizando boto3.
3. Criação de uma tabela temporária no PostgreSQL.
4. Importação dos registros com COPY.
5. Associação das vendas aos clientes existentes.
6. Inserção ou atualização usando ON CONFLICT.
7. Confirmação da transação no banco de dados.

## Resultados

A integração foi executada com sucesso:

- 3 registros processados.
- Faturamento total: R$ 3.730,00.
- Sem duplicação de IDs de vendas.
- Relacionamento entre vendas e clientes preservado.

## Segurança

- Senha do PostgreSQL solicitada durante a execução.
- Configurações de conexão por variáveis de ambiente.
- Comunicação com o RDS por SSL.
- Acesso privado ao S3 por VPC Gateway Endpoint.
- Arquivos sensíveis excluídos do Git pelo .gitignore.

## Execução

Configurar as variáveis de ambiente:

- AWS_REGION
- S3_BUCKET
- S3_KEY (opcional)
- RDS_HOST
- RDS_DATABASE (opcional)
- RDS_USER (opcional)

Requisitos:

- Python 3
- boto3
- Cliente PostgreSQL psql
- Credenciais AWS com acesso ao objeto S3
- Conectividade de rede com o RDS

Executar:

python integracao_s3_rds.py

O programa solicita a senha do PostgreSQL.

## Observações

O script foi validado em um ambiente AWS CloudShell
com acesso privado ao S3 e ao PostgreSQL RDS.

Para executar em outro ambiente, é necessário
configurar as permissões AWS e o acesso de rede.

## Objetivo

Demonstrar conhecimentos práticos de integração
de dados, serviços AWS, Python, SQL e PostgreSQL.
