from fastapi import FastAPI

import asyncio
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.routers import (
    predict,
)

from app.services.classifier import Classifier


logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

def create_app(test: bool = False) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.text_classifier = Classifier()
        yield

    app = FastAPI(lifespan=lifespan)

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(predict.router)

    @app.get("/")
    async def agent_root():
        return JSONResponse(content={"detail": "Hello World!"})

    return app

app = create_app()

async def run_apps():
    config_agent = uvicorn.Config(
        "main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=["."]
    )
    server_agent = uvicorn.Server(config_agent)

    # Run both servers concurrently
    await asyncio.gather(server_agent.serve())


# main function to run the app
if __name__ == "__main__":
    asyncio.run(run_apps())

# Run in terminal to start: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000