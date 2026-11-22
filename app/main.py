from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.viacep import CepNaoEncontrado, FalhaViaCEP, consultar_cep

app = FastAPI(title="Serviço de consulta de CEP", version="0.1.0")


class Endereco(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    uf: str


@app.get("/ceps/{cep}", response_model=Endereco, summary="Consultar endereço",
         responses={400: {"description": "Formato inválido"},
                    404: {"description": "CEP inexistente"},
                    502: {"description": "Falha no provedor ViaCEP"}})
def buscar_endereco(cep: str):
    """Aceita oito dígitos com ou sem hífen, por exemplo 01001-000."""
    try:
        return consultar_cep(cep)
    except ValueError as erro:
        raise HTTPException(400, detail=str(erro)) from erro
    except CepNaoEncontrado as erro:
        raise HTTPException(404, detail=str(erro)) from erro
    except FalhaViaCEP as erro:
        raise HTTPException(502, detail=str(erro)) from erro
