# MyChatMe - マルチリンガルAIチャットアプリケーション

[![Built with Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b.svg)](https://www.streamlit.io)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

高度なマルチリンガルAIチャットアプリケーションで、複数の言語での対話とプロンプトテンプレート管理を実現します。

[English](README_en.md) | 日本語

## 🌟 主な機能

- 🤖 複数のAIモデルをサポート
  - OpenAI GPT-4
  - Google Gemini-2.0
  - Anthropic Claude-3.5
- 🌐 多言語対応
  - 日本語とEnglishのインターフェース
  - 言語切り替え機能
- 📝 プロンプトテンプレート管理
  - テンプレートの保存・編集
  - カテゴリ分類
- 💾 チャット履歴
  - マークダウン形式でエクスポート
  - PDF出力対応
- 🎨 カスタマイズ可能なテーマ
- ⚡ レスポンシブデザイン

## 🛠️ 技術スタック

- **フロントエンド**: Streamlit
- **バックエンド**: Python 3.12
- **AI統合**:
  - OpenAI API
  - Google Gemini API (via OpenRouter)
  - Anthropic Claude API (via OpenRouter)
- **国際化**: カスタムi18nシステム
- **データ出力**: ReportLab (PDF生成)

## 📋 必要条件

- Python 3.12以上
- OpenAI APIキー
- OpenRouter APIキー（Gemini-2.0とClaude-3.5用）

## 🚀 セットアップ

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/mychatme.git
cd mychatme
```

2. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
```bash
# .env ファイルを作成
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

4. アプリケーションの起動:
```bash
streamlit run main.py
```

## 💡 使用方法

1. **言語の選択**:
   - サイドバーから日本語/英語を選択

2. **AIモデルの選択**:
   - GPT-4, Gemini-2.0, Claude-3.5から選択
   - 各モデルの特徴に応じて使い分け

3. **プロンプトテンプレート**:
   - テンプレートの作成・保存
   - 保存したテンプレートの呼び出し
   - テンプレートの編集・削除

4. **チャット履歴の管理**:
   - チャット内容のエクスポート（MD/PDF）
   - タイムゾーン対応の履歴管理

5. **テーマカスタマイズ**:
   - ライト/ダークモード
   - カラーテーマの変更

## 🔒 セキュリティ

- API認証情報は環境変数で管理
- セッション管理による安全な状態保持
- エラーハンドリングとレート制限の実装

## 🤝 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- [Streamlit](https://streamlit.io/) - 素晴らしいWebアプリケーションフレームワーク
- [OpenAI](https://openai.com/) - GPT-4モデルの提供
- [OpenRouter](https://openrouter.ai/) - 統合AIモデルアクセス
- [ReportLab](https://www.reportlab.com/) - PDFエクスポート機能

## 📞 サポート

問題や提案がある場合は、GitHubのIssueセクションでお知らせください。
