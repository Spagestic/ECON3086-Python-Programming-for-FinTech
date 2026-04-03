from pathlib import Path
import json
import os

import requests


def load_env_file(env_path: str = ".env") -> None:
  """Load key=value pairs from a local .env file into environment variables."""
  path = Path(env_path)
  if not path.exists():
    return

  for raw_line in path.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line:
      continue

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    os.environ.setdefault(key, value)


def main() -> None:
  load_env_file()

  api_key = os.getenv("OPENROUTER_API_KEY")
  if not api_key or api_key == "your_openrouter_api_key_here":
    raise RuntimeError(
      "Please set OPENROUTER_API_KEY in the project .env file before running this script."
    )

  url = "https://openrouter.ai/api/v1/chat/completions"
  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    # Optional, but recommended by OpenRouter for app identification:
    "HTTP-Referer": "http://localhost",
    "X-OpenRouter-Title": "ECON3086 In-Class Example",
  }
  payload = {
    "model": "qwen/qwen3.6-plus:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?",
      }
    ],
  }

  response = requests.post(url, headers=headers, json=payload, timeout=60)
  response.raise_for_status()

  result = response.json()
  print(result["choices"][0]["message"]["content"])


if __name__ == "__main__":
  main()
