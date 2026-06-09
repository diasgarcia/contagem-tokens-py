from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable

import tiktoken


ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_env(path: Path = ENV_PATH) -> None:
    """Small .env loader so this project only depends on tiktoken."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def env_float(name: str, default: float) -> float:
    value = os.environ.get(name, "")
    try:
        return float(value)
    except ValueError:
        return default


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name, "")
    try:
        return int(value)
    except ValueError:
        return default


def encoding_for_model(model: str) -> tiktoken.Encoding:
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"[aviso] Modelo {model!r} nao mapeado no tiktoken. Usando o200k_base.")
        return tiktoken.get_encoding("o200k_base")


def token_pieces(enc: tiktoken.Encoding, token_ids: Iterable[int]) -> list[str]:
    pieces: list[str] = []
    for token_id in token_ids:
        raw = enc.decode_single_token_bytes(token_id)
        pieces.append(raw.decode("utf-8", errors="replace"))
    return pieces


def print_title(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def count_text(enc: tiktoken.Encoding, text: str) -> dict[str, object]:
    token_ids = enc.encode(text)
    return {
        "text": text,
        "ids": token_ids,
        "pieces": token_pieces(enc, token_ids),
        "count": len(token_ids),
    }


def print_token_result(label: str, enc_name: str, result: dict[str, object]) -> None:
    print(f"{label}")
    print(f"Encoding: {enc_name}")
    print(f"Texto: {result['text']}")
    print(f"Quantidade: {result['count']} tokens")
    print(f"IDs: {result['ids']}")
    print(f"Pedacos: {result['pieces']}")
    print()


def approximate_chat_tokens(messages: list[dict[str, str]], model: str) -> tuple[int, list[dict[str, object]]]:
    """
    Approximation for chat-style messages.

    It includes a small overhead per message. This is good for study and local
    estimation, but the provider response usage is the best source for real cost.
    """
    enc = encoding_for_model(model)

    # Common rule used by OpenAI cookbook examples for many chat models.
    tokens_per_message = 3
    tokens_per_name = 1
    assistant_reply_primer = 3

    total = assistant_reply_primer
    rows: list[dict[str, object]] = []

    for i, message in enumerate(messages, start=1):
        role = message.get("role", "")
        content = message.get("content", "")
        name = message.get("name", "")

        role_tokens = len(enc.encode(role))
        content_tokens = len(enc.encode(content))
        name_tokens = len(enc.encode(name)) + tokens_per_name if name else 0
        message_total = tokens_per_message + role_tokens + content_tokens + name_tokens

        total += message_total
        rows.append(
            {
                "n": i,
                "role": role,
                "role_tokens": role_tokens,
                "content_tokens": content_tokens,
                "overhead": tokens_per_message + name_tokens,
                "total": message_total,
            }
        )

    return total, rows


def exercise_1() -> None:
    print_title("Exercicio 1 - contar tokens de uma frase")
    text = "A inteligência artificial está evoluindo rápido."
    enc = tiktoken.get_encoding("cl100k_base")
    result = count_text(enc, text)
    print_token_result("Resposta:", "cl100k_base", result)


def exercise_2() -> None:
    print_title("Exercicio 2 - comparar encodings")
    text = "A inteligência artificial está evoluindo rápido."
    encodings = ["cl100k_base", "o200k_base", "p50k_base"]
    results: list[tuple[str, dict[str, object]]] = []

    for enc_name in encodings:
        enc = tiktoken.get_encoding(enc_name)
        result = count_text(enc, text)
        results.append((enc_name, result))
        print_token_result(f"Comparacao com {enc_name}:", enc_name, result)

    best_count = min(int(result["count"]) for _, result in results)
    best = [enc_name for enc_name, result in results if int(result["count"]) == best_count]
    print(f"Mais eficiente nesse texto: {', '.join(best)} com {best_count} tokens.")


def exercise_3(model: str) -> tuple[int, list[dict[str, str]]]:
    print_title("Exercicio 3 - chat multi-turn")
    messages = [
        {"role": "system", "content": "Você é um assistente útil e direto."},
        {"role": "user", "content": "O que é tokenização?"},
        {"role": "assistant", "content": "Tokenização é dividir texto em unidades chamadas tokens."},
        {"role": "user", "content": "Por que isso importa em LLMs?"},
        {"role": "assistant", "content": "Porque afeta limite de contexto, custo e qualidade da resposta."},
        {"role": "user", "content": "Me dê um exemplo curto."},
        {"role": "assistant", "content": "A palavra 'rapidamente' pode virar mais de um token."},
    ]

    total, rows = approximate_chat_tokens(messages, model)

    print(f"Modelo usado para escolher encoding: {model}")
    print("Contagem aproximada por mensagem:")
    print()
    print(f"{'#':<3} {'role':<10} {'role':>6} {'conteudo':>9} {'overhead':>9} {'total':>7}")
    print("-" * 52)
    for row in rows:
        print(
            f"{row['n']:<3} {row['role']:<10} "
            f"{row['role_tokens']:>6} {row['content_tokens']:>9} "
            f"{row['overhead']:>9} {row['total']:>7}"
        )

    print("-" * 52)
    print(f"Total aproximado do chat: {total} tokens")
    print()
    print("Obs.: para custo real, prefira o campo usage retornado pelo provider.")
    return total, messages


def exercise_4(input_tokens: int, model: str) -> None:
    print_title("Exercicio 4 - custo estimado")
    output_tokens = env_int("ESTIMATED_OUTPUT_TOKENS", 300)
    input_price = env_float("INPUT_PRICE_PER_1M", 0.15)
    output_price = env_float("OUTPUT_PRICE_PER_1M", 0.60)

    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price
    total_cost = input_cost + output_cost

    print(f"Modelo escolhido: {model}")
    print(f"Tokens de entrada estimados: {input_tokens}")
    print(f"Tokens de saida estimados: {output_tokens}")
    print(f"Preco entrada por 1M tokens: US$ {input_price:.6f}")
    print(f"Preco saida por 1M tokens:   US$ {output_price:.6f}")
    print()
    print(f"Custo entrada: US$ {input_cost:.8f}")
    print(f"Custo saida:   US$ {output_cost:.8f}")
    print(f"Custo total:   US$ {total_cost:.8f}")
    print()
    print("Importante: os precos no .env sao didaticos. Confira os valores atuais")
    print("em https://openai.com/api/pricing/ antes de usar em algo real.")


def env_summary() -> None:
    print_title("Configuracao carregada")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    print(f"OPENAI_MODEL: {model}")
    print(f"OPENAI_API_KEY: {'definida' if api_key else 'vazia'}")
    print("Obs.: este script nao chama a API e nao gasta credito.")


def main() -> None:
    load_env()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    env_summary()
    exercise_1()
    exercise_2()
    input_tokens, _messages = exercise_3(model)
    exercise_4(input_tokens, model)

    print_title("Checklist")
    print("[ok] contar tokens de texto simples")
    print("[ok] comparar cl100k_base, o200k_base e p50k_base")
    print("[ok] estimar tokens de conversa multi-turn")
    print("[ok] estimar custo antes de chamar API")


if __name__ == "__main__":
    main()
