from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session

# Common database dependency
def get_db(session: Session = Depends(get_session)) -> Session:
    return session