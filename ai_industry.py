# -*- coding: utf-8 -*-
"""
AI台股雷達 PRO v17.0｜AI 產業資料庫
- 50+ AI 細分族群
- 公司多重 AI 標籤
- 供應鏈定位
- 公司 AI 定位資料
"""

AI_THEMES = {
    "半導體": ["晶圓代工", "成熟製程", "先進封裝", "CoWoS", "SoIC", "InFO", "封測", "ASIC", "GPU", "NPU", "IP", "EDA"],
    "記憶體": ["HBM", "DDR5", "DDR6", "DRAM", "NAND", "Enterprise SSD", "Memory Module"],
    "AI伺服器": ["AI Server", "ODM", "Rack", "機殼", "導軌", "滑軌", "Power", "UPS", "BBU", "PDU", "液冷", "風冷", "散熱"],
    "高速傳輸": ["PCB", "CCL", "ABF", "Connector", "高速Cable", "Switch IC", "PCIe", "SerDes", "Retimer", "Redriver"],
    "光通訊": ["800G", "1.6T", "CPO", "矽光子", "光模組", "雷射", "光纖"],
    "網通": ["Ethernet", "InfiniBand", "Router", "Switch", "NIC"],
    "AI應用": ["Robot", "Edge AI", "Industrial AI", "智慧工廠", "醫療AI", "AI車用", "ADAS", "無人機", "AI PC", "AI手機", "AI眼鏡"],
    "AI基建": ["Data Center", "Cloud", "IDC", "Cooling", "Power Grid", "儲能"],
}

# 熱門主題權重：越接近 AI 核心供應鏈，權重越高
THEME_WEIGHT = {
    "CoWoS": 100, "SoIC": 92, "ASIC": 95, "GPU": 95, "HBM": 96,
    "AI Server": 92, "ODM": 86, "液冷": 94, "散熱": 88, "BBU": 88,
    "Power": 86, "UPS": 78, "Data Center": 86, "CPO": 92, "矽光子": 90,
    "800G": 88, "1.6T": 92, "PCB": 82, "ABF": 82, "Connector": 78,
    "Switch IC": 84, "SerDes": 84, "Retimer": 80, "Robot": 76, "Edge AI": 74,
}

# 可持續擴充；沒有列入者會依產業與主流族群自動推斷
COMPANY_AI_TAGS = {
    "2330": ["晶圓代工", "先進封裝", "CoWoS", "SoIC", "ASIC", "GPU", "AI基建"],
    "2303": ["晶圓代工", "成熟製程", "AI邊緣晶片"],
    "2454": ["IC設計", "ASIC", "Edge AI", "AI手機", "AI車用"],
    "3661": ["ASIC", "AI Server", "Data Center", "NVIDIA供應鏈"],
    "6531": ["ASIC", "IP", "HPC", "Data Center"],
    "3443": ["IC設計", "高速傳輸", "Switch IC", "AI Server"],
    "5274": ["IP", "SerDes", "高速傳輸", "AI Server"],
    "2382": ["AI Server", "ODM", "Data Center", "Rack", "雲端伺服器"],
    "3231": ["AI Server", "ODM", "Data Center", "雲端伺服器"],
    "6669": ["AI Server", "ODM", "Data Center", "Rack"],
    "2356": ["AI Server", "ODM", "AI PC", "Edge AI"],
    "2317": ["AI Server", "ODM", "Connector", "Data Center", "電動車AI"],
    "2376": ["AI Server", "ODM", "AI PC", "Edge AI"],
    "2324": ["AI Server", "ODM", "雲端伺服器"],
    "8210": ["AI Server", "機殼", "Rack", "Data Center"],
    "3017": ["散熱", "液冷", "AI Server", "Data Center", "GB300"],
    "3324": ["散熱", "液冷", "AI Server", "Data Center"],
    "6230": ["散熱", "液冷", "AI Server", "Power"],
    "2421": ["散熱", "風冷", "AI Server"],
    "3653": ["散熱", "液冷", "AI Server"],
    "2308": ["Power", "UPS", "BBU", "Data Center", "Cooling", "Robot", "AI基建"],
    "6412": ["Power", "AI Server", "Data Center", "UPS"],
    "1513": ["Power Grid", "重電", "AI基建", "Data Center"],
    "1514": ["Power Grid", "重電", "AI基建"],
    "1519": ["Power Grid", "重電", "AI基建", "儲能"],
    "1605": ["Power Grid", "電線電纜", "AI基建"],
    "3037": ["PCB", "AI Server", "高速傳輸", "Data Center"],
    "8046": ["PCB", "ABF", "AI Server", "高速傳輸"],
    "2383": ["PCB", "AI Server", "高速傳輸", "伺服器板"],
    "2368": ["PCB", "AI Server", "高速傳輸"],
    "6213": ["PCB", "AI Server", "高速傳輸"],
    "3189": ["Connector", "高速Cable", "AI Server", "Data Center"],
    "3163": ["CPO", "矽光子", "光模組", "800G", "1.6T", "Data Center"],
    "3363": ["CPO", "光通訊", "光模組", "800G"],
    "3081": ["光通訊", "光模組", "Data Center"],
    "2345": ["網通", "Switch", "Ethernet", "Data Center"],
    "6285": ["網通", "Switch", "Ethernet", "Data Center"],
    "1590": ["Robot", "Industrial AI", "智慧工廠"],
    "2049": ["Robot", "Industrial AI", "智慧工廠"],
    "2359": ["Robot", "Industrial AI", "AI應用"],
}

SUPPLY_CHAIN_STAGE = {
    "2330": "上游｜晶圓代工與先進封裝",
    "2303": "上游｜晶圓代工",
    "2454": "上游｜IC設計",
    "3661": "上游｜ASIC設計服務",
    "6531": "上游｜ASIC/IP設計",
    "2382": "中游｜AI伺服器ODM",
    "3231": "中游｜AI伺服器ODM",
    "6669": "中游｜AI伺服器ODM",
    "2356": "中游｜伺服器/AI PC",
    "2317": "中游｜伺服器組裝與零組件",
    "3017": "中游｜AI散熱/液冷",
    "3324": "中游｜AI散熱/液冷",
    "2308": "中游｜電源/BBU/資料中心基建",
    "3037": "中游｜高階PCB",
    "3163": "中游｜光通訊/CPO",
    "1513": "下游基建｜重電/電網",
    "1519": "下游基建｜重電/儲能",
}

AI_PRODUCT_HINTS = {
    "晶圓代工": "AI晶片晶圓製造、HPC製程服務",
    "先進封裝": "CoWoS、SoIC、AI/HPC先進封裝",
    "ASIC": "AI ASIC、客製化加速晶片、HPC設計服務",
    "AI Server": "AI伺服器、GPU伺服器、雲端資料中心設備",
    "ODM": "AI伺服器代工、雲端伺服器整機與機櫃整合",
    "散熱": "伺服器散熱模組、均熱板、熱管、風扇",
    "液冷": "冷板、液冷模組、CDU相關散熱方案",
    "Power": "伺服器電源、電源供應器、資料中心電力系統",
    "UPS": "不斷電系統、資料中心備援電力",
    "BBU": "電池備援模組、伺服器備援電源",
    "PCB": "高階伺服器PCB、HDI、加速卡板材",
    "ABF": "高階IC載板、AI/HPC封裝載板",
    "CPO": "共封裝光學、資料中心光互連",
    "矽光子": "矽光子晶片、光電整合模組",
    "光模組": "800G/1.6T光模組、資料中心傳輸模組",
    "Robot": "工業機器人、智慧製造、自動化設備",
    "Power Grid": "電網、重電設備、資料中心供電基建",
}


def normalize_tags(tags):
    out = []
    for t in tags or []:
        t = str(t).strip()
        if t and t not in out:
            out.append(t)
    return out


def infer_ai_tags(stock_id, industry="", theme="", theme_group=""):
    stock_id = str(stock_id).strip()
    tags = list(COMPANY_AI_TAGS.get(stock_id, []))
    text = f"{industry} {theme} {theme_group}"
    keyword_map = {
        "半導體": ["晶圓代工", "IC設計", "ASIC"],
        "晶圓": ["晶圓代工"], "IC": ["IC設計"], "封測": ["封測"],
        "電腦": ["AI Server", "ODM"], "伺服器": ["AI Server", "ODM"],
        "散熱": ["散熱", "液冷"], "電源": ["Power", "UPS"], "重電": ["Power Grid", "AI基建"],
        "PCB": ["PCB", "高速傳輸"], "零組件": ["Connector", "PCB"],
        "光通訊": ["光通訊", "CPO", "800G"], "通信": ["網通", "Ethernet"],
        "機器人": ["Robot", "Industrial AI"], "資訊服務": ["AI軟體", "Cloud"],
    }
    for kw, mapped in keyword_map.items():
        if kw in text:
            tags.extend(mapped)
    return normalize_tags(tags)


def ai_theme_group(tags):
    tags = set(tags or [])
    for group, items in AI_THEMES.items():
        if tags.intersection(set(items)):
            return group
    return "非AI核心"


def theme_heat_weight(tags):
    if not tags:
        return 0
    vals = [THEME_WEIGHT.get(t, 55) for t in tags]
    return round(sum(vals) / len(vals), 2)


def supply_chain_stage(stock_id, tags=None):
    stock_id = str(stock_id).strip()
    if stock_id in SUPPLY_CHAIN_STAGE:
        return SUPPLY_CHAIN_STAGE[stock_id]
    tags = tags or []
    if any(t in tags for t in ["晶圓代工", "ASIC", "IC設計", "HBM", "CoWoS"]):
        return "上游｜晶片/半導體"
    if any(t in tags for t in ["AI Server", "ODM", "散熱", "液冷", "PCB", "Power", "CPO"]):
        return "中游｜伺服器與關鍵零組件"
    if any(t in tags for t in ["Data Center", "Cloud", "Power Grid", "Robot"]):
        return "下游｜資料中心/AI應用/基建"
    return "觀察｜AI關聯待確認"


def ai_product_summary(tags):
    items = []
    for t in tags or []:
        hint = AI_PRODUCT_HINTS.get(t)
        if hint and hint not in items:
            items.append(hint)
    return "；".join(items[:5]) if items else "AI關聯產品待補充，可從公司年報或法說會更新。"
