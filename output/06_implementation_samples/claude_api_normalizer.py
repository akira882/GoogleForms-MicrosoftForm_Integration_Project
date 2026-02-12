#!/usr/bin/env python3
"""
Claude API自動正規化スクリプト（Phase 3）

表記ゆれを自動修正し、データ品質を向上させます。
"""

import anthropic
import json
from typing import Dict, Any, List

class ClaudeNormalizer:
    """Claude APIを使用したデータ正規化クラス"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def normalize_company_name(self, company_name: str) -> str:
        """会社名の正規化（株式会社の表記統一）"""
        prompt = f"""
以下の会社名を正規化してください。
- 「(株)」「㈱」「Co., Ltd.」は全て「株式会社」に統一
- 前株・後株の位置はそのまま
- 回答は会社名のみを返してください（説明不要）

会社名: {company_name}
"""
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()
    
    def auto_map_question(self, question_text: str, standard_schema: List[str]) -> str:
        """質問文を標準スキーマにマッピング"""
        prompt = f"""
以下の質問文を、標準スキーマのいずれかにマッピングしてください。

質問文: {question_text}

標準スキーマ:
{json.dumps(standard_schema, ensure_ascii=False, indent=2)}

回答は標準スキーマの項目名のみを返してください。
該当するものがない場合は "unknown" と返してください。
"""
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()

if __name__ == "__main__":
    # 使用例（APIキーを設定して実行）
    # normalizer = ClaudeNormalizer(api_key="your-api-key-here")
    # print(normalizer.normalize_company_name("GMOﾃｯｸ(株)"))
    print("APIキーを設定すると、AIによる自動正規化が実行可能です。")
