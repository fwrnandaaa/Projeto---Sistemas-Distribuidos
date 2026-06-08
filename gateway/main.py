from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
import re

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