from dotenv import load_dotenv

load_dotenv()

from pprint import pprint
from fastapi import FastAPI, Request
from pydantic import BaseModel
from enum import Enum
import time
import os
import sqlite3
import aiosqlite
import requests


gtranslate_key = os.environ['GOOGLE_TRANSLATE_API_KEY']
deepl_key = os.environ['DEEPL_API_KEY']
translationsdb = os.environ['TRANSLATION_DATABASE']


if os.path.isfile(translationsdb):
    pass
else:
    connection_obj = sqlite3.connect(translationsdb)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS requests")
    table = """ CREATE TABLE requests (
                username INTEGER,
                timestamp REAL,
                characters INTEGER,
                method INTEGER
            ); """
    cursor_obj.execute(table)
    connection_obj.close()


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

class TranslationData(BaseModel):
    user: str | None = None
    q: str
    source: Language = Language.English
    target: Language = Language.Japanese
    method: int

async def checkquota() -> bool:
    return True

app = FastAPI()

async def checkquota(method):
    async with aiosqlite.connect(translationsdb) as db:
        lastmonth = time.time() - 2592000
        cursor = await db.execute('SELECT SUM(characters) FROM requests WHERE timestamp > ? AND method = ?', (lastmonth, method))
        amount = await cursor.fetchone()
        try:
            if amount[0] > 1500000:
                return False
        except Exception as e:
            print(e)
            return False
        return True

async def addtodb(method, response, user):
    async with aiosqlite.connect(translationsdb) as db:
        await db.execute('INSERT INTO requests VALUES (?, ?, ?, ?)', (user, time.time(), len(response), 0))
        await db.commit()


@app.post("/translate")
async def translate(data: TranslationData)  -> ResponseMessage:
    q = data.q
    target = data.target.value
    source = data.source.value
    user = data.user
    api = data.method
    if target == source:
        return {"response": "Error: Source and Target languages must be different"}
    
    match api:
        case 0: # Google Translate
            if checkquota(api):
                dat = {
                    "q":q,
                    "target":target.replace("NB", "NO"),
                    "source":source.replace("NB", "NO")
                }
                uri = "https://translation.googleapis.com/language/translate/v2?key="+gtranslate_key
                returndata = requests.request(
                    method="POST",
                    url=uri,
                    json=dat
                ).json()
                try:
                    r = returndata["data"]["translations"][0]["translatedText"]
                except Exception as e:
                    return {"response": "Error: Unexpected Response from Google Translate"}
                await addtodb(api, r, user)
                return {"response": r}

        case 2: # DeepL
            if checkquota(api):
                dat = {
                    "text":[q],
                    "source_lang":source,
                    "target_lang":target
                }
                uri = "https://api.deepl.com/v2/translate"
                returndata = requests.request(
                    headers={'Authorization': deepl_key},
                    method="POST",
                    url=uri,
                    json=dat
                ).json()
                try:
                    r = returndata["translations"][0]["text"]
                except Exception as e:
                    return {"response": "Error: Unexpected Response from DEEPL"}
                await addtodb(api, r, user)
                return {"response": r}
        
        case 1: # LibreTranslate
            dat = {
                "q":q,
                "target":target,
                "source":source
            }
            returndata = requests.request(
                method="POST",
                url="http://localhost:5000/translate",
                json=dat
            ).json()
            try:
                if "translatedText" in returndata:
                    r = returndata["translatedText"]
                else:
                    return {"response": "Error: Translation Failed"}
            except requests.exceptions.JSONDecodeError:
                return {"response": "ERROR: Error retrieving translation"}
            return {"response": r}
