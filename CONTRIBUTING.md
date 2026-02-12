# 貢献ガイド

GMO Forms統合プロジェクトへの貢献を歓迎します！

---

## 🎯 貢献の種類

以下の貢献を受け付けています:

1. **バグ報告** - Issue で報告してください
2. **機能提案** - Issue で提案してください
3. **ドキュメント改善** - Pull Request を送ってください
4. **コード貢献** - Pull Request を送ってください

---

## 🐛 バグ報告

バグを発見した場合、以下の情報を含めてIssueを作成してください:

**テンプレート:**

```markdown
## 環境
- OS: [e.g. macOS 14.0]
- Pythonバージョン: [e.g. 3.11.5]
- 依存パッケージバージョン: [requirements.txtから]

## 再現手順
1. ...
2. ...
3. ...

## 期待する動作
...

## 実際の動作
...

## エラーメッセージ
\`\`\`
完全なスタックトレースを貼り付け
\`\`\`

## スクリーンショット（optional）
...
```

---

## 💡 機能提案

新機能の提案は大歓迎です。以下を含めてください:

1. **問題の説明** - どんな問題を解決しますか？
2. **提案する機能** - 具体的に何をしますか？
3. **ユースケース** - どのように使いますか？
4. **代替案** - 他の解決方法はありますか？

---

## 💻 Pull Request

### 事前準備

1. このリポジトリをForkしてください
2. ブランチを作成してください（`git checkout -b feature/AmazingFeature`）
3. 変更をコミットしてください（`git commit -m 'Add: AmazingFeature'`）
4. Pushしてください（`git push origin feature/AmazingFeature`）
5. Pull Requestを作成してください

### コミットメッセージ規約

以下のプレフィックスを使用してください:

- `Add:` - 新機能追加
- `Fix:` - バグ修正
- `Update:` - 既存機能の更新
- `Docs:` - ドキュメント変更のみ
- `Style:` - コードフォーマット変更
- `Refactor:` - リファクタリング
- `Test:` - テスト追加・修正
- `Chore:` - ビルドプロセス等の変更

**例:**
```
Add: Claude API 自動正規化機能
Fix: Google Forms API 認証エラー
Docs: QUICK_START.md の手順を明確化
```

### コードスタイル

- **Python:** PEP 8準拠
- **JavaScript:** ESLint推奨設定
- **コメント:** 日本語または英語

### テスト

Pull Requestを送る前に、以下を実行してください:

```bash
# テスト実行
pytest

# リンター実行
flake8 output/06_implementation_samples/*.py
```

---

## 📝 ドキュメント貢献

ドキュメントの改善も大歓迎です:

- タイポ修正
- 説明の明確化
- 新しい例の追加
- スクリーンショットの追加

小さな変更でも Pull Request を送ってください。

---

## 🏆 貢献者

貢献者はREADME.mdに記載されます。

---

## 📄 ライセンス

このプロジェクトに貢献することで、あなたの貢献がMIT Licenseの下で公開されることに同意したものとみなされます。

---

**ご質問がある場合:** [GitHub Issues](https://github.com/yourusername/gmo-forms-integration/issues) または Email: your-email@example.com
