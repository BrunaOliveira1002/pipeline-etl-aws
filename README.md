# Pipeline ETL com Python e AWS

## 📌 Sobre o projeto

Este projeto demonstra a implementação de um pipeline ETL (Extract, Transform, Load) utilizando Python e serviços da Amazon Web Services (AWS).

O objetivo é automatizar o processamento de dados de vendas, realizando a leitura de dados brutos, remoção de registros duplicados e armazenamento dos dados tratados.

## 🛠️ Tecnologias utilizadas

- **Python:** desenvolvimento do pipeline ETL.
- **Boto3:** integração do Python com os serviços AWS.
- **Amazon S3:** armazenamento dos dados nas camadas Bronze e Silver.
- **Amazon EC2:** execução do pipeline em ambiente Linux na nuvem.
- **AWS IAM:** gerenciamento de permissões de acesso aos recursos.

## 🏗️ Arquitetura do projeto

Amazon S3 (Bronze) → Amazon EC2 (Python + Boto3) → Amazon S3 (Silver)

## 🔄 Funcionamento do pipeline

1. Extração dos dados brutos armazenados no Amazon S3.
2. Leitura e processamento dos registros em Python.
3. Identificação e remoção de vendas duplicadas.
4. Geração de um novo arquivo CSV com os dados tratados.
5. Armazenamento do resultado na camada Silver do Amazon S3.

## 📊 Resultados

| Métrica | Resultado |
|---|---|
| Registros na Bronze | 4 |
| Registros na Silver | 3 |
| Duplicidades removidas | 1 |

O pipeline foi executado com sucesso em uma instância Amazon EC2, utilizando uma função IAM para acessar o Amazon S3 sem armazenar chaves de acesso no código.