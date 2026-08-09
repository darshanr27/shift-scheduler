from fastapi import FastAPI, Depends
from routers.auth import  router as auth_router
from routers.shifts import router as shift_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(shift_router)

from services.auth_service import get_current_user
from models.user import User

@app.get("/test-auth")
def test_auth(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}"}