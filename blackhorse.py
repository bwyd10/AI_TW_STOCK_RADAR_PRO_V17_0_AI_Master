import math

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


def calculate_blackhorse(result):
    score = 0

    revenue_growth = _to_float(result.get("營收成長%"))
    rs = _to_float(result.get("RS強度"))
    chip_score = _to_float(result.get("法人籌碼分"))
    champion_score = _to_float(result.get("AI冠軍分數"))
    roe = _to_float(result.get("ROE%"))
    distance_high = _to_float(result.get("距52週高點%"), 999)
    volume_ratio = _to_float(result.get("量比50日"))

    if revenue_growth >= 15:
        score += 20
    elif revenue_growth >= 5:
        score += 10

    if rs >= 1.2:
        score += 20
    elif rs >= 1.0:
        score += 10

    if chip_score >= 15:
        score += 20
    elif chip_score >= 8:
        score += 10

    if _yes(result.get("VCP通過")):
        score += 15

    if champion_score >= 80:
        score += 15
    elif champion_score >= 70:
        score += 8

    if roe >= 15:
        score += 10
    elif roe >= 10:
        score += 5

    if distance_high <= 15:
        score += 5

    if 1.2 <= volume_ratio <= 2.5:
        score += 5

    score = min(100, round(score, 2))

    if score >= 90:
        stars = "★★★★★"
        level = "S級黑馬"
    elif score >= 75:
        stars = "★★★★☆"
        level = "A級黑馬"
    elif score >= 60:
        stars = "★★★☆☆"
        level = "觀察黑馬"
    else:
        stars = "★★☆☆☆"
        level = "一般觀察"

    return {
        "黑馬指數": score,
        "爆發機率": stars,
        "黑馬評級": level,
    }