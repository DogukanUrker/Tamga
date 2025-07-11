# Tamga / examples / fastapi_webapp.py
# Example: Using Tamga with FastAPI

from fastapi import FastAPI, Request

from tamga import Tamga

app = FastAPI()
logger = Tamga(
    log_to_console=True,
    log_to_file=True,
    log_file="fastapi_app.log",
    buffer_size=10,
    show_time=True,
    is_colored=True,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.dir(
        "Incoming request",
        method=request.method,
        path=request.url.path,
        client=str(request.client.host),
    )
    response = await call_next(request)
    logger.dir(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
    )
    return response


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello from FastAPI + Tamga!"}


@app.get("/error")
def error_route():
    try:
        1 / 0
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "Something went wrong"}
    return {"ok": True}


# To run:
# uvicorn examples.fastapi_webapp:app --reload
