import boto3

REGION = "ap-east-1"
TABLE_NAME = "jogos_lotofacil"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(TABLE_NAME)

def LimparTabela(confirmacao=False):

    if not confirmacao:

        print("=" * 60)
        print("[LOTOFACIL] LIMPEZA CANCELADA")
        print("=" * 60)
        print("[LOTOFACIL] Confirmação obrigatória para apagar os jogos.")

        return

    print("=" * 60)
    print("[LOTOFACIL] INICIANDO LIMPEZA DA TABELA")
    print("=" * 60)

    response = table.scan()

    itens = response.get(
        "Items",
        []
    )

    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        itens.extend(
            response.get("Items", [])
        )

    print(
        f"[LOTOFACIL] Itens encontrados: {len(itens)}"
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

    resposta = input(
        "ATENÇÃO: apagar TODOS os jogos. Digite SIM para confirmar: "
    )

    if resposta == "SIM":

        LimparTabela(
            confirmacao=True
        )

    else:

        print(
            "[LOTOFACIL] Operação cancelada."
        )

