from spyne import Application, rpc, ServiceBase, Unicode, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.error import ResourceNotFoundError
from wsgiref.simple_server import make_server
from dados import planos_aceitos, cobertura

class ConvenioService(ServiceBase):

    @rpc(Unicode, Unicode, _returns=Unicode)
    def cadastrar_convenio(ctx, cpf, plano):
        if plano not in planos_aceitos:
            raise ResourceNotFoundError(f"Plano {plano} não é aceito pela clínica")
        cobertura[cpf] = plano
        return f"Convênio cadastrado: {cpf} → {plano}"

    @rpc(Unicode, Unicode, _returns=Unicode)
    def verificar_convenio(ctx, cpf, plano):
        if cpf not in cobertura:
            raise ResourceNotFoundError(f"CPF {cpf} não possui convênio cadastrado")
        if cobertura[cpf] != plano:
            raise ResourceNotFoundError(f"Paciente não possui cobertura pelo plano {plano}")
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
    print("Servidor SOAP rodando em http://localhost:8003")
    print("WSDL disponível em http://localhost:8003/?wsdl")
    server.serve_forever()