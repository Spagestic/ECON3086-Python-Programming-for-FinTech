from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests
from dotenv import load_dotenv


GAMMA_BASE = "https://gamma-api.polymarket.com"
FIRECRAWL_SEARCH_URL = "https://api.firecrawl.dev/v1/search"


def load_local_env(env_path: str = ".env") -> None:
    path = Path(env_path)
    if path.exists():
        load_dotenv(path)


@dataclass
class MarketCandidate:
    id: str
    question: str
    slug: str | None = None
    volume24hr: float | None = None
    liquidity: float | None = None
    outcome_prices: list[float] | None = None
    clob_token_ids: list[str] | None = None


def parse_jsonish(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def safe_float(value: Any) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_token_ids(raw: Any) -> list[str]:
    parsed = parse_jsonish(raw)
    if isinstance(parsed, list):
        return [str(item) for item in parsed if str(item).strip()]
    if isinstance(parsed, str):
        return [part.strip() for part in parsed.split(",") if part.strip()]
    return []


class PolymarketSingleAgent:
    def __init__(self) -> None:
        load_local_env()
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        self.mistral_model = os.getenv("MISTRAL_MODEL", "mistral-large-2512")
        self.session = requests.Session()

    def fetch_markets(self, limit: int = 10) -> list[dict[str, Any]]:
        params = {
            "limit": limit,
            "order": "volume24hr",
            "ascending": "false",
            "active": "true",
            "closed": "false",
        }
        response = self.session.get(f"{GAMMA_BASE}/markets", params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []

    def choose_market(self, markets: list[dict[str, Any]]) -> MarketCandidate:
        if not markets:
            raise RuntimeError("No Polymarket markets were returned.")

        market = markets[0]
        return MarketCandidate(
            id=str(market.get("id", "")),
            question=str(market.get("question", "")),
            slug=market.get("slug"),
            volume24hr=safe_float(market.get("volume24hr")),
            liquidity=safe_float(market.get("liquidity")),
            outcome_prices=parse_jsonish(market.get("outcomePrices")),
            clob_token_ids=parse_token_ids(market.get("clobTokenIds")),
        )

    def fetch_firecrawl_context(self, query: str) -> list[dict[str, Any]]:
        if not self.firecrawl_api_key:
            return []

        headers = {
            "Authorization": f"Bearer {self.firecrawl_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "limit": 5,
            "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True},
        }
        response = self.session.post(FIRECRAWL_SEARCH_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        results = data.get("data", []) if isinstance(data, dict) else []
        return results if isinstance(results, list) else []

    def build_prompt(
        self,
        market: MarketCandidate,
        sources: list[dict[str, Any]],
    ) -> str:
        source_text = []
        for item in sources[:5]:
            title = item.get("title") or item.get("metadata", {}).get("title") or "Untitled"
            url = item.get("url") or item.get("link") or ""
            snippet = item.get("markdown") or item.get("content") or item.get("description") or ""
            source_text.append(f"- {title}\n  URL: {url}\n  Snippet: {snippet[:1200]}")

        sources_block = "\n\n".join(source_text) if source_text else "No external sources were collected."
        token_ids = ", ".join(market.clob_token_ids or []) or "None found"

        return f"""
You are a Polymarket research agent.

Your job is to read one market, inspect a few public web sources, and make a simulated trading decision.
Do not place any trades. Return only valid JSON.

Market:
- question: {market.question}
- slug: {market.slug}
- volume24hr: {market.volume24hr}
- liquidity: {market.liquidity}
- outcome_prices: {market.outcome_prices}
- clob_token_ids: {token_ids}

Web context:
{sources_block}

Decision rules:
- Prefer markets where the event is well-defined, time-bounded, and researchable from public sources.
- If the evidence is weak or the market is too ambiguous, choose skip.
- If you choose a side, use "YES" or "NO".
- Include a short thesis and mention the most important source(s).

Return JSON with these fields:
{{
  "decision": "buy_yes" | "buy_no" | "skip",
  "confidence": 0.0,
  "side": "YES" | "NO" | null,
  "entry_price": 0.0 | null,
  "fair_value": 0.0 | null,
  "expected_value_edge": 0.0 | null,
  "reasoning": ["..."],
  "key_sources": ["..."],
  "risk_flags": ["..."],
  "research_summary": "..."
}}
""".strip()

    def ask_llm(self, prompt: str) -> dict[str, Any]:
        if not self.mistral_api_key:
            raise RuntimeError("MISTRAL_API_KEY is not set.")

        response = self.session.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.mistral_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.mistral_model,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0.2,
            },
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"] or ""
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
        json_text = match.group(1) if match else content
        return json.loads(json_text)

    def run(self) -> dict[str, Any]:
        markets = self.fetch_markets(limit=10)
        market = self.choose_market(markets)
        query = market.question
        sources = self.fetch_firecrawl_context(query)
        if not sources:
            sources = self.fetch_firecrawl_context(f'"{query}"')
        prompt = self.build_prompt(market, sources)
        decision = self.ask_llm(prompt)

        return {
            "market": {
                "id": market.id,
                "question": market.question,
                "slug": market.slug,
                "volume24hr": market.volume24hr,
                "liquidity": market.liquidity,
                "outcome_prices": market.outcome_prices,
                "clob_token_ids": market.clob_token_ids,
            },
            "sources": sources,
            "decision": decision,
        }


def main() -> None:
    agent = PolymarketSingleAgent()
    result = agent.run()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
