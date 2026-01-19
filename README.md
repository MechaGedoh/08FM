# SUUMO 不動産会社リストアップアプリ

SUUMOの賃貸物件検索結果ページから、物件を取り扱っている不動産会社を自動で抽出し、重複を排除してリストアップするWebアプリケーションです。

## 機能

- 🔍 SUUMO・HOME'S検索結果URLから不動産会社名を自動抽出
- 🌐 サイト自動判定（SUUMO/HOME'S）
- 📝 複数URL一括処理（1行に1URL）
- 🔄 複数ページの検索結果にも対応（SUUMO自動ページネーション）
- ✨ 重複する会社名を自動で排除
- 🎨 モダンでプレミアムなダークテーマUI
- ⚡ 高速なレスポンスと滑らかなアニメーション

## 対応サイト

### SUUMO (suumo.jp)
- 賃貸物件検索結果ページ
- ページネーション自動対応
- 例: `https://suumo.jp/jj/chintai/ichiran/...`

### HOME'S (homes.co.jp)
- 単一会社ページ（物件詳細）
  - 例: `https://www.homes.co.jp/chintai/room/...`
- 複数会社ページ（取扱会社一覧）
  - 例: `https://www.homes.co.jp/chintai/.../realtors/`

## 必要要件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## セットアップ手順

### 方法1: 実行ファイル版（推奨）

**Pythonのインストール不要！**

1. **実行ファイルをダブルクリック**
   ```
   SUUMO_HOMES_Scraper.exe
   ```

2. **ブラウザでアクセス**
   
   コンソールウィンドウが開き、Flaskサーバーが起動します。
   ブラウザで以下のURLを開きます：
   ```
   http://localhost:5000
   ```

3. **終了方法**
   
   コンソールウィンドウで `Ctrl+C` を押す

### 方法2: Pythonソースコード版

1. **プロジェクトディレクトリに移動**
   ```powershell
   cd d:\08FM
   ```

2. **仮想環境の作成（推奨）**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **依存パッケージのインストール**
   ```powershell
   pip install -r requirements.txt
   ```

## 使い方

1. **アプリケーションの起動**
   ```powershell
   python app.py
   ```

2. **ブラウザでアクセス**
   
   ブラウザで以下のURLを開きます：
   ```
   http://localhost:5000
   ```

3. **URLを入力して検索**
   
   - SUUMOの検索結果ページのURLをコピー
   - アプリの入力欄にURLを貼り付け
   - 「検索」ボタンをクリック
   - 抽出された不動産会社のリストが表示されます

## 使用例

### SUUMO検索結果
```
https://suumo.jp/jj/chintai/ichiran/FR301FC005/?fw2=&ek=057319450&mt=9999999&cn=9999999&ra=013&et=7&shkr1=03&ar=030&bs=040&ct=6.0&shkr3=03&shkr2=03&mb=20&rn=0573&shkr4=03&cb=5.5
```

このURLで検索すると、以下の4社がリストアップされます：
- (株)ミニミニ城東新小岩店
- (株)アシスト
- (株)福家不動産
- (株)タウンハウジング東京 北千住店

### HOME'S単一会社ページ
```
https://www.homes.co.jp/chintai/room/b46c7b063dc7a6c39d6c4a1eb368d4060a830168/?bid=1219660160864
```

結果: アイレントホーム株式会社　小岩店

### HOME'S複数会社ページ
```
https://www.homes.co.jp/chintai/b-1214120110351/realtors/
```

結果: 15社（ソレイユ、アエラス、ハウスコムなど）

### 複数URL一括処理
テキストエリアに以下のように複数のURLを入力（1行1URL）：
```
https://suumo.jp/jj/chintai/ichiran/...
https://www.homes.co.jp/chintai/room/...
https://www.homes.co.jp/chintai/.../realtors/
```

全URLから会社を抽出し、重複を自動排除したリストが表示されます。

## 技術スタック

- **バックエンド**: Flask (Python)
- **スクレイピング**: BeautifulSoup4 + Requests
- **フロントエンド**: HTML + CSS + Vanilla JavaScript
- **デザイン**: カスタムCSS（ダークテーマ + グラデーション）

## プロジェクト構造

```
d:/08FM/
├── app.py                 # Flaskアプリケーション（バックエンド）
├── requirements.txt       # Python依存パッケージ
├── README.md             # このファイル
└── static/               # 静的ファイル（フロントエンド）
    ├── index.html        # メインHTMLページ
    ├── style.css         # スタイルシート
    └── script.js         # フロントエンドJavaScript
```

## 注意事項

- ⚠️ このツールは個人利用を目的としています
- ⚠️ 過度なアクセスを避けるため、SUUMO複数ページの場合は1秒間隔でアクセスします
- ⚠️ SUUMO・HOME'Sの利用規約を遵守してください
- ⚠️ サイト構造変更により、将来動作しなくなる可能性があります

## ライセンス

このプロジェクトは個人利用を目的としています。
