from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# test


@router.get("/", status_code=status.HTTP_200_OK)
def read_users():
    return {"message": "List of users"}
