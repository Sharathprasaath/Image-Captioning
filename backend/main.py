from fastapi import FastAPI
from PIL import Image
from helper import Helper
app = FastAPI()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Image_captioning

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_world():
    return {"Msg": "hello world"}
@app.post("/image/caption")
async def text_encode(data: dict):
    # Inputs
    bytes = data.get("image") # image
    img = Helper.bytes_2_img(bytes)
    img=Image.fromarray(img)
    img_path=img_path = r"C:\Users\Sharath Prasaath\App\temp.jpg"

    img.save(img_path) 
    print(img)
    text=Image_captioning().caption(img_path)
    text= text.replace("startseq ", "").replace(" endseq", "")
    return {"image": text.capitalize()}