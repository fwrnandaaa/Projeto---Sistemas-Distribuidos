import grpc

import relatorio_pb2
import relatorio_pb2_grpc

RELATORIOS_GRPC_ADDR = "localhost:8005"


def _stub():
    canal = grpc.insecure_channel(RELATORIOS_GRPC_ADDR)
    return relatorio_pb2_grpc.RelatorioServiceStub(canal)


def gerar_dashboard() -> dict:
    stub = _stub()
    resposta = stub.GerarDashboard(relatorio_pb2.Vazio(), timeout=5)
    return {
        "total_medicos": resposta.total_medicos,
        "total_consultas": resposta.total_consultas,
        "consultas_hoje": resposta.consultas_hoje,
        "especialidade_mais_procurada": resposta.especialidade_mais_procurada,
        "medico_mais_procurado": resposta.medico_mais_procurado,
    }


def registrar_agendamento(agenda_id: int, usuario_cpf: str) -> dict:
    stub = _stub()
    resposta = stub.RegistrarAgendamento(
        relatorio_pb2.NovoAgendamentoRequest(agenda_id=agenda_id, usuario_cpf=usuario_cpf),
        timeout=5,
    )
    return {
        "sucesso": resposta.sucesso,
        "mensagem": resposta.mensagem,
        "agendamento_id": resposta.agendamento_id,
    }