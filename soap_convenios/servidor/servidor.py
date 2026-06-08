from spyne import Application, rpc, ServiceBase, Unicode, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from dados import planos_aceitos, cobertura

class ConvenioService(ServiceBase):

    @rpc(Unicode, Unicode, _returns=Unicode)
    def verificar_convenio(ctx, cpf, plano):
        if cpf not in cobertura:
            raise Exception(f"CPF {cpf} não encontrado na base de dados")
        if cobertura[cpf] != plano:
            raise Exception(f"Paciente não possui cobertura pelo plano {plano}")
        return f"Cobertura ativa: {cpf} possui cobertura pelo plano {plano}"

    @rpc(_returns=Array(Unicode))
    def listar_planos_aceitos(ctx):
        return planos_aceitos

application = Application(
    [ConvenioService],
    tns="clinica.convenio",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    wsgi_app = WsgiApplication(application)
    server = make_server("0.0.0.0", 8003, wsgi_app)
    server.serve_forever()