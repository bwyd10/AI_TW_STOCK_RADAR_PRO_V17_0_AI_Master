
def world_champion_score(result):
    sepa=float(result.get("SEPA總分",0) or 0)
    ai=float(result.get("AI冠軍分數",0) or 0)
    bh=float(result.get("黑馬指數",0) or 0)
    score=round(sepa*0.4+ai*0.4+bh*0.2,2)
    grade="S+" if score>=90 else "S" if score>=80 else "A" if score>=70 else "B"
    return {"world_score":score,"world_grade":grade}
