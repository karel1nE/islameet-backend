from fastapi import FastAPI, HTTPException, Depends, Header, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SECRET_KEY = "key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    birthdayStamp = Column(Integer, nullable=True)
    photoURL = Column(String, nullable=True)
    description = Column(String, nullable=True)
    city = Column(String, nullable=True)
    isMale = Column(Boolean, nullable=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)  # Хэшированный пароль
    refreshToken = Column(String, nullable=True)

class ChatDB(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название чата
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID создателя чата

class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)  # ID чата
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID отправителя
    content = Column(String, nullable=False)  # Содержимое сообщения
    timestamp = Column(Integer, nullable=False, default=lambda: int(datetime.utcnow().timestamp()))  # Временная метка

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    id: Optional[int]
    email: EmailStr
    birthdayStamp: Optional[int] = None
    photoURL: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    isMale: Optional[bool] = None
    name: Optional[str] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    
class ChatCreate(BaseModel):
    name: str

class MessageCreate(BaseModel):
    chat_id: int
    content: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    token_data = decode_access_token(token)
    db_user = db.query(UserDB).filter(UserDB.email == token_data.email).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return db_user

@app.post("/token", tags=["AppAuth"], response_model=Token, operation_id="signIn")
async def sign_in(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/token", tags=["AppAuth"], operation_id="signUp")
async def sign_up(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserDB(
        email=user.email,
        birthdayStamp=user.birthdayStamp,
        photoURL=user.photoURL,
        description=user.description,
        city=user.city,
        isMale=user.isMale,
        name=user.name,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}

@app.get("/user", tags=["AppUser"], operation_id="getProfile")
async def get_profile(current_user: UserDB = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "birthdayStamp": current_user.birthdayStamp,
        "photoURL": current_user.photoURL,
        "description": current_user.description,
        "city": current_user.city,
        "isMale": current_user.isMale,
        "name": current_user.name,
    }

@app.put("/user", tags=["AppUser"], operation_id="updatePassword")
async def update_password(
    oldPassword: str = Query(...),
    newPassword: str = Query(...),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(oldPassword, current_user.password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")
    current_user.password = get_password_hash(newPassword)
    db.commit()
    return {"message": "Password updated successfully"}

@app.get("/user/{all}", tags=["AppUser"], operation_id="getAllProfiles")
async def get_all_profiles(all: str, db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

@app.post("/chat", tags=["AppChat"], operation_id="createChat")
async def create_chat(chat: ChatCreate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    new_chat = ChatDB(name=chat.name, creator_id=current_user.id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return {
        "id": new_chat.id,
        "name": new_chat.name,
        "creator_id": new_chat.creator_id,
        "message": "Chat created successfully"
    }

@app.post("/message", tags=["AppChat"], operation_id="sendMessage")
async def send_message(message: MessageCreate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(ChatDB).filter(ChatDB.id == message.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    new_message = MessageDB(
        chat_id=message.chat_id,
        sender_id=current_user.id,
        content=message.content,
        timestamp=int(datetime.utcnow().timestamp())
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {
        "id": new_message.id,
        "chat_id": new_message.chat_id,
        "sender_id": new_message.sender_id,
        "content": new_message.content,
        "timestamp": new_message.timestamp,
        "message": "Message sent successfully"
    }

@app.get("/chat/{chat_id}", tags=["AppChat"], operation_id="getChatMessages")
async def get_chat_messages(
    chat_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatDB).filter(ChatDB.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = db.query(MessageDB).filter(MessageDB.chat_id == chat_id).order_by(MessageDB.timestamp).all()
    return [
        {
            "id": message.id,
            "chat_id": message.chat_id,
            "sender_id": message.sender_id,
            "content": message.content,
            "timestamp": message.timestamp
        }
        for message in messages
    ]
