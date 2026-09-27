import boto3
import json
import time

REGION = "ap-east-1"
FUNCTION_NAME = "NOME_DA_SUA_LAMBDA_01"

lambda_client = boto3.client(
    "lambda",
    region_name=REGION
)

tentativa = 0

while True:
    tentativa += 1

    try:
        response = lambda_client.invoke(
            FunctionName="Lotofacil-Engine",
            InvocationType="RequestResponse",
            Payload=json.dumps({}).encode("utf-8")
        )

        payload = json.loads(
            response["Payload"].read().decode("utf-8")
        )

        status = payload.get("statusCode")

        print(f"Tentativa {tentativa} -> status {status}")

        if status == 200:
            print("\n==============================")
            print("FUNCIONANDO TUDO OK!")
            print("==============================")
            print(payload)
            break

        if status == 500:
            print("ERRO NA LAMBDA:")
            print(payload)
            break

    except Exception as erro:
        print(f"Erro ao chamar Lambda: {erro}")
        break

    time.sleep(2)