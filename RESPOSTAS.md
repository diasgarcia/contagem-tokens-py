# Respostas dos exercicios

Esses resultados foram gerados com `tiktoken==0.12.0`.

## Exercicio 1 - contar tokens de uma frase

Frase:

```text
A inteligência artificial está evoluindo rápido.
```

Encoding usado:

```text
cl100k_base
```

Resultado:

```text
Quantidade: 10 tokens
IDs: [32, 90745, 24625, 21075, 15833, 3721, 44906, 36099, 98420, 13]
Pedacos: ['A', ' intelig', 'ência', ' artificial', ' está', ' ev', 'olu', 'indo', ' rápido', '.']
```

## Exercicio 2 - comparar encodings

Mesma frase em tres encodings:

```text
cl100k_base -> 10 tokens
o200k_base  -> 8 tokens
p50k_base   -> 19 tokens
```

Nesse texto, o mais eficiente foi:

```text
o200k_base, com 8 tokens
```

Interpretacao:

- `o200k_base` conseguiu juntar mais pedacos grandes, como `" inteligência"` e `" rápido"`.
- `p50k_base` quebrou mais o texto, principalmente por causa de acentos.
- Isso mostra por que o encoding escolhido muda a estimativa de custo/contexto.

## Exercicio 3 - chat multi-turn

Conversa montada:

```text
1 system
3 user
3 assistant
```

Modelo usado para escolher encoding:

```text
gpt-4o-mini
```

Contagem aproximada:

```text
#   role         role  conteudo  overhead   total
----------------------------------------------------
1   system          1         9         3      13
2   user            1         6         3      10
3   assistant       1        10         3      14
4   user            1         9         3      13
5   assistant       1        13         3      17
6   user            1         6         3      10
7   assistant       1        13         3      17
----------------------------------------------------
Total aproximado do chat: 97 tokens
```

Observacao:

Essa contagem e uma estimativa local. Para custo real, o mais confiavel e o campo `usage` retornado pelo provider depois da chamada.

## Exercicio 4 - custo estimado

Configuracao usada no `.env`:

```text
OPENAI_MODEL=gpt-4o-mini
INPUT_PRICE_PER_1M=0.15
OUTPUT_PRICE_PER_1M=0.60
ESTIMATED_OUTPUT_TOKENS=300
```

Entrada:

```text
Tokens de entrada estimados: 97
Tokens de saida estimados: 300
```

Calculo:

```text
Custo entrada = 97 / 1_000_000 * 0.15
Custo saida   = 300 / 1_000_000 * 0.60
```

Resultado:

```text
Custo entrada: US$ 0.00001455
Custo saida:   US$ 0.00018000
Custo total:   US$ 0.00019455
```

Importante:

Os precos do `.env` sao didaticos. Antes de usar em algo real, confirme o preco atual em:

```text
https://openai.com/api/pricing/
```
