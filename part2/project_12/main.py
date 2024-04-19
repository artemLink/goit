import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import contacts_router, auth_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api")
app.include_router(contacts_router.router, prefix="/api")


@app.get("/")
def index():
    return {"message": "ContactBook Application"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            # raise HTTPException(status_code=500, detail="Database is not configured correctly")
            return JSONResponse(status_code=500, content={"detail": "Database is not configured correctly"})
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=500, detail="Error connecting to the database")
        return JSONResponse(status_code=500, content={"detail": "Error connecting to the database"})


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=8000, reload=True, log_level="info"
    )
