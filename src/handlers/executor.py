import json


def handler(event, context):
    """
    Defense Executor (Dry-Run Mode)
    Recebe a análise da IA e decide se bloqueia ou não.
    """
    print(f"Recebendo ordem de execução: {json.dumps(event)}")

    # Extrai os dados das etapas anteriores
    # O Step Functions passa o output da Lambda anterior como input desta
    payload = event.get('payload', {})
    analysis = event.get('analysis', {})

    source_ip = payload.get('source_ip', 'unknown')
    is_malicious = analysis.get('malicious', False)
    confidence = analysis.get('confidence', 0.0)

    # Lógica de Decisão
    response_action = {}

    if is_malicious and confidence > 0.7:
        # AQUI ENTRARIA O CÓDIGO REAL DE BLOQUEIO (WAF/Firewall)
        # Para o MVP, fazemos apenas o Log (Dry-Run)
        print(f"🚨 AMEAÇA CONFIRMADA! Iniciando bloqueio do IP: {source_ip}")
        print(f"Motivo: {analysis.get('reasoning')}")

        response_action = {
            "status": "BLOCKED",
            "action_taken": "WAF_BLOCK_IP",
            "target": source_ip,
            "mode": "DRY-RUN (Simulação)"
        }
    else:
        print(f"✅ Tráfego considerado seguro ou inconclusivo. Nenhuma ação tomada.")
        response_action = {
            "status": "ALLOWED",
            "action_taken": "NONE",
            "target": source_ip
        }

    # Retorna o relatório final
    final_report = {
        "task_id": event.get('task_id'),
        "original_event": payload,
        "ai_analysis": analysis,
        "defense_result": response_action
    }

    print(f"Relatório Final: {json.dumps(final_report)}")
    return final_report