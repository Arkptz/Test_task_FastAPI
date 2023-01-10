import uvicorn


def startup():
    uvicorn.run("app.api:app", host="localhost", port=8081, reload=True)

if __name__ == "__main__":
    startup()