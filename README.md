# Contagem de tokens com tiktoken

Projeto simples para resolver os exercicios da apostila de tokenizacao.

## O que tem aqui

- `main.py`: resolve os 4 exercicios usando `tiktoken`.
- `.env`: lugar para colar sua `OPENAI_API_KEY` e ajustar modelo/precos.
- `requirements.txt`: dependencia do projeto.
- `run.bat`: cria ambiente virtual, instala dependencia e roda tudo.

## Como rodar do jeito facil

1. Abra a pasta:

```text
C:\Users\rafael\Documents\contagem-tokens-py
```

2. Clique duas vezes em:

```text
run.bat
```

O script vai:

1. criar a pasta `.venv`
2. instalar `tiktoken`
3. rodar `main.py`
4. mostrar as respostas dos exercicios no terminal

## Onde colocar a chave da OpenAI

Abra o arquivo `.env` e coloque sua chave aqui:

```text
OPENAI_API_KEY=cole_sua_key_aqui
```

Por enquanto o `main.py` nao chama a API da OpenAI. Ele so usa `tiktoken` localmente, entao nao gasta credito.

## Como rodar manualmente

Se quiser rodar sem o `.bat`:

```powershell
cd C:\Users\rafael\Documents\contagem-tokens-py
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Como mudar os precos do exercicio 4

No `.env`, altere:

```text
INPUT_PRICE_PER_1M=0.15
OUTPUT_PRICE_PER_1M=0.60
ESTIMATED_OUTPUT_TOKENS=300
```

Unidade dos precos: dolares por 1 milhao de tokens.

Confirme valores reais antes de usar em algo oficial:

```text
https://openai.com/api/pricing/
```

## O que os exercicios fazem

### Exercicio 1

Conta tokens da frase:

```text
A inteligência artificial está evoluindo rápido.
```

usando `cl100k_base`.

### Exercicio 2

Compara a mesma frase nos encodings:

```text
cl100k_base
o200k_base
p50k_base
```

### Exercicio 3

Monta um chat com:

```text
1 system
3 user
3 assistant
```

e estima o total de tokens da conversa.

### Exercicio 4

Usa o total do chat como entrada, estima uma saida e calcula custo aproximado.

## Observacao importante

Para custo real, o melhor dado e o campo `usage` retornado pelo provider depois da chamada.

O `tiktoken` e otimo para estimar antes de enviar, mas pode existir diferenca entre estimativa local e cobranca/uso real da API.
