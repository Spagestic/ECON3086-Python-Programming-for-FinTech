from openai import OpenAI
import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def analyse_news_title(news_title: str) -> dict:

    prompt = f"""
You are a financial analyst specializing in stock market events. Carefully analyze the following news headline:

"{news_title}"

Please answer the following points and return your assessment in valid JSON format.
For your answer, return only a well-formed JSON object covering these fields:
- impact_on_stock_price: specify "impact" (choose: "positive", "negative", or "neutral") and a one-sentence "reason".
- impact_duration: specify "duration" (choose: "short-term", "medium-term", or "long-term") and a brief "rationale".
- relation_to_financials: specify "aspect" ("costs", "profits", or "both") and a short "reasoning".
- other_investment_factors: an array with at least one object that has "factor" (name/type) and "description" (brief explanation of its relevance).

Example format:
{{
  "impact_on_stock_price": {{"impact": "...", "reason": "..."}},
  "impact_duration": {{"duration": "...", "rationale": "..."}},
  "relation_to_financials": {{"aspect": "...", "reasoning": "..."}},
  "other_investment_factors": [
    {{"factor": "...", "description": "..."}}
  ]
}}

Replace the ... areas with your own analysis.
Return only valid JSON.
"""


    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",      # Optional
        },
        extra_body={},
        model="google/gemini-2.5-pro",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    content = completion.choices[0].message.content

    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
    if code_match:
        json_str = code_match.group(1)
    else:
        json_str = content

    return json.loads(json_str)



news_title = "Singer D4vd reportedly identified as suspect in death of teen found in Tesla"
result = analyse_news_title(news_title)
print(json.dumps(result, indent=2, ensure_ascii=False))
