
from fastapi import FastAPI
from bridge.router import router

app = FastAPI(title="TV-Oanda Bridge")
app.include_router(router)