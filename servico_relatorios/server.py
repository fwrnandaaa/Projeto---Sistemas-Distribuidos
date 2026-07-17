from collections import Counter
from concurrent import futures
from datetime import date

import grpc
import requests

import relatorio_pb2
import relatorio_pb2_grpc

MEDICOS_URL = "http://localhost:8001"
AGENDAMENTOS_URL = "http://localhost:8002"
GRPC_PORT = 8005


class RelatorioServiceServicer(relatorio_pb2_grpc.RelatorioServiceServicer):
    def GerarDashboard(self, request, context):
        try:
            resposta_medicos = requests.get(f"{MEDICOS_URL}/medicos/", timeout=5)
            resposta_agendamentos = requests.get(
                f"{AGENDAMENTOS_URL}/agendamentos/", timeout=5
            )
            resposta_medicos.raise_for_status()
            resposta_agendamentos.raise_for_status()
            medicos = resposta_medicos.json()
            agendamentos = resposta_agendamentos.json()
        except (requests.RequestException, ValueError) as erro:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details(f"Não foi possível consultar os serviços: {erro}")
            return relatorio_pb2.DashboardResponse()

        hoje = date.today().isoformat()
        consultas_hoje = sum(
            1
            for agendamento in agendamentos
            if agendamento.get("agenda_detalhe", {}).get("data") == hoje
        )

        medicos_por_id = {medico["id"]: medico for medico in medicos}
        contagem_especialidade = Counter()
        contagem_medico = Counter()
        for agendamento in agendamentos:
            medico_id = agendamento.get("agenda_detalhe", {}).get("medico_id")
            medico = medicos_por_id.get(medico_id)
            if medico:
                contagem_medico[medico["nome"]] += 1
                especialidade = medico.get("especialidade_detalhe")
                if especialidade:
                    contagem_especialidade[especialidade["nome"]] += 1

        especialidade_top = (
            contagem_especialidade.most_common(1)[0][0]
            if contagem_especialidade
            else "Sem dados"
        )
        medico_top = (
            contagem_medico.most_common(1)[0][0]
            if contagem_medico
            else "Sem dados"
        )

        return relatorio_pb2.DashboardResponse(
            total_medicos=len(medicos),
            total_consultas=len(agendamentos),
            consultas_hoje=consultas_hoje,
            especialidade_mais_procurada=especialidade_top,
            medico_mais_procurado=medico_top,
        )

    def RegistrarAgendamento(self, request, context):
        try:
            resposta = requests.post(
                f"{AGENDAMENTOS_URL}/agendamentos/",
                json={"usuario_cpf": request.usuario_cpf, "agenda": request.agenda_id},
                timeout=5,
            )
        except requests.RequestException as erro:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details(f"Não foi possível consultar o serviço de agendamentos: {erro}")
            return relatorio_pb2.AgendamentoResponse(
                sucesso=False, mensagem="Serviço de agendamentos indisponível"
            )

        try:
            dados = resposta.json()
        except ValueError:
            dados = {}

        if resposta.status_code not in (200, 201):
            mensagem = dados.get("detail", resposta.text or "Não foi possível registrar o agendamento")
            return relatorio_pb2.AgendamentoResponse(sucesso=False, mensagem=str(mensagem))

        return relatorio_pb2.AgendamentoResponse(
            sucesso=True,
            mensagem="Agendamento registrado com sucesso",
            agendamento_id=dados.get("id", 0),
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    relatorio_pb2_grpc.add_RelatorioServiceServicer_to_server(
        RelatorioServiceServicer(), server
    )
    endereco = f"[::]:{GRPC_PORT}"
    porta = server.add_insecure_port(endereco)
    if porta == 0:
        raise RuntimeError(f"Não foi possível abrir a porta gRPC {GRPC_PORT}.")

    server.start()
    print(f"Serviço de relatórios gRPC ativo em {endereco}", flush=True)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=5)


if __name__ == "__main__":
    serve()
