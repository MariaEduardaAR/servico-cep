# Serviço de consulta de CEP

Trabalho 2 de Reuso de Software da UFC Quixadá. Dupla: Eduarda Rodrigues e Nathalia.

O projeto terá uma API para reutilizar a consulta de endereços em uma loja e em um formulário de matrícula.

## Primeira etapa

A função normalizar_cep, em app/cep.py, recebe um CEP com oito dígitos, aceita o hífen opcional e preserva o zero inicial. Um formato inválido gera ValueError.

Na raiz do repositório, execute com Python 3:

```bash
python3 -c "from app.cep import normalizar_cep; print(normalizar_cep('01001-000'))"
```

Resultado esperado: 01001000.
