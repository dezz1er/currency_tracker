from fastapi import APIRouter, HTTPException, status
from app.api.models.user import UserRegistration

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/register')
async def registration(userdata: UserRegistration,):
    if userdata.username in user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already exists'
        )
