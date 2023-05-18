from fastapi import FastAPI
from routers.user import router as user_router 

app = FastAPI(
    title="animevast",
    version="0.0.1",
    description="Boundless space for anime",
)

app.include_router(router=user_router) # include other FastAPI route

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host= "127.0.0.1", port=9000, reload=True)