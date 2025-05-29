from fastapi import FastAPI
from fga_demo_app.routes import router

app = FastAPI(title="FGA Demo App")

app.include_router(router)
