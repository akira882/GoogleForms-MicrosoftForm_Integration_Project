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

## セットアップとカスタマイズ

### 1. 依存パッケージのインストール
```bash
pip install -r ../requirements.txt
```

### 2. 環境設定（プレースホルダーの置換）
以下のファイルに含まれる `YOUR_...` という記述は、環境に合わせて書き換える必要があります。

*   **`ms_forms_power_automate_webhook.json`**:
    *   `YOUR_FORM_ID`: Microsoft FormsのURLに含まれるID
    *   `YOUR_WEBHOOK_ID`: Make.comのWebhookモジュールで発行されたURLの末尾
    *   `YOUR_SUBSCRIPTION_ID`: Azure サブスクリプションID
*   **`make_com_scenario_template.json`**:
    *   `YOUR_GOOGLE_SHEETS_ID`: 書き込み先スプレッドシートのURLから取得
*   **`google_forms_api_connector.py`**:
    *   実行時に `--form-id` と `--credentials` を指定

### 3. 実行方法

#### Google Formsからのデータ取得例
```bash
python google_forms_api_connector.py \
  --form-id 1A2B3C4D5E6F \
  --credentials credentials.json
```

#### スキーマ正規化テスト
```bash
python data_schema_normalizer.py
```

## セキュリティ・コンプライアンス上の注意

- **認証情報の管理**: APIキーやサービスアカウント鍵は絶対にリポジトリに含めないでください。環境変数（`.env`）の使用を強く推奨します。
- **匿名化の徹底**: 公共のAI（Claude API等）にデータを送信する際は、必ず `anonymizer.py` を使用して個人情報を不可逆なハッシュ値に変換してください。
- **GMOインターネットグループ基準**: 実際の導入にあたっては、GMO Techセキュリティ委員会のガイドラインに従った設定を行ってください。

---

**最終更新:** 2026-02-12  
**作成者:** 小清水（Akira Koshimizu）
