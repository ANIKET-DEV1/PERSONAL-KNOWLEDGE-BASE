from fastapi import FastAPI
from .routing import auth,user,note
from app.config.app_config import getAppconfig
app= FastAPI()
app.include_router(auth.auth)
app.include_router(user.user)
app.include_router(note.note)
@app.get("/")
def root():
    config= getAppconfig()
    return {"app_name":config.app_name,
            "database_url":config.database_url}


