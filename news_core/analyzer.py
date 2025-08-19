import os
from openai import OpenAI

client_ai = OpenAI()

def summarize_and_analyze(text: str, model: str) -> str:
    """記事本文を要約 & 分析"""
    if not text.strip():
        return "記事本文なし。"

    prompt = f"""
以下の記事本文を読み、投資家向けに要約と分析をしてください。

記事本文:
{text[:10000]}

出力フォーマット:
1) 要約（5〜6行程度で詳しく）
2) 市場/投資への影響（ポジ/ネガ/中立を必ず明記し、理由を含める）
3) 影響の大きさ（大/中/小を必ず明記し、根拠を含める）
4) ウラン燃料サイクルのどの段階に関連するか分類してください。
カテゴリ:
- mining（採掘・精錬）
- enrichment（転換・濃縮）
- fuel（燃料製造）
- power（原子力発電）
- waste（廃棄物・再処理）
- other（関連なし）

5) 関連する補足情報（市場動向、周辺ニュース、長期的視点などを2〜3行で）
"""
    try:
        response = client_ai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_summary = response.choices[0].message.content.strip()

        # Markdown形式でフォーマット
        formatted = f"""
📢 **ニュース速報**

{raw_summary}

Analyzed by {model}
"""
        return formatted
    except Exception as e:
        return f"[ERROR] AI分析失敗: {e}"
