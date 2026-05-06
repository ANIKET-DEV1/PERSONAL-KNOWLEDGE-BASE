from fastapi import FastAPI,Path,HTTPException,routing
from .models.models import UserCreate,NoteSchemas
from app.config.app_config import getAppconfig
app= FastAPI()
items=[]
@app.get("/")
def root():
    config= getAppconfig()
    return {"app_name":config.app_name,
            "database_url":config.database_url}

@app.post("/user")
def user(item:UserCreate):
    items.append(item)
    return {"items":item}

@app.get("/user")
def showuser():
    return items

@app.put("/user/{name}")
def upitems(name:str,update_items:UserCreate):
    for i,item in enumerate(items):
        if item.name==name:
            items[i]=update_items
            return("Update done")
    return HTTPException(404,"Not found")
    
@app.delete("/user/{name}")
def dele(name:str):
    global items
    items =[item for item in items if item.name!=name]
    return "deleted"