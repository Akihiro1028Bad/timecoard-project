# タイムカード情報処理アプリケーション

このアプリケーションは、タイムカードの写真をアップロードし、AIを使用して情報を抽出し、Excelファイルとしてダウンロードできるウェブベースのツールです。

## 機能

- タイムカード写真のアップロード（前半と後半）
- 画像の前処理と最適化
- AI（Claude）を使用したタイムカード情報の抽出
- 抽出された情報の表示と編集
- 編集済みデータのExcelファイルへの出力

## 必要条件

- Python 3.7以上
- Flask
- Anthropic API キー
- その他の依存ライブラリ（requirements.txtを参照）

## インストール

1. リポジトリをクローンします：

2. 必要なライブラリをインストールします：

3. `.env`ファイルを作成し、Anthropic APIキーを設定します：

## 使用方法

1. アプリケーションを起動します：

2. ブラウザで `http://localhost:5000` にアクセスします。

3. 月を選択し、タイムカードの前半と後半の写真をアップロードします。

4. 「アップロードして処理」ボタンをクリックします。

5. 抽出された情報を確認し、必要に応じて編集します。

6. 「Excelファイルをダウンロード」ボタンをクリックしてデータをダウンロードします。

## ファイル構成

- `app.py`: メインのFlaskアプリケーション
- `config.py`: アプリケーションの設定
- `ai_communication.py`: Anthropic APIとの通信を管理
- `image_processing.py`: 画像の前処理を行う
- `excel_generation.py`: Excelファイルの生成を担当
- `index.html`: メインのHTMLテンプレート
- `styles.css`: アプリケーションのスタイル
- `main.js`: クライアントサイドのJavaScript

## 主要な処理フロー

1. ユーザーが月を選択し、タイムカードの写真をアップロード
2. `image_processing.py`で画像の前処理を実行
3. `ai_communication.py`を通じてAnthropic APIに処理された画像を送信し、タイムカード情報を抽出
4. 抽出された情報をユーザーに表示し、編集を可能にする
5. ユーザーが編集を完了し、Excelダウンロードボタンをクリック
6. `excel_generation.py`を使用してExcelファイルを生成し、ダウンロードを提供

## 注意事項

- このアプリケーションはデモンストレーション目的で作成されています。実際の使用には、セキュリティやエラー処理の追加の考慮が必要です。
- Anthropic APIの使用には料金が発生する可能性があります。使用前に料金体系を確認してください。
- アップロードされた画像や生成されたExcelファイルは一時的にサーバーに保存されます。適切なデータ管理とプライバシー保護の措置を講じてください。

## 将来の改善点

- ユーザー認証の実装
- 複数のAIモデルのサポート
- バッチ処理機能の追加
- エラーハンドリングの強化
- ユニットテストとインテグレーションテストの追加

## ライセンス

[ライセンス情報をここに記載]

## 貢献

プルリクエストは歓迎します。大きな変更を加える場合は、まずissueを開いて変更内容を議論してください。

## サポート

問題が発生した場合は、Githubのissueを通じてご連絡ください。