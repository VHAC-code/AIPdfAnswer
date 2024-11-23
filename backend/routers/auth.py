from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from pydantic import BaseModel  # type: ignore
from auth import get_db, get_password_hash, create_access_token, authenticate_user, blacklist_token, oauth2_scheme, SECRET_KEY, ALGORITHM, blacklisted_tokens
from models import User
from jose import JWTError, jwt  # Import JWTError and jwt for decoding

router = APIRouter()

# Request and response schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully!"}

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Generate access token
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout/")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode the token to extract the user information
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        # Verify the user exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found for the provided token",
            )
        # Blacklist the token
        if token not in blacklisted_tokens:
            blacklist_token(token)
        return {"message": "Logged out successfully!"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

