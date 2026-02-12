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
        
    def detect_inconsistencies(self, data: Dict[str, Any]) -> List[str]:
        """データ内の論理的矛盾を検知（例：郵便番号型と住所の不一致、年齢と生年月日の矛盾）"""
        # 個人情報保護のため、送信前に最低限のチェック（メールアドレス等はハッシュ化されるべき）
        prompt = f"""
以下のフォーム回答データ内に論理的な矛盾や不整合、あるいは明らかな入力ミスの可能性があれば具体的に指摘してください。
エンジニアではなく、人事担当者が理解できる言葉で回答してください。

データ:
{json.dumps(data, ensure_ascii=False, indent=2)}

出力形式:
["指摘事項1：〜〜", "指摘事項2：〜〜"]
※矛盾がない場合は空のリスト [] を返してください。
"""
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            content = message.content[0].text.strip()
            # JSONパースの試行
            start = content.find('[')
            end = content.find(']') + 1
            if start != -1 and end != 0:
                return json.loads(content[start:end])
            return []
        except Exception as e:
            # 実際のプロダクション環境ではロギングを行う
            return [f"AI解析エラー: {str(e)}"]

if __name__ == "__main__":
    # 使用例（APIキーを設定して実行）
    # normalizer = ClaudeNormalizer(api_key="your-api-key-here")
    # sample = {"zip": "150-0001", "address": "大阪府大阪市..."}
    # print(normalizer.detect_inconsistencies(sample))
    print("APIキーを設定すると、AIによる高度な矛盾検知（Semantic Validation）が実行可能です。")
