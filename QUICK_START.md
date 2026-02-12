# クイックスタートガイド

**読了時間: 5分 | 対象: エンジニア**

このガイドでは、5分でGoogle Forms × Microsoft Forms統合の基本動作を確認できます。

---

## 🎯 このガイドで実現すること

- ✅ Google Forms APIからデータ取得
- ✅ データを統一スキーマに変換
- ✅ ローカルで動作確認

**注:** 完全な実装は [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) を参照してください。

---

## 📋 前提条件

### 必須

- Python 3.9以上
- Google Workspace アカウント
- Google Forms が1つ以上存在すること

### オプション（Phase 1完全実装時）

- Microsoft 365 アカウント（E3以上推奨）
- Make.com アカウント

---

## 🚀 5分クイックスタート

### Step 1: リポジトリをクローン（30秒）

```bash
git clone https://github.com/akira882/GoogleForms-MicrosoftForm_Integration_Project.git
cd GoogleForms-MicrosoftForm_Integration_Project
```

### Step 2: 依存関係をインストール（1分）

```bash
# Python仮想環境の作成（推奨）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### Step 3: Google Forms API認証設定（2分）

1. **Google Cloud Console** (https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成: `client-forms-integration-test`
3. **APIとサービス > ライブラリ** から「Google Forms API」を有効化
4. **認証情報** > **認証情報を作成** > **サービスアカウント**
   - サービスアカウント名: `forms-connector`
   - 役割: `Forms Response Reader`
5. **キー** > **新しいキーを追加** > **JSON** でダウンロード
6. ダウンロードしたJSONを `credentials.json` として保存

### Step 4: テストフォームを作成（30秒）

Google Formsで簡単なテストフォームを作成:

```
タイトル: テスト応募フォーム
質問1: お名前（短答）
質問2: メールアドレス（短答）
質問3: ご応募の動機（長文）
```

自分でテスト回答を1件送信してください。

### Step 5: フォームIDを取得（10秒）

フォームのURLから Form ID を抽出:

```
https://docs.google.com/forms/d/1A2B3C4D5E6F7G8H9I0J/edit
                              ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                              これがForm ID
```

### Step 6: データ取得テスト（30秒）

```bash
python output/06_implementation_samples/google_forms_api_connector.py \
  --form-id YOUR_FORM_ID \
  --credentials credentials.json
```

**成功例:**

```json
[
  {
    "response_id": "abc123...",
    "form_source": "google_forms",
    "form_id": "1A2B3C4D5E6F",
    "form_title": "テスト応募フォーム",
    "submitted_at": "2026-02-12T10:30:00Z",
    "respondent_email": "test@example.com",
    "responses": [
      {
        "question_id": "q1",
        "question_text": "お名前",
        "answer": "山田太郎",
        "question_type": "text"
      }
    ],
    "metadata": {
      "company": "Client",
      "data_version": "v1.1"
    }
  }
]

取得件数: 1件
```

---

## ✅ 成功確認

以下が確認できれば成功です:

- [ ] JSON形式でデータが表示された
- [ ] `form_source: "google_forms"` が含まれている
- [ ] `responses` 配列に質問と回答が含まれている
- [ ] エラーが発生していない

---

## 🔧 トラブルシューティング

### エラー: `google.auth.exceptions.DefaultCredentialsError`

**原因:** 認証情報ファイルが見つからない

**解決策:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

### エラー: `403 Forbidden`

**原因:** サービスアカウントにフォームへのアクセス権がない

**解決策:**
1. Google Formsの**設定** > **回答** > **回答先を変更**
2. サービスアカウントのメールアドレスを共有先に追加
   - 権限: **編集者** または **閲覧者**

### エラー: `ImportError: No module named 'google'`

**原因:** 依存パッケージ未インストール

**解決策:**
```bash
pip install -r requirements.txt
```

詳細は [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) を参照。

---

## 📖 次のステップ

### Phase 1 完全実装

クイックスタートで動作確認ができたら、Phase 1の完全実装に進んでください。

1. [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - Day 1〜30の詳細手順
2. [CHECKLIST.md](./CHECKLIST.md) - 進捗管理用チェックリスト

### Microsoft Forms 統合

Microsoft Formsの統合には以下が必要です:

1. Microsoft 365 アカウント（E3以上推奨）
2. Power Automate の設定
3. Make.com アカウント

詳細は [output/01_feasibility_report.md](./output/01_feasibility_report.md) を参照。

---

## 💡 よくある質問

**Q: なぜMicrosoft Forms APIを直接使用しないのか？**

A: Microsoft Forms Graph APIが未GA（2026年2月時点）のため、Power Automate経由のWebhook連携のみが利用可能です。

**Q: Make.comは必須か？**

A: Phase 1ではMake.comを推奨していますが、Zapierやカスタムスクリプトでも代替可能です。

**Q: BigQueryは無料で使えるか？**

A: 月間1TBクエリ、10GBストレージまで無料です。Phase 2の想定データ量では無料枠内に収まります。

詳細は [FAQ.md](./FAQ.md) を参照。

---

## 📞 サポート

問題が発生した場合:

1. [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) を確認
2. [GitHub Issues](https://github.com/akira882/GoogleForms-MicrosoftForm_Integration_Project/issues) で報告
3. Email: akira882@gmail.com

---

**次のステップ:** [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) で完全実装を開始してください。

---

**最終更新:** 2026-02-12  
**作成者:** Claude Code (Sonnet 4.5)
