from fastapi import FastAPI, Request
from pydantic import BaseModel
from enum import Enum
import aiosqlite

class Language(str, Enum):
    Arabic = "AR",
    Bulgarian = "BG",
    Czech = "CS",
    Danish = "DA",
    German = "DE",
    Greek = "EL",
    English = "EN",
    Spanish = "ES",
    Estonian = "ET",
    Finnish = "FI",
    French = "FR",
    Hungarian = "HU",
    Indonesian = "ID",
    Italian = "IT",
    Japanese = "JA",
    Korean = "KO",
    Lithuanian = "LT",
    Latvian = "LV",
    Norwegian = "NB",
    Dutch = "NL",
    Polish = "PL",
    Portuguese = "PT",
    Romanian = "RO",
    Russian = "RU",
    Slovak = "SK",
    Slovenian = "SL",
    Swedish = "SV",
    Turkish = "TR",
    Ukrainian = "UK"

class ResponseMessage(BaseModel):
    response: str


class TranslationAPI(str, Enum):
    googletranslate = "googletranslate"
    deepl = "deepl"
    libretranslate = "libretranslate"


async def checkquota() -> bool:
    return true


app = FastAPI()

@app.post("/translate/{translation_api}")
async def get_model(translation_api: TranslationAPI, source: Language, target: Language, q: str, user: str | None = None)  -> ResponseMessage:
    match translation_api:
        case "googletranslate":
            if source == "NB":
                source = "NO"
            if target == "NB":
                target = "NO"
            return "Using Google Translate"
        case "deepl":
            return "Using DeepL"
        case "libretranslate":
            return "Using LibreTranslate"
