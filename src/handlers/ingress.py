import json
import os
import boto3
import uuid

# Clientes AWS iniciados fora do handler (Performance)
sfn = boto3.client('stepfunctions')
sts = boto3.client('sts')


def get_state_machine_arn():
    """Descobre o endereço da State Machine dinamicamente"""
    # Pergunta para a AWS: "Qual é o meu Account ID?"
    account_id = sts.get_caller_identity()["Account"]
    region = os.environ.get('AWS_REGION', 'us-east-1')
    stage = os.environ.get('sls_stage', 'dev')

    # O nome deve bater com o que está no serverless.yml
    machine_name = f"ACD-Workflow-{stage}"

    return f"arn:aws:states:{region}:{account_id}:stateMachine:{machine_name}"


def handler(event, context):
    try:
        # Garante que o body é um dicionário, mesmo se vier como string
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event.get('body', {})

        task_id = str(uuid.uuid4())

        # Prepara os dados para o Step Functions
        input_payload = {
            "task_id": task_id,
            "payload": body,
            "metadata": {
                "source_ip": event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown'),
                "timestamp": event.get('requestContext', {}).get('requestTimeEpoch', 0)
            }
        }

        # Inicia o fluxo
        state_machine_arn = get_state_machine_arn()
        print(f"Iniciando execução na máquina: {state_machine_arn}")

        sfn.start_execution(
            stateMachineArn=state_machine_arn,
            name=task_id,
            input=json.dumps(input_payload)
        )

        return {
            "statusCode": 202,
            "body": json.dumps({
                "message": "Security Event Received",
                "task_id": task_id,
                "status": "processing"
            })
        }

    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")  # Isso vai aparecer no log se der erro de novo
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }