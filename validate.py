import requests

def is_real_woman(name: str) -> bool:
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": name,
        "language": "en",
        "format": "json",
        "limit": 1
    }
    r = requests.get(url, params=params).json()
    if not r.get("search"):
        return False

    entity_id = r["search"][0]["id"]

    details = requests.get("https://www.wikidata.org/wiki/Special:EntityData/" + entity_id + ".json").json()
    claims = details["entities"][entity_id].get("claims", {})

    gender_claims = claims.get("P21", [])
    if not gender_claims:
        return False
    for claim in gender_claims:
        if claim["mainsnak"]["datavalue"]["value"]["id"] == "Q6581072":
            return True

    return False


print(is_real_woman("Taylor Swift"))