__all__ = ['get']

import requests

def get(url,*args,**kwargs):
    result = []
    while True:
        r = requests.get(url,*args,**kwargs)
        r.raise_for_status()
        result+=r.json()
        if "next" not in r.links or url == r.links["next"]["url"]:
            break
        url = r.links["next"]["url"]
    return result

