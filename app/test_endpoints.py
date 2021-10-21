import io
import shutil
import time
from fastapi import responses
from app.main import BASE_DIR, app , UPLOAD_DIR
from fastapi.testclient import TestClient
from PIL import Image,ImageChops

client=TestClient(app)

def test_get_home():
    response=client.get("/")
    assert response.status_code==200
    assert "text/html" in response.headers['content-type']

# def test_post_home():
#     response=client.post("/")
#     assert response.status_code==200
#     assert "application/json" in response.headers['content-type']
#     assert response.json() == {"message":"hello world"}

def test_prediction_upload():
    img_saved_path=BASE_DIR/"images"
    for path in img_saved_path.glob("*"):
        try:
            img=Image.open(path)
        except:
            img=None
        response = client.post("/",files={"file":open(path,'rb')})
        if img is None:
            assert response.status_code==400
        else:
            assert response.status_code==200
            print(response.text)
            data=response.json()
            assert len(data.keys())==2

def test_echo_upload():
    img_saved_path=BASE_DIR/"images"
    for path in img_saved_path.glob("*"):
        try:
            img=Image.open(path)
        except:
            img=None
        response = client.post("/img-echo/",files={"file":open(path,'rb')})
        if img is None:
            assert response.status_code==400
        else:
            assert response.status_code==200
            r_stream=io.BytesIO(response.content)
            echo_img=Image.open(r_stream)
            difference=ImageChops.difference(echo_img,img).getbbox()
            assert difference is None
    shutil.rmtree(UPLOAD_DIR)