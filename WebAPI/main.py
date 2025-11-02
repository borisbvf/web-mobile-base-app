from fastapi import FastAPI
from routes import user

app = FastAPI(title="BaseAppUsers")

app.include_router(
    router=user.user_router,
    prefix="/user",
    tags=["user"]
)

@app.get("/")
async def root():
    return {"Hello": "World"}
