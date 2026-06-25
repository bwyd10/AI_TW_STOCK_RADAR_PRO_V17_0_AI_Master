# -*- coding: utf-8 -*-
"""PRO v16.1｜近12月營收分析（免費資料源優先，失敗時安全降級）"""
from datetime import datetime
import math
import pandas as pd
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def _to_float(v, default=0.0):
    try:
        if v is None:
            return default
        s = str(v).replace(",", "").replace("%", "").strip()
        if s in ["", "-", "--", "nan", "None"]:
            return default
        x = float(s)
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except Exception:
        return default


def _fetch_month(stock_id, market, year, month):
    """從公開資訊觀測站月營收HTML抓單月。失敗回傳 None。"""
    roc_year = year - 1911
    market_dir = "sii" if market == "上市" else "otc"
    url = f"https://mops.twse.com.tw/nas/t21/{market_dir}/t21sc03_{roc_year}_{month}_0.html"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code != 200:
            return None
        res.encoding = "big5"
        tables = pd.read_html(res.text)
        for tb in tables:
            df = tb.copy()
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [str(c[-1]) for c in df.columns]
            df.columns = [str(c).strip() for c in df.columns]
            code_col = next((c for c in df.columns if "公司代號" in c or "代號" == c), None)
            rev_col = next((c for c in df.columns if "當月營收" in c), None)
            mom_col = next((c for c in df.columns if "上月比較" in c), None)
            yoy_col = next((c for c in df.columns if "去年同月" in c), None)
            if not code_col or not rev_col:
                continue
            hit = df[df[code_col].astype(str).str.strip().str.zfill(4).str[-4:] == str(stock_id).zfill(4)[-4:]]
            if hit.empty:
                continue
            r = hit.iloc[0]
            return {
                "年月": f"{year}-{month:02d}",
                "月營收": _to_float(r.get(rev_col)),
                "月增率%": _to_float(r.get(mom_col)) if mom_col else None,
                "年增率%": _to_float(r.get(yoy_col)) if yoy_col else None,
            }
    except Exception:
        return None
    return None


def get_revenue_analysis(stock_id, market, fallback_growth=None, months=12):
    rows = []
    today = datetime.today()
    # 公開資訊觀測站通常最新月份會落後，因此從上個月開始往回抓。
    y, m = today.year, today.month - 1
    if m == 0:
        y -= 1
        m = 12

    for _ in range(months):
        row = _fetch_month(stock_id, market, y, m)
        if row:
            rows.append(row)
        m -= 1
        if m == 0:
            y -= 1
            m = 12

    if rows:
        df = pd.DataFrame(rows).sort_values("年月").reset_index(drop=True)
        yoy = pd.to_numeric(df.get("年增率%"), errors="coerce").dropna()
        mom = pd.to_numeric(df.get("月增率%"), errors="coerce").dropna()
        latest_yoy = float(yoy.iloc[-1]) if len(yoy) else 0.0
        avg_yoy = float(yoy.tail(3).mean()) if len(yoy) else latest_yoy
        positive_yoy_count = int((yoy.tail(6) > 0).sum()) if len(yoy) else 0
    else:
        df = pd.DataFrame(columns=["年月", "月營收", "月增率%", "年增率%"])
        latest_yoy = _to_float(fallback_growth)
        avg_yoy = latest_yoy
        positive_yoy_count = 0

    score = 0
    if latest_yoy >= 30:
        score += 40
    elif latest_yoy >= 15:
        score += 30
    elif latest_yoy >= 5:
        score += 20
    elif latest_yoy > 0:
        score += 10

    if avg_yoy >= 20:
        score += 30
    elif avg_yoy >= 10:
        score += 20
    elif avg_yoy > 0:
        score += 10

    if positive_yoy_count >= 5:
        score += 30
    elif positive_yoy_count >= 3:
        score += 20
    elif positive_yoy_count >= 1:
        score += 10

    score = min(100, round(score, 2))
    if score >= 85:
        rating, text = "★★★★★", "營收動能強勁，具成長股條件"
    elif score >= 70:
        rating, text = "★★★★☆", "營收趨勢偏多，值得追蹤"
    elif score >= 50:
        rating, text = "★★★☆☆", "營收普通，需搭配EPS與籌碼確認"
    else:
        rating, text = "★★☆☆☆", "營收動能偏弱或資料不足"

    return {
        "df": df,
        "營收趨勢分": score,
        "營收趨勢評級": rating,
        "營收解讀": text,
        "最新年增率%": round(latest_yoy, 2),
        "近3月平均年增率%": round(avg_yoy, 2),
    }
