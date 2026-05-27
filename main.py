from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request, error: str = None):
    """Ruta raíz — muestra el formulario de login."""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error}
    )


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Captura el formulario y redirige según la contraseña."""
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return RedirectResponse(url=f"/bienvenido?usuario={username}", status_code=303)
    return RedirectResponse(url="/?error=Credenciales+incorrectas", status_code=303)


@app.get("/bienvenido", response_class=HTMLResponse)
async def bienvenido(request: Request, usuario: str = ""):
    """Pantalla de bienvenida tras autenticación exitosa."""
    return templates.TemplateResponse(
        "bienvenido.html",
        {"request": request, "usuario": usuario}
    )