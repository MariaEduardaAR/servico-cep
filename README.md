# Serviço de consulta de CEP

Trabalho 2 de Reuso de Software da UFC Quixadá. Dupla: Maria Eduarda Almeida Rodrigues e Nathalia de Oliveira Lima.

Uma API REST preenche o endereço de entrega de uma loja e o endereço de matrícula de uma escola. Os dois formulários chamam a mesma rota. A consulta usa o ViaCEP e requer internet. Os testes simulam o provedor e podem ser executados sem rede após a instalação.

## Executar no Linux

Em uma máquina nova com Git e Python 3 (a demonstração foi realizada com Python 3.13):
```bash
git clone https://github.com/MariaEduardaAR/servico-cep.git
cd servico-cep
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Em um clone já preparado, entre na raiz do projeto, ative o ambiente e execute apenas a última linha. Mantenha o terminal aberto. Para encerrar use Ctrl+C.

| Abrir no navegador | Finalidade |
|---|---|
| [Pedido da loja](http://127.0.0.1:8000/formularios/loja.html) | Preencher o endereço de entrega |
| [Matrícula escolar](http://127.0.0.1:8000/formularios/escola.html) | Preencher o endereço do aluno |
| [Documentação interativa](http://127.0.0.1:8000/docs) | Consultar e experimentar o contrato da API |
| [OpenAPI](http://127.0.0.1:8000/openapi.json) | Ler o contrato em JSON |

## Reproduzir a demonstração com o CEP da UFC em Quixadá

1. Abra a loja e consulte 63902-580. Confira Avenida José de Freitas Queiroz, bairro Cedro, Quixadá, CE.
2. Abra a escola e consulte o mesmo CEP. Confira os mesmos campos e as duas chamadas HTTP 200 no terminal.
3. Troque o CEP por abc e consulte novamente. A tela limpa o endereço e mostra a mensagem de formato inválido. O terminal registra HTTP 400.

## Integrar outro consumidor

Com o servidor ativo, execute em outro terminal:
```bash
curl -i http://127.0.0.1:8000/ceps/63902-580
```

A rota GET /ceps/{cep} aceita oito dígitos com hífen opcional. No sucesso devolve:
```json
{"cep":"63902-580","logradouro":"Avenida José de Freitas Queiroz","bairro":"Cedro","cidade":"Quixadá","uf":"CE"}
```

Os erros usam o campo JSON detail. HTTP 400 indica formato inválido, 404 indica CEP inexistente e 502 indica falha ao consultar ou interpretar o provedor.

## Testes e Retry

Com o ambiente ativo, na raiz do repositório:
```bash
python -m unittest discover -s tests -v
python -m unittest discover -s tests -p 'test_retry.py' -k recupera -v
```

O primeiro comando roda os 15 testes. O segundo demonstra um HTTP 503 simulado do provedor seguido de sucesso. A consulta faz até três tentativas, com pausas de 0,2 e 0,4 segundo. Ao esgotar as tentativas, a API devolve 502.

## Organização

- app/cep.py valida e normaliza o CEP.
- app/viacep.py consulta o provedor, aplica Retry e converte a resposta.
- app/main.py publica a rota REST, o modelo de endereço e os arquivos dos formulários.
- consumidores/ contém as duas páginas e o JavaScript de integração compartilhado.
- tests/ cobre consulta ao provedor, contrato HTTP e Retry.

[Relatório técnico em PDF](docs/relatorio.pdf)
