from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.main import router


app = FastAPI(root_path="/api/auth")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router=router)


@app.get('/')
async def root():
    return {"message":"Hello from auth service."}
