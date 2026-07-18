from fastapi import FastAPI

from routers import router

app = FastAPI(
    title="Kelontong API",
    description="A FastAPI service for managing a kelontong (grocery store) merchandise catalog.",
    version="1.0.0",
    contact={
        "name": "Hendi Santika",
        "email": "hendisantika@yahoo.co.id",
        "url": "https://github.com/hendisantika",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(router=router, prefix="/api")
