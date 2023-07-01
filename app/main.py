from http import HTTPStatus

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Luck Bank API",
    version="1.0",
    contact={
        "name": "Marlon Martins",
        "url": "https://github.com/marlonmartins2",
        "email": "marlon.azevedo.m@gmail.com",
    },
    license_info={
        "name": "Copyright",
        "url": "https://github.com/marlonmartins2/luck-bank/blob/master/LICENSE",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health_check")
def health_check():
    """
    Check if API is running.
    """
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
