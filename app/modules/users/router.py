from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
