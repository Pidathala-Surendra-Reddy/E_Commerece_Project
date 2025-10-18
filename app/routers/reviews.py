from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import decode_access_token

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def get_current_user(authorization: str = Header(...), db: Session = Depends(database.get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(401, "Invalid token")
    user = db.query(models.User).filter(models.User.user_id == int(payload["user_id"])).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user

@router.post("/", response_model=schemas.ReviewOut)
def add_review(payload: schemas.ReviewCreate, user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    review = models.Review(user_id=user.user_id, product_id=payload.product_id,
                           rating=payload.rating, comment=payload.comment)
    db.add(review); db.commit(); db.refresh(review)
    return review

@router.get("/product/{product_id}", response_model=list[schemas.ReviewOut])
def get_reviews(product_id:int, db: Session = Depends(database.get_db)):
    return db.query(models.Review).filter(models.Review.product_id == product_id).all()
