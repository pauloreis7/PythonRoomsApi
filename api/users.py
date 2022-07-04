from typing import Optional, List
from fastapi import APIRouter, Path
from pydantic import BaseModel

users_router = APIRouter()

users = []

class User(BaseModel):
    """Users class attributes"""

    name: str
    email: str
    password: str
    bio: Optional[str]

@users_router.get('/users', response_model=List[User])
async def list_users():
    """Get all users list"""

    return users

@users_router.get('/users/{user_index}')
async def find_user(
    user_index: int = Path(..., description='User index to retrieve', gt=1)
):
    """Find a user"""

    user = users[user_index]

    return {'user': user}

@users_router.post('/users')
async def create_user(user: User):
    """Create a user"""

    users.append(user)

    return {'msg': True}
