# app/api/routes.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ready")
def readiness_probe():
    # Có thể kiểm tra DB/ping sau này
    return JSONResponse({"ready": True})


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return "User-agent: *\nDisallow:"
