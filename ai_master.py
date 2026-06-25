# -*- coding: utf-8 -*-
"""
AI台股雷達 PRO v17.0｜世界冠軍 AI Master 評分引擎
"""
import math

from ai_industry import infer_ai_tags, ai_theme_group, theme_heat_weight, supply_chain_stage, ai_product_summary


def _to_float(value, default=0.0):
    try:
        if value is None:
            return default
        if isinstance(value, str):
            value = value.replace(",", "").replace("%", "").strip()
            if value in ["", "-", "--", "nan", "None"]:
                return default
        value = float(value)
        if math.isnan(value) or math.isinf(value):
            return default
        return value
    except Exception:
        return default


def _yes(value):
    return str(value).strip().lower() in ["yes", "true", "1", "通過"]


def _clip(v, lo=0, hi=100):
    return max(lo, min(hi, v))


def calculate_ai_heat_score(result, tags):
    """AI Heat Score：主題權重、法人、量價、RS、成長、突破綜合。"""
    tag_score = theme_heat_weight(tags)
    chip = _to_float(result.get("法人籌碼分"), 0) / 30 * 100
    volume = _to_float(result.get("量比50日"), 1)
    volume_score = _clip((volume - 0.8) / 1.8 * 100)
    rs = _to_float(result.get("RS強度"), 1)
    rs_score = _clip((rs - 0.8) / 0.8 * 100)
    revenue = _to_float(result.get("營收成長%"), 0)
    eps_growth = _to_float(result.get("EPS成長%"), 0)
    growth_score = _clip((max(revenue, 0) * 0.45 + max(eps_growth, 0) * 0.55), 0, 100)
    breakout = 80 if str(result.get("突破訊號", "")).strip() not in ["", "無", "False"] else 45
    trend = 90 if _yes(result.get("Trend通過")) else 45
    heat = (
        tag_score * 0.28 + chip * 0.17 + volume_score * 0.13 + rs_score * 0.15
        + growth_score * 0.12 + breakout * 0.07 + trend * 0.08
    )
    return round(_clip(heat), 2)


def calculate_ai_position_score(tags, stage):
    if not tags:
        return 0
    core = {"CoWoS", "SoIC", "ASIC", "GPU", "HBM", "AI Server", "液冷", "CPO", "矽光子", "BBU", "Power", "Data Center"}
    score = 40 + min(35, len(tags) * 6)
    score += min(20, len(set(tags).intersection(core)) * 5)
    if "上游" in stage or "中游" in stage:
        score += 5
    return round(_clip(score), 2)


def leader_rating(ai_position, champion, heat):
    mix = ai_position * 0.45 + champion * 0.35 + heat * 0.20
    if mix >= 88:
        return "★★★★★ 全球AI龍頭"
    if mix >= 78:
        return "★★★★☆ AI核心供應鏈"
    if mix >= 66:
        return "★★★☆☆ AI受惠股"
    if mix >= 52:
        return "★★☆☆☆ AI間接受惠"
    return "★☆☆☆☆ AI關聯待觀察"


def future_growth_rating(result, tags):
    revenue = _to_float(result.get("營收成長%"), 0)
    eps_growth = _to_float(result.get("EPS成長%"), 0)
    roe = _to_float(result.get("ROE%"), 0)
    ai_score = calculate_ai_position_score(tags, supply_chain_stage(result.get("股票代號"), tags))
    score = _clip(revenue * 0.25 + eps_growth * 0.25 + roe * 1.1 + ai_score * 0.35)
    if score >= 80:
        return "★★★★★"
    if score >= 65:
        return "★★★★☆"
    if score >= 50:
        return "★★★☆☆"
    if score >= 35:
        return "★★☆☆☆"
    return "★☆☆☆☆"


def champion_score_v2(result, ai_position, heat):
    eps_growth = _to_float(result.get("EPS成長%"), 0)
    rev_growth = _to_float(result.get("營收成長%"), 0)
    chip = _to_float(result.get("法人籌碼分"), 0) / 30 * 100
    technical = _to_float(result.get("SEPA技術分"), 0)
    blackhorse = _to_float(result.get("黑馬指數"), 0)
    rs = _to_float(result.get("RS強度"), 1)
    breakout = 100 if str(result.get("突破訊號", "")).strip() not in ["", "無", "False"] else 45
    eps_score = _clip(eps_growth, 0, 100)
    rev_score = _clip(rev_growth, 0, 100)
    market_popularity = _clip((_to_float(result.get("量比50日"), 1) - 0.7) / 1.8 * 100)
    rs_score = _clip((rs - 0.8) / 0.8 * 100)
    total = (
        eps_score * 0.15 + rev_score * 0.15 + ai_position * 0.20 + chip * 0.10
        + technical * 0.10 + blackhorse * 0.10 + breakout * 0.05 + heat * 0.10
        + ((market_popularity + rs_score) / 2) * 0.05
    )
    return round(_clip(total), 2)


def ai_advice(result):
    score = _to_float(result.get("AI Champion Score 2.0"), 0)
    heat = _to_float(result.get("AI Heat Score"), 0)
    leader = str(result.get("AI Leader Rating", ""))
    tags = result.get("AI標籤", "")
    if score >= 85 and heat >= 80:
        action = "強勢核心股，適合列入優先觀察；等待回測支撐或突破確認，避免追高一次買滿。"
    elif score >= 75:
        action = "AI核心供應鏈偏多，適合分批觀察；若法人與營收同步轉強，可提高權重。"
    elif score >= 65:
        action = "屬於AI受惠觀察股，題材有機會但確認度不足，建議等技術面與籌碼轉強。"
    else:
        action = "目前分數不足，先放入追蹤名單，不建議只因AI題材進場。"
    return f"{leader}｜AI標籤：{tags}。{action}"


def enrich_ai_master(result):
    tags = infer_ai_tags(
        result.get("股票代號"),
        result.get("官方產業", ""),
        result.get("主流族群", ""),
        result.get("族群大類", ""),
    )
    stage = supply_chain_stage(result.get("股票代號"), tags)
    ai_group = ai_theme_group(tags)
    ai_position = calculate_ai_position_score(tags, stage)
    heat = calculate_ai_heat_score(result, tags)
    champion = champion_score_v2(result, ai_position, heat)
    result["AI標籤"] = "、".join(tags) if tags else "非AI核心"
    result["AI族群"] = ai_group
    result["AI供應鏈定位"] = stage
    result["AI產品重點"] = ai_product_summary(tags)
    result["AI產業地位分"] = ai_position
    result["AI Heat Score"] = heat
    result["AI Champion Score 2.0"] = champion
    result["AI Leader Rating"] = leader_rating(ai_position, champion, heat)
    result["未來三年AI成長性"] = future_growth_rating(result, tags)
    result["AI白話解讀"] = ai_advice(result)
    return result
