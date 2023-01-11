import urllib.parse
from fastapi import FastAPI, Body
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Encode(BaseModel):
    url:str

@app.post('/encode')
def encode(data:Encode):
    return urllib.parse.quote(data.url, safe='https://')




def startup():
    uvicorn.run("main:app", host="localhost", port=8081, reload=True)

if __name__ == "__main__":
    startup()