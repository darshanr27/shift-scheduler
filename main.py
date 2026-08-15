from fastapi import FastAPI, Depends
from routers.auth import  router as auth_router
from routers.shifts import router as shift_router
from routers.assignments import router as assignment_router
from routers.export import router as export_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(shift_router)
app.include_router(assignment_router)
app.include_router(export_router)