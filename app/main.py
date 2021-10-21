from fastapi import FastAPI,Request,File,UploadFile,Depends,HTTPException
import pathlib
from fastapi.responses import HTMLResponse,FileResponse
from functools import lru_cache
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
import uuid
import os
import io
from PIL import Image
import pytesseract


class Settings(BaseSettings):
    debug:bool = False
    echo_active=False

    class Config:
        env_file=".env"

@lru_cache
def get_settings():
    return Settings()


DEBUG=get_settings().debug

BASE_DIR=pathlib.Path(__file__).parent
UPLOAD_DIR=BASE_DIR/"uploads"

print(BASE_DIR)

app=FastAPI()
templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))

print(DEBUG)
@app.get("/",response_class=HTMLResponse)
def home_view(request:Request,settings:Settings=Depends(get_settings)):
    print(settings.debug)
    return templates.TemplateResponse("home.html",{"request":request,"abc":123})

@app.post("/")
async def prediction_view(file:UploadFile=File(...),settings:Settings=Depends(get_settings)):
    bytes_str=io.BytesIO(await file.read())
    try:
        img=Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid Image",status_code=400)
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    preds=pytesseract.image_to_string(img)
    predictions=[x for x in preds.split("\n")]
    return {"results":predictions,"orginal":preds}

@app.post("/img-echo/",response_class=FileResponse)
async def img_echo_view(file:UploadFile=File(...),settings:Settings=Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid Exception",status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str=io.BytesIO(await file.read())
    try:
        img=Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid Image",status_code=400)
    fname=pathlib.Path(file.filename)
    fext=fname.suffix
    dest=UPLOAD_DIR/f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest