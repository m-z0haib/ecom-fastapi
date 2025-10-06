from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schema import User_Out, Create_User
from models import Users
from Authentication import hash_password, verify_password, create_new_token, admin_only
from fastapi.security import OAuth2PasswordRequestForm
get_db()

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/registeration", response_model=User_Out)
def user_registration(user: Create_User, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=404, detail="Username Already Exists")
    hashed_password = hash_password(user.user_password)
    new_user = Users(username = user.username, user_email = user.user_email, user_password = hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def user_login(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.user_email == from_data.username).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User Does Not Exists")
    if not verify_password(from_data.password, existing_user.user_password):
        raise HTTPException(status_code=404, detail="Invalid Password")
    new_token = create_new_token(user_data={"username": existing_user.username, "user_role": existing_user.user_role})
    return {"access_token": new_token, "token_type": "bearer"}

@router.get("/{user_id}", response_model=User_Out)
def view_profile(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User Do not Exist")
    return existing_user

@router.put("/{user_id}/role")
def update_role(user_id: int, new_role: str, db: Session = Depends(get_db)):
    user_roles = ["admin", "user"]
    if new_role not in user_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Role")
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not defined")
    user.user_role = new_role
    db.commit()
    db.refresh(user)
    return {"message": "User role is updated successfully"}

@router.delete('/{user_id}')
def delete_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found")
    db.delete(user)
    db.commit()

    return {"message":"User is deleted"}

@router.put("/{user_id}/profile")
def update_profile(user_id: int, new_email: str, new_ph: int, new_adrs: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not defined")
    user.user_address = new_adrs
    user.user_phone = new_ph
    user.user_email = new_email
    db.commit()
    db.refresh(user)
    return {"message": "User profile is updated successfully"}

