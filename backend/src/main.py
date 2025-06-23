from fastapi import FastAPI

version = "0.1.0"

app = FastAPI(
    title="TomoPlan",
    description="A simple task planning app",
    version=version,
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
