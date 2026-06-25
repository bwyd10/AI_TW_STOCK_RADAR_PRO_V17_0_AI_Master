
def calculate_valuation(result):
    eps=float(result.get("EPS",0) or 0)
    price=float(result.get("收盤價",0) or 0)
    fair_pe=18
    fair_value=round(eps*fair_pe,2) if eps>0 else 0
    undervalued=round((fair_value-price)/price*100,2) if price>0 and fair_value>0 else 0
    return {"fair_value":fair_value,"undervalued_pct":undervalued}
