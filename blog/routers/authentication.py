from fastapi import APIRouter

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)
@router.post('/login')
def login():
    return 'login'
