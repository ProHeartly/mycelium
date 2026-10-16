from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

src = Jinja2Templates(directory="src")

# THis is index aka the main root
@app.get("/")
def root(request: Request):
    return src.TemplateResponse("index.html", {"request": request})