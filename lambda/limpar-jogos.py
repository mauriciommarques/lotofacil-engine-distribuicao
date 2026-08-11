import boto3

REGION = "ap-east-1"
TABLE_NAME = "jogos_lotofacil"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(TABLE_NAME)


def LimparTabela():

    print("=" * 60)
    print("[LOTOFACIL] INICIANDO LIMPEZA DA TABELA")
    print("=" * 60)

    response = table.scan()

    itens = response.get(
        "Items",
        []
    )

    print(
        f"[LOTOFACIL] Itens encontrados: {len(itens)}"
    )

    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        itens.extend(
            response.get("Items", [])
        )

    if not itens:

        print(
            "[LOTOFACIL] Tabela já está vazia."
        )

        return

    with table.batch_writer() as batch:

        for item in itens:

            batch.delete_item(
                Key={
                    "pk": item["pk"],
                    "sk": item["sk"]
                }
            )

    print(
        f"[LOTOFACIL] Itens apagados: {len(itens)}"
    )

    print(
        "[LOTOFACIL] >>> TABELA LIMPA <<<"
    )


def lambda_handler(event, context):

    try:

        LimparTabela()

        return {
            "statusCode": 200,
            "body": "Tabela limpa com sucesso."
        }

    except Exception as erro:

        print(
            f"[LOTOFACIL] ERRO: {erro}"
        )

        return {
            "statusCode": 500,
            "body": str(erro)
        }


# EXECUÇÃO LOCAL
if __name__ == "__main__":
    LimparTabela()