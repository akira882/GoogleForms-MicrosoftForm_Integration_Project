# 実装サンプルコード集

このディレクトリには、GMO Tech フォームデータ統合プロジェクトの実装サンプルコードが含まれています。

## ファイル一覧

| ファイル | 説明 | Phase |
|---------|------|-------|
| `google_forms_api_connector.py` | Google Forms APIでデータ取得 | Phase 1 |
| `ms_forms_power_automate_webhook.json` | Power AutomateフローJSON | Phase 1 |
| `data_schema_normalizer.py` | 統一スキーマへの変換 | Phase 1 |
| `bigquery_schema.json` | BigQueryテーブル定義 | Phase 2 |
| `claude_api_normalizer.py` | Claude APIで自動マッピング | Phase 3 |
| `make_com_scenario_template.json` | Make.comシナリオテンプレート | Phase 1 |
| `anonymizer.py` | 個人情報匿名化 | Phase 3 |

## セットアップ

```bash
# 依存パッケージのインストール
pip install -r ../requirements.txt
```

## 使用例

```bash
# Google Forms APIでデータ取得
python google_forms_api_connector.py \
  --form-id 1A2B3C4D5E6F \
  --credentials /path/to/credentials.json

# 個人情報の匿名化
python anonymizer.py --input data.json --output anonymized.json
```

## 注意事項

- 本番環境で使用する前に、必ずテスト環境で動作確認してください
- APIキーや認証情報は `.env` ファイルで管理し、Gitにコミットしないでください
- 個人情報保護法に準拠した運用を行ってください

---

**作成日:** 2026-02-12
**バージョン:** v1.0
