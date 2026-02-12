# GMO Tech 採用提案書プロジェクト

## プロジェクト概要

GMO Techの採用面接に向けた「Google Forms × Microsoft Forms ハイブリッドデータ統合アーキテクチャ」の実現可能性精査プロジェクト

## ディレクトリ構成

```
gmo_tech_project/
├── README.md（本ファイル）
├── requirements.txt（Python依存関係）
└── output/
    ├── 01_feasibility_report.md（技術実現可能性レポート）
    ├── 02_roadmap.md（3フェーズ実装ロードマップ）
    ├── 03_roi_analysis.md（コスト・ROI分析レポート）
    ├── 04_security_design.md（セキュリティ・コンプライアンス設計書）
    ├── 05_interview_presentation.md（採用面接用プレゼンテーション資料）
    └── 06_implementation_samples/
        ├── google_forms_api_connector.py
        ├── ms_forms_power_automate_webhook.json
        ├── data_schema_normalizer.py
        ├── bigquery_schema.json
        ├── claude_api_normalizer.pyはなｋ
        ├── make_com_scenario_template.json
        └── anonymizer.py
```

## 解決する課題

- GMO Tech社内：Google Formsでデータ収集（既存運用）
- GMOグループ新規傘下企業：Microsoft Formsでデータ収集（統合困難）
- 問題の本質：Microsoft Forms Graph APIが未GA（2026年2月時点）
- 年間M&A複数件のGMOグループで再現性ある統合テンプレートが必要

## 提案アーキテクチャ（3フェーズロードマップ）

- **Phase 1（1ヶ月）**: Make.com + Power Automateハイブリッド構成 月額$25以下
- **Phase 2（2〜3ヶ月）**: BigQuery + Looker Studio 分析基盤構築
- **Phase 3（6ヶ月〜）**: Claude API自動正規化パイプライン + グループ標準化

## ドリームチームメンバー

1. **中村 海（Kai Nakamura）** - シニア統合アーキテクト / API統合エンジニア
2. **田中 雪（Yuki Tanaka）** - データエンジニアリング & BIリード
3. **石川 涼（Ryo Ishikawa）** - HRテックプロダクトマネージャー / M&A統合スペシャリスト
4. **鈴木 藍佳（Aika Suzuki）** - セキュリティ & コンプライアンスエンジニア
5. **松本 健二（Kenji Matsumoto）** - ビジネスアナリスト / ROI戦略家

## 定量的根拠

- Gartner: データ品質問題のコストは年間平均1,290万ドル（約19億円）
- Forrester: 従業員は週平均12時間（30%）をデータ検索に費やす
- GMO Tech: 2024年度に年間33,624時間のAI削減実績あり
- ROI回収期間試算: 3〜6ヶ月（初期投資450〜750万円）

## セットアップ

```bash
# 依存関係のインストール
pip install -r requirements.txt
```

## 生成日時

2026-02-11

## 作成者

Claude Code (Sonnet 4.5) - 5名のドリームチームによる討議ベース
