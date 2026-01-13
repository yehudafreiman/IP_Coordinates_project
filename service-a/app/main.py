from fastapi import FastAPI
import routers

if __name__ == "__main__":
    app = FastAPI
    app.include_router(routers.router)