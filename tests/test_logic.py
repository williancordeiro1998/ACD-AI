import sys
import os
import json

# Adiciona a pasta raiz ao caminho do Python para conseguir importar 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.handlers.executor import handler

def test_executor_should_block_high_confidence_threats():
    """
    Testa se o Executor decide bloquear quando a IA diz que é 95% malicioso.
    """
    # 1. Preparar (Arrange) - O Input simulado
    mock_event = {
        "payload": {"source_ip": "1.2.3.4"},
        "analysis": {
            "malicious": True,
            "confidence": 0.95,
            "reasoning": "Teste unitário de ataque"
        }
    }

    # 2. Executar (Act) - Chama a função Python direto (sem AWS)
    response = handler(mock_event, None)

    # 3. Validar (Assert)
    assert response["defense_result"]["status"] == "BLOCKED"
    assert response["defense_result"]["mode"] == "DRY-RUN (Simulação)"
    print("\n✅ Teste de Bloqueio: SUCESSO")

def test_executor_should_allow_safe_traffic():
    """
    Testa se o Executor libera tráfego normal.
    """
    mock_event = {
        "payload": {"source_ip": "8.8.8.8"},
        "analysis": {
            "malicious": False,
            "confidence": 0.0,
            "reasoning": "Tráfego limpo"
        }
    }

    response = handler(mock_event, None)

    assert response["defense_result"]["status"] == "ALLOWED"
    print("✅ Teste de Tráfego Seguro: SUCESSO")