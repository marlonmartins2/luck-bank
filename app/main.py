from http import HTTPStatus

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from settings import settings

from version import __version__

from routers import (
    auth_router,
    accounts_router,
    address_router,
    documents_router,
    user_router,
)


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    version=__version__,
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
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(accounts_router)
app.include_router(address_router)
app.include_router(documents_router)

@app.get("/health_check")
def health_check():
    """
    Check if API is running.
    """
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
