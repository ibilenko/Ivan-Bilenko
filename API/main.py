from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import crud,models,schemas
from database import SessionLocal, engine
create_engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class worker:
    db_string = "postgresql://postgres:sjvnfi_LFMR740@internal.cfnsbden5utu.us-east-2.rds.amazonaws.com:5432/"
    engine = create_engine(db_string, pool_size=10, max_overflow=20)
    acc = crud.init(engine)
    driver = crud.entrance(acc, engine)

def check() -> bool:
    try:
        driver.execute_script("window.scrollTo(0,0)", "")
        df = pd.read_sql(f"select status from link.acc_info where acc_name = 'Ivan Bilenko")
        if df.empty:
            raise NameError(f'Отсутсвует статус по аккаунту {worker.acc.name}')
        elif df['status'][0] == 'work':
            return False
        else:
            return True
    except:
        worker.driver = crud.entrance(worker.acc, worker.engine)
        return True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/send")
def create_user(data:schemas.SendPackage,db: Session = Depends(get_db)):
    if check():
        execute.engine.connect(f"update link.acc_info set 'work'  where acc_name = 'Ivan Bilenko")
    try:
        crud.send_message(data.client_name, data.message, worker.driver)
        execute.engine.connect(f"update link.acc_info set 'free'  where acc_name = 'Ivan Bilenko")
    except:
        return {'failed'}
    # if check():
    #     worker.engine.connect.execute(f"update link.acc_info set status = 'send_message' where acc_name = {worker.acc.name}")
    #     if crud.send_message(data.client_name,data.message,worker.driver):
    #         worker.engine.connect.execute(f"update link.acc_info set status = 'free' where acc_name = {worker.acc.name}")
    #         return {'succes'}
    # else:
    #     return {'acc_busy'}


@app.get("/update")
def create_user(db: Session = Depends(get_db)):
    try:
        crud.parsing_unread_message(worker.acc,worker.driver,worker.engine)
    except:
        return {'succes'}

print(worker.acc,worker.driver,worker.engine)

