from typing import Optional, List

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    """Users class attributes"""

    name: str
    email: str
    password: str
    bio: Optional[str]

@app.get('/users', response_model=List[User])
async def list_users():
    """Get all users list"""

    return users

@app.get('/users/{user_index}')
async def find_user(
    user_index: int = Path(..., description='User index to retrieve', gt=1),
    query: str = Query(None, max_length=5)
):
    """Find user"""

    user = users[user_index]

    return {'user': user, 'query': query}

@app.post('/users')
async def create_user(user: User):
    """Create a user"""

    users.append(user)

    return {'msg': True}
