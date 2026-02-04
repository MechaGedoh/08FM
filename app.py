from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin, urlparse

app = Flask(__name__, static_folder='static')

def detect_site(url):
    """
    URLからサイトを判定（SUUMO/HOME'S）
    """
    parsed = urlparse(url)
    if 'suumo.jp' in parsed.netloc:
        return 'SUUMO'
    elif 'homes.co.jp' in parsed.netloc:
        return 'HOMES'
    return None

def scrape_suumo_page(url):
    """
    SUUMOの検索結果ページから不動産会社名を抽出
    jnc（物件詳細）ページにも対応
    """
    try:
        # リクエストヘッダーを設定（ブラウザのように見せる）
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # ページを取得
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # BeautifulSoupでHTMLをパース
        soup = BeautifulSoup(response.content, 'lxml')
        
        # CSSセレクタで会社名を抽出
        # パターン1: 検索結果ページ（bc_*）
        company_elements = soup.select('.detailnote-box-item > div:first-of-type')
        
        # パターン2: 物件詳細ページ（jnc_*）- 複数店舗対応
        if not company_elements:
            company_elements = soup.select('.itemcassette-header-ttl')
        
        # パターン3: 物件詳細ページ（jnc_*）- メイン店舗のみ（フォールバック）
        if not company_elements:
            company_elements = soup.select('.advance_actioncard_reserve-sales-title')
        
        companies = set()
        for element in company_elements:
            company_name = element.get_text(strip=True)
            if company_name:
                companies.add(company_name)
        
        # ページネーションのチェック
        next_page = soup.select_one('.pagination-next')
        
        return list(companies), next_page
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"ページの取得に失敗しました: {str(e)}")
    except Exception as e:
        raise Exception(f"エラーが発生しました: {str(e)}")

def scrape_homes_page(url):
    """
    HOME'Sページから不動産会社名を抽出
    単一会社パターンと複数会社パターンの両方に対応
    人間確認（CAPTCHA）ページの検出にも対応
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # 人間確認（CAPTCHA）ページの検出
        page_text = soup.get_text().lower()
        title = soup.title.string.lower() if soup.title and soup.title.string else ''
        
        # reCAPTCHA や人間確認ページの典型的なパターンを検出
        captcha_indicators = [
            'recaptcha',
            'captcha',
            'robot',
            'ロボット',
            '人間確認',
            'セキュリティチェック',
            'security check',
            'are you human',
            'verify you are human',
            'not a robot'
        ]
        
        for indicator in captcha_indicators:
            if indicator in page_text or indicator in title:
                raise Exception('HOME\'Sで人間確認（CAPTCHA）が表示されました。ブラウザで直接アクセスして確認してください。')
        
        # reCAPTCHA要素の直接検出
        recaptcha_elements = soup.select('.g-recaptcha, [class*="recaptcha"], iframe[src*="recaptcha"]')
        if recaptcha_elements:
            raise Exception('HOME\'Sで人間確認（CAPTCHA）が表示されました。ブラウザで直接アクセスして確認してください。')
        
        companies = set()
        
        # パターン1: 複数会社ページ (.realtorsTtl .name)
        multi_company_elements = soup.select('.realtorsTtl .name')
        if multi_company_elements:
            for element in multi_company_elements:
                company_name = element.get_text(strip=True)
                if company_name:
                    companies.add(company_name)
        
        # パターン2: 単一会社ページ (p.text-sm.mb-1)
        # 複数会社が見つからない場合のみ実行
        if not companies:
            single_company_elements = soup.select('p.text-sm.mb-1')
            for element in single_company_elements:
                company_name = element.get_text(strip=True)
                # 会社名らしいもの（株式会社や店舗名を含む）のみ抽出
                if company_name and ('株式会社' in company_name or '店' in company_name):
                    companies.add(company_name)
                    break  # 単一会社ページなので1つ見つかったら終了
        
        return list(companies)
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"ページの取得に失敗しました: {str(e)}")
    except Exception as e:
        raise Exception(f"エラーが発生しました: {str(e)}")

def scrape_suumo_all_pages(start_url):
    """
    SUUMOの全てのページから不動産会社名を抽出（ページネーション対応）
    """
    all_companies = set()
    current_url = start_url
    page_count = 0
    max_pages = 10  # 安全のため最大ページ数を制限
    
    while current_url and page_count < max_pages:
        companies, next_page = scrape_suumo_page(current_url)
        all_companies.update(companies)
        page_count += 1
        
        # 次のページがあれば続ける
        if next_page and next_page.get('href'):
            # 相対URLを絶対URLに変換
            current_url = urljoin(start_url, next_page['href'])
            # 過度なアクセスを避けるため、少し待機
            time.sleep(1)
        else:
            break
    
    return sorted(list(all_companies))

def scrape_url(url):
    """
    URLからサイトを自動判定してスクレイピング
    """
    site = detect_site(url)
    
    if site == 'SUUMO':
        return scrape_suumo_all_pages(url)
    elif site == 'HOMES':
        return scrape_homes_page(url)
    else:
        raise Exception('SUUMOまたはHOME\'SのURLを指定してください')

@app.route('/')
def index():
    """
    トップページを表示
    """
    return send_from_directory('static', 'index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    """
    POST /api/scrape
    リクエストボディ: {"urls": ["https://suumo.jp/...", "https://www.homes.co.jp/..."]}
    レスポンス: {"companies": ["会社名1", "会社名2", ...], "count": 2}
    """
    try:
        data = request.get_json()
        
        # 後方互換性のため、urlとurlsの両方をサポート
        urls = data.get('urls', [])
        if not urls and 'url' in data:
            urls = [data['url']]
        
        if not urls:
            return jsonify({'error': 'URLが指定されていません'}), 400
        
        all_companies = set()
        
        # 各URLを処理
        for url in urls:
            url = url.strip()
            if not url:
                continue
            
            # URLの検証
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return jsonify({'error': f'無効なURLです: {url}'}), 400
            
            # サイトの検証
            site = detect_site(url)
            if not site:
                return jsonify({'error': f'SUUMOまたはHOME\'SのURLを指定してください: {url}'}), 400
            
            # スクレイピング実行
            try:
                companies = scrape_url(url)
                all_companies.update(companies)
            except Exception as e:
                # 個別URLのエラーはログに記録して続行
                print(f"Error scraping {url}: {str(e)}")
                # エラーを返すか続行するか選択可能
                # ここでは続行する
        
        return jsonify({
            'companies': sorted(list(all_companies)),
            'count': len(all_companies)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
