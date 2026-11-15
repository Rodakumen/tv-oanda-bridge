
from fastapi import FastAPI

from bridge import models  # noqa: F401
from bridge.database import init_db
from bridge.router import router

init_db()

app = FastAPI(title="TV-Oanda Bridge")
app.include_router(router)