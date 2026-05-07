from app.app import app
print("Import successful!")
if  __name__=="__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="localhost",port=8000,reload=True)
