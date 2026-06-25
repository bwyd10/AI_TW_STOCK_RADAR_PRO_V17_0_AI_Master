# AI台股雷達 PRO v17.0｜世界冠軍 AI Master

此版本以 v16.1 為底稿升級，保留原本台股資料、SEPA、VCP、法人籌碼、黑馬指數、EPS、月營收與企業分析功能，新增 AI Master 核心。

## v17.0 新增功能

- 50+ AI 細分族群資料庫
- 公司多重 AI 標籤
- AI 供應鏈定位：上游 / 中游 / 下游 / 基建
- AI Heat Score
- AI Champion Score 2.0
- AI Leader Rating
- 未來三年 AI 成長性評級
- AI 產品重點與白話解讀
- AI Master Dashboard
- Excel 報表升級為 AI Master 決策欄位

## 執行方式

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud 部署

1. 將本專案 ZIP 解壓後上傳 GitHub。
2. Streamlit Cloud 選擇 `app.py`。
3. Python 版本建議 3.10～3.12。
4. 若資料源暫時連線失敗，重新整理或縮小掃描檔數。

## 注意

本工具僅供量化研究與教學，不構成投資建議。股價、法人、財務資料可能因資料源延遲或缺漏而不完整。
