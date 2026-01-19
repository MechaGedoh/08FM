document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scrapeForm');
    const urlInput = document.getElementById('urlInput');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');
    const resultsSection = document.getElementById('resultsSection');
    const companiesList = document.getElementById('companiesList');
    const companyCount = document.getElementById('companyCount');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const urlText = urlInput.value.trim();

        if (!urlText) {
            showError('URLを入力してください');
            return;
        }

        // 複数URLを改行で分割
        const urls = urlText
            .split('\n')
            .map(url => url.trim())
            .filter(url => url.length > 0);

        if (urls.length === 0) {
            showError('有効なURLを入力してください');
            return;
        }

        // UI状態をリセット
        hideError();
        hideResults();
        showLoading();
        disableForm();

        try {
            const response = await fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ urls }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'エラーが発生しました');
            }

            displayResults(data.companies, data.count);

        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
            enableForm();
        }
    });

    function showLoading() {
        loadingIndicator.classList.remove('hidden');
    }

    function hideLoading() {
        loadingIndicator.classList.add('hidden');
    }

    function showError(message) {
        errorMessage.textContent = `❌ ${message}`;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
    }

    function hideResults() {
        resultsSection.classList.add('hidden');
        companiesList.innerHTML = '';
    }

    function displayResults(companies, count) {
        companyCount.textContent = count;
        companiesList.innerHTML = '';

        if (companies.length === 0) {
            showError('不動産会社が見つかりませんでした');
            return;
        }

        companies.forEach((company, index) => {
            const li = document.createElement('li');
            li.textContent = company;
            li.style.animationDelay = `${index * 0.05}s`;
            companiesList.appendChild(li);
        });

        resultsSection.classList.remove('hidden');
    }

    function disableForm() {
        submitBtn.disabled = true;
        urlInput.disabled = true;
    }

    function enableForm() {
        submitBtn.disabled = false;
        urlInput.disabled = false;
    }
});
