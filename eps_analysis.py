# -*- coding: utf-8 -*-
"""PRO v16.1｜EPS趨勢分析（Yahoo Finance優先，失敗時安全降級）"""
import math
import pandas as pd
import yfinance as yf
from utils import yf_symbol


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


def get_eps_analysis(stock_id, market, fallback_eps=None, fallback_growth=None):
    rows = []
    note = "Yahoo季度EPS資料不足，使用目前EPS與成長率估算"
    try:
        ticker = yf.Ticker(yf_symbol(stock_id, market))
        q = ticker.quarterly_income_stmt
        if q is not None and not q.empty:
            candidates = ["Basic EPS", "Diluted EPS", "Basic Average Shares"]
            eps_row_name = next((r for r in q.index if str(r) in ["Basic EPS", "Diluted EPS"]), None)
            if eps_row_name:
                s = q.loc[eps_row_name].dropna().head(8)
                for dt, val in s.items():
                    try:
                        d = pd.to_datetime(dt)
                        period = f"{d.year}Q{d.quarter}"
                    except Exception:
                        period = str(dt)[:10]
                    rows.append({"季度": period, "EPS": _to_float(val)})
                note = "Yahoo季度EPS"
    except Exception:
        pass

    if not rows:
        eps = _to_float(fallback_eps)
        growth = _to_float(fallback_growth)
        if eps > 0:
            q_eps = eps / 4
            # 用EPS成長率建立一組保守趨勢估算，避免畫面空白。
            step = max(-0.08, min(0.10, growth / 100 / 4)) if growth else 0
            vals = []
            for i in range(8):
                factor = (1 - step * (7 - i))
                vals.append(round(max(0, q_eps * factor), 2))
            rows = [{"季度": f"近{i+1}季", "EPS": v} for i, v in enumerate(vals)]
        else:
            rows = []

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna().reset_index(drop=True)
        eps_series = pd.to_numeric(df["EPS"], errors="coerce").dropna()
    else:
        eps_series = pd.Series(dtype=float)

    latest_eps = float(eps_series.iloc[-1]) if len(eps_series) else _to_float(fallback_eps)
    first_eps = float(eps_series.iloc[0]) if len(eps_series) else latest_eps
    positive_count = int((eps_series > 0).sum()) if len(eps_series) else (1 if latest_eps > 0 else 0)
    up_count = int((eps_series.diff().dropna() > 0).sum()) if len(eps_series) >= 2 else 0

    score = 0
    if latest_eps > 0:
        score += 30
    if latest_eps > first_eps and first_eps > 0:
        score += 30
    if up_count >= 5:
        score += 25
    elif up_count >= 3:
        score += 18
    elif up_count >= 1:
        score += 10
    if positive_count >= 6:
        score += 15
    elif positive_count >= 4:
        score += 10

    score = min(100, round(score, 2))
    if score >= 85:
        rating, text = "★★★★★", "EPS趨勢強勁，獲利成長品質佳"
    elif score >= 70:
        rating, text = "★★★★☆", "EPS趨勢偏多，可持續追蹤"
    elif score >= 50:
        rating, text = "★★★☆☆", "EPS表現普通，需搭配營收與法人籌碼"
    else:
        rating, text = "★★☆☆☆", "EPS動能偏弱或資料不足"

    return {
        "df": df,
        "EPS趨勢分": score,
        "EPS趨勢評級": rating,
        "EPS解讀": text,
        "最新EPS": round(latest_eps, 2),
        "資料備註": note,
    }
