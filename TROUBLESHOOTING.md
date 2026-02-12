# トラブルシューティングガイド

よくある問題と解決策をまとめました。

---

## 📋 目次

- [Google Forms API関連](#google-forms-api関連)
- [Power Automate関連](#power-automate関連)
- [Make.com関連](#makecom関連)
- [BigQuery関連](#bigquery関連)
- [Claude API関連](#claude-api関連)
- [一般的な問題](#一般的な問題)

---

## Google Forms API関連

### ❌ エラー: `403 Forbidden - The caller does not have permission`

**原因:** サービスアカウントにフォームへのアクセス権がない

**解決策:**
1. Google Formsを開く
2. **設定** > **回答** タブ
3. サービスアカウントのメールアドレス（例: `forms-connector@project-id.iam.gserviceaccount.com`）を共有先に追加
4. 権限: **編集者** または **閲覧者** を選択

---

### ❌ エラー: `google.auth.exceptions.DefaultCredentialsError`

**原因:** 認証情報ファイルが見つからない

**解決策:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/credentials.json"

# またはPythonコード内で直接指定
credentials = service_account.Credentials.from_service_account_file(
    '/full/path/to/credentials.json'
)
```

---

### ❌ エラー: `429 Too Many Requests`

**原因:** APIレート制限超過（600 requests/分）

**解決策:**
```python
import time

# Make.comでスロットリング設定
# 1秒あたり5リクエストに制限
time.sleep(0.2)  # 各リクエスト間に200ms待機
```

---

## Power Automate関連

### ❌ Webhookが動作しない

**原因1:** Webhook URLが間違っている

**解決策:**
- Make.comで Webhook URL を再確認
- URLをコピーして Power Automate に貼り付け直す

**原因2:** Power Automateフローが無効化されている

**解決策:**
1. Power Automate (https://flow.microsoft.com) にログイン
2. **マイフロー** から該当フローを開く
3. 右上の **オンにする** をクリック

---

### ❌ エラー: `The webhook request failed with status code 401`

**原因:** Make.com Webhook に認証設定がされている

**解決策:**
- Make.com Webhook モジュールで **Signature Verification** をオフにする
- または Power Automate で署名ヘッダーを追加

---

## Make.com関連

### ❌ シナリオが実行されない

**原因:** シナリオがオフになっている

**解決策:**
1. Make.com ダッシュボードを開く
2. シナリオの **ON/OFF スイッチ** を確認
3. **Scheduling** が設定されているか確認（Webhook以外の場合）

---

### ❌ エラー: `Invalid JSON format`

**原因:** Power Automateから送信されたデータ形式が不正

**解決策:**
```json
// Power Automate のHTTP Actionで以下を設定
{
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "form_source": "ms_forms",
    "form_id": "@{body('Get_response_details')?['id']}",
    // ...
  }
}
```

---

### ❌ operations上限に達した

**原因:** Make.com Proプラン（月間10,000 operations）を超過

**解決策:**
1. **Businessプラン**（月間40,000 operations）にアップグレード
2. または不要なシナリオを停止
3. シナリオ実行頻度を調整

**コスト:**
- Proプラン: $10〜$25/月
- Businessプラン: $99/月

---

## BigQuery関連

### ❌ エラー: `Access Denied: Project`

**原因:** BigQueryプロジェクトへのアクセス権がない

**解決策:**
1. Google Cloud Console > **IAM と管理**
2. サービスアカウントに `BigQuery Data Editor` 役割を追加

---

### ❌ エラー: `Table not found`

**原因:** テーブルが作成されていない

**解決策:**
```sql
CREATE TABLE `client_unified_forms.responses`
(
  response_id STRING NOT NULL,
  form_source STRING NOT NULL,
  submitted_at TIMESTAMP NOT NULL,
  responses JSON,
  metadata JSON
)
PARTITION BY DATE(submitted_at)
CLUSTER BY form_source;
```

---

### ❌ コストが予想以上に高い

**原因:** パーティションを使用していないクエリ

**解決策:**
```sql
-- ❌ 悪い例（全データスキャン）
SELECT * FROM `client_unified_forms.responses`;

-- ✅ 良い例（パーティション指定）
SELECT * FROM `client_unified_forms.responses`
WHERE DATE(submitted_at) = '2026-02-12';
```

---

## Claude API関連

### ❌ エラー: `401 Unauthorized`

**原因:** APIキーが無効または未設定

**解決策:**
```python
import os
from anthropic import Anthropic

# 環境変数から取得
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# または直接指定
client = Anthropic(api_key="sk-ant-...")
```

---

### ❌ エラー: `429 Rate limit exceeded`

**原因:** APIレート制限超過

**解決策:**
```python
import time
from anthropic import APIError, RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    # 指数バックオフ
    time.sleep(60)  # 60秒待機
    response = client.messages.create(...)
```

---

### ❌ 精度が低い（正規化ミス）

**原因:** Few-shot例が不十分

**解決策:**
```python
prompt = f"""
以下の会社名を正規化してください。

【例】
入力: ㈱Client
出力: 株式会社Client

入力: Client Internet Co., Ltd.
出力: Client Internet株式会社

入力: {company_name}
出力:
"""
```

---

## 一般的な問題

### ❌ データが重複して登録される

**原因:** Webhook が複数回実行されている

**解決策:**
- `response_id` をプライマリキーとして設定
- BigQueryで `MERGE` 文を使用

```sql
MERGE `client_unified_forms.responses` T
USING (SELECT * FROM UNNEST(@new_data)) S
ON T.response_id = S.response_id
WHEN NOT MATCHED THEN INSERT ...
```

---

### ❌ 日本語が文字化けする

**原因:** エンコーディング設定が不正

**解決策:**
```python
# ファイル読み込み時
with open('data.csv', 'r', encoding='utf-8') as f:
    data = f.read()

# JSON出力時
json.dumps(data, ensure_ascii=False, indent=2)
```

---

### ❌ タイムゾーンがずれる

**原因:** UTC と JST の混在

**解決策:**
```python
from datetime import datetime, timezone
import pytz

# UTCで保存
submitted_at = datetime.now(timezone.utc).isoformat()

# JSTで表示
jst = pytz.timezone('Asia/Tokyo')
jst_time = datetime.fromisoformat(submitted_at).astimezone(jst)
```

---

## 🆘 それでも解決しない場合

### サポートチャンネル

1. **GitHub Issues:** https://github.com/akira882/GoogleForms-MicrosoftForm_Integration_Project/issues
2. **Email:** akira882@gmail.com
3. **ドキュメント:** [README.md](./README.md)

### Issue作成時の情報

以下を含めてください:

- **環境:** OS, Pythonバージョン, 依存パッケージバージョン
- **エラーメッセージ:** 完全なスタックトレース
- **再現手順:** 1, 2, 3...
- **期待する動作:** 何が起こるべきか
- **実際の動作:** 何が起こったか

---

**最終更新:** 2026-02-12  
**作成者:** 小清水 晶｜Akira Koshimizu
