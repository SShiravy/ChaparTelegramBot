from Models.user import User
from Models.delivery import Delivery
from sqlmodel import Session, select
from database import engine
from custom_logger import logger


def add_new_user(user:User) -> bool:
    try:
        with Session(engine) as db_session:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            logger.info(f"new user:{user} added to database")
    except Exception as e:
        logger.error(f"error on adding user:{user} to database, error:{e}")
        return False
    return True

def add_new_delivery(delivery:Delivery) -> bool:
    try:
        with Session(engine) as db_session:
            db_session.add(delivery)
            db_session.commit()
            db_session.refresh(delivery)
            logger.info(f"new delivery:{delivery} added to database")
    except Exception as e:
        logger.error(f"error on adding delivery:{delivery} to database, error:{e}")
        return False
    return True

def fetch_user_by_id(user_id:str)->User|None:
    try:
        with Session(engine) as db_session:
            user = db_session.exec(select(User).where(User.account_id == user_id)).one()
    except Exception as e:
        logger.error(f"error on fetching user:{user_id} from database, error:{e}")
        return None
    return user

def fetch_delivery_by_id(delivery_id:int)->Delivery|None:
    try:
        with Session(engine) as db_session:
            delivery = db_session.exec(select(Delivery).where(Delivery.id == delivery_id)).one()
    except Exception as e:
        logger.error(f"error on fetching delivery:{delivery_id} from database, error:{e}")
        return None
    return delivery


def update_user_in_db(user:User) -> bool:
    try:
        with Session(engine) as db_session:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            logger.info(f"user:{user} updated in database")
    except Exception as e:
        logger.error(f"error on updating user:{user} in database, error:{e}")
        return False
    return True

def update_delivery_in_db(delivery:Delivery) -> bool:
    try:
        with Session(engine) as db_session:
            db_session.add(delivery)
            db_session.commit()
            db_session.refresh(delivery)
            logger.info(f"delivery:{delivery} updated in database")
    except Exception as e:
        logger.error(f"error on updating delivery:{delivery} in database, error:{e}")
        return False
    return True

def get_user_deliveries(user_id:str):
    try:
        with Session(engine) as db_session:
            deliveries = db_session.exec(select(Delivery).where(Delivery.user_id == user_id)).all()
    except Exception as e:
        logger.error(f"error on getting user:{user_id} deliveries from database, error:{e}")
        return []
    return deliveries

