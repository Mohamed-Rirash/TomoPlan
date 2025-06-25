from fastapi import APIRouter


router = APIRouter(
    prefix="auth",
    tags=["auth"],
)


@router.post("/sign up")
async def register_user():
    pass


@router.post("/sign in")
async def login():
    pass


@router.post("/forgetpassword")
async def forget_password():
    pass
