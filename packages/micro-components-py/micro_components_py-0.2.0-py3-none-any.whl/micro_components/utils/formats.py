import json

def string_to_any(text):
    try:    text = json.loads(text)
    except: ...
    return text