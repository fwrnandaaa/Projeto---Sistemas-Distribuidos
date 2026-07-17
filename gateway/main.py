from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
import re
import relatorios_client

class NovoAgendamentoGrpcSchema(BaseModel):
    agenda_id: int
    usuario_cpf: str

class MedicoSchema(BaseModel):
    nome: str
    crm: str
    especialidade_id: int

class EspecialidadeSchema(BaseModel):
    nome: str

class AgendaSchema(BaseModel):
    medico_id: int
    data: str        
    horario: str    
    disponivel: bool = True

class AgendamentoSchema(BaseModel):
    usuario_cpf: str
    agenda: int

MEDICOS_URL      = "http://localhost:8001"
AGENDAMENTOS_URL = "http://localhost:8002"

#inicianlizando o servidor
app = FastAPI()

#configurando liberação do frontend(api.js) para acessar o gateway
#a porta 3000 é a porta padrão do react, por isso a liberação dela
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
#função pra add os links do hateoas na resposta para o api.js
#data: dados que vieram do microsserviço
#request: request que veio do api.js
#resource: nome do recurso(médico ou agendamento)
def add_hateoas(data, request: Request, resource: str):
    base = str(request.base_url).rstrip("/")
    
    #função responsão por add os links 
    def hateoas(item: dict):
        item_id = item.get("id")
        #o links vai servir para retornar a lista completa do microsserviço que vc quer, 
        #se o source for = a médico então ele retorna a lista dos médicos disponíveis
        links = {"collection": {"href": f"{base}/{resource}"}}

        if item_id:
            links["self"] = {"href": f"{base}/{resource}/{item_id}"}
            if resource == "medicos":
                links["agendamentos"] = {"href": f"{base}/agendamentos?medico_id={item_id}"}
            if resource == "agendas":
                links["agendamentos"] = {"href": f"{base}/agendamentos"}
        return {**item, "_links": links}
 
    #essa função vai ser útil quando data repassada pelo backend tiver vários itens,
    #nesse caso o isinstance garante que a função hateoas adicione os links de hateoas para todos itens 
    # recebidos.
    #se data for do tipo list cai no for, se nao for então ele faz o hateoas direto no data.
    if isinstance(data, list):
        resultado = []
        for item in data:
            resultado.append(hateoas(item))
        return resultado
    return hateoas(data)

#as rotas dos médicos

@app.get("/medicos",  tags=["Médicos"])
def listar_medicos(request: Request):
    #o httpx.get está chamando o microsserviço do méico, funciona da mesma forma que o fetch no api.js
    resp = httpx.get(f"{MEDICOS_URL}/medicos/")
    #verifica se o microsserviço foi chamado corretamente e, caso tenha sido, chama o add_hateoas para 
    #a adição dos links
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Erro no serviço de médicos")
    return add_hateoas(resp.json(), request, "medicos")


@app.get("/medicos/{id}", tags=["Médicos"])
def buscar_medico(id: int, request: Request):
    resp = httpx.get(f"{MEDICOS_URL}/medicos/{id}/")
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return add_hateoas(resp.json(), request, "medicos")

#diferente do get, poste  delete precisam ter sey status code definidos 
#caso contrário retornariam 200 mesmo quando não deu certo
#payload recebe os dados enviados pelo frontend  requisição
@app.post("/medicos", tags=["Médicos"], status_code=201)
def criar_medico(payload: MedicoSchema, request: Request):
    dados = payload.model_dump()
    dados["especialidade"] = dados.pop("especialidade_id")
    resp = httpx.post(f"{MEDICOS_URL}/medicos/", json=dados)
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return add_hateoas(resp.json(), request, "medicos")


@app.delete("/medicos/{id}", tags=["Médicos"], status_code=204)
def deletar_medico(id: int):
    resp = httpx.delete(f"{MEDICOS_URL}/medicos/{id}/")
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

#rotas de especilidade
@app.get("/especialidades", tags=["Especialidades"])
def listar_especialidades(request: Request):
    resp = httpx.get(f"{MEDICOS_URL}/especialidades/")
    return add_hateoas(resp.json(), request, "especialidades")


@app.post("/especialidades", tags=["Especialidades"], status_code=201)
def criar_especialidade(payload: EspecialidadeSchema, request: Request):
    resp = httpx.post(f"{MEDICOS_URL}/especialidades/", json=payload.model_dump())
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return add_hateoas(resp.json(), request, "especialidades")


@app.get("/agendas", tags=["Agendamentos"])
def listar_agendas(request: Request, medico_id: int = None):
    url = f"{AGENDAMENTOS_URL}/agendas/"
    if medico_id:
        url += f"?medico_id={medico_id}"
    resp = httpx.get(url)
    return add_hateoas(resp.json(), request, "agendas")


@app.post("/agendas", tags=["Agendamentos"], status_code=201)
def criar_agenda(payload: AgendaSchema, request: Request):
    medico_resp =  httpx.get(f"{MEDICOS_URL}/medicos/{payload.medico_id}/")
    if medico_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Médico não encontrado")
    resp = httpx.post(f"{AGENDAMENTOS_URL}/agendas/", json=payload.model_dump())
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return add_hateoas(resp.json(), request, "agendas")

@app.delete("/agendas/{id}", tags=["Agendamentos"], status_code=204)
def deletar_agenda(id: int):
    resp = httpx.delete(f"{AGENDAMENTOS_URL}/agendas/{id}/")
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")


@app.get("/agendamentos", tags=["Agendamentos"])
def listar_agendamentos(request: Request):
    resp = httpx.get(f"{AGENDAMENTOS_URL}/agendamentos/")
    return add_hateoas(resp.json(), request, "agendamentos")


@app.post("/agendamentos", tags=["Agendamentos"], status_code=201)
def criar_agendamento(payload: AgendamentoSchema, request: Request):
    resp = httpx.post(f"{AGENDAMENTOS_URL}/agendamentos/", json=payload.model_dump())
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return add_hateoas(resp.json(), request, "agendamentos")


@app.delete("/agendamentos/{id}", tags=["Agendamentos"], status_code=204)
def cancelar_agendamento(id: int):
    resp = httpx.delete(f"{AGENDAMENTOS_URL}/agendamentos/{id}/")
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

SOAP_URL = "http://localhost:8003/"

def chamar_soap(xml: str) -> str:
    resposta = httpx.post(
        SOAP_URL,
        content=xml.encode("utf-8"),
        headers={"Content-Type": "text/xml; charset=utf-8"},
        timeout=30.0
    )
    return resposta.text

@app.get("/convenio/planos", tags=["Convênio"])
def listar_planos():
    xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:tns="clinica.convenio">
       <soapenv:Body>
          <tns:listar_planos_aceitos/>
       </soapenv:Body>
    </soapenv:Envelope>"""
    resposta = chamar_soap(xml)
    planos = re.findall(r"<[^>]*string[^>]*>(.*?)</[^>]*string>", resposta)
    return {"planos": planos}

@app.post("/convenio/cadastrar", tags=["Convênio"])
def cadastrar_convenio(cpf: str, plano: str):
    xml = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:tns="clinica.convenio">
       <soapenv:Body>
          <tns:cadastrar_convenio>
             <tns:cpf>{cpf}</tns:cpf>
             <tns:plano>{plano}</tns:plano>
          </tns:cadastrar_convenio>
       </soapenv:Body>
    </soapenv:Envelope>"""
    resposta = chamar_soap(xml)
    if "Fault" in resposta:
        raise HTTPException(status_code=400, detail="Plano não aceito pela clínica")
    resultado = re.findall(r"<[^>]*cadastrar_convenioResult[^>]*>(.*?)</[^>]*cadastrar_convenioResult>", resposta)
    return {"resultado": resultado[0] if resultado else "Sem resposta"}

@app.get("/convenio/verificar", tags=["Convênio"])
def verificar_convenio(cpf: str, plano: str):
    xml = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:tns="clinica.convenio">
       <soapenv:Body>
          <tns:verificar_convenio>
             <tns:cpf>{cpf}</tns:cpf>
             <tns:plano>{plano}</tns:plano>
          </tns:verificar_convenio>
       </soapenv:Body>
    </soapenv:Envelope>"""
    resposta = chamar_soap(xml)
    if "Fault" in resposta:
        raise HTTPException(status_code=400, detail="Convênio não encontrado ou plano inválido")
    resultado = re.findall(r"<[^>]*verificar_convenioResult[^>]*>(.*?)</[^>]*verificar_convenioResult>", resposta)
    return {"resultado": resultado[0] if resultado else "Sem resposta"}

@app.get("/relatorios/dashboard", tags=["Relatórios (gRPC)"])
def obter_dashboard():
    try:
        return relatorios_client.gerar_dashboard()
    except Exception as erro:
        raise HTTPException(status_code=503, detail=f"Serviço de Relatórios indisponível: {erro}")


@app.post("/relatorios/agendamentos", tags=["Relatórios (gRPC)"], status_code=201)
def registrar_agendamento_via_grpc(payload: NovoAgendamentoGrpcSchema):
    try:
        resultado = relatorios_client.registrar_agendamento(
            agenda_id=payload.agenda_id, usuario_cpf=payload.usuario_cpf
        )
    except Exception as erro:
        raise HTTPException(status_code=503, detail=f"Serviço de Relatórios indisponível: {erro}")

    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    return resultado