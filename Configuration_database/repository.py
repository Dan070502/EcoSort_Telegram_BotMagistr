from sqlalchemy import insert, select, update, delete, or_, and_
from sqlalchemy.orm import Session
from Configuration_database.database_model import engine, garbage_applications, users
import datetime

print(engine)


class SQL:
    session = Session(engine)

    def garbage_app_insert(self,
                           address: str, longtitude: float, latitude: float,
                           user_id: int, photo: bytearray, det_photo: bytearray, date: datetime):
        ins = insert(garbage_applications).values(
            address=address,
            longtitude=longtitude,
            latitude=latitude,
            user_id=user_id,
            photo=photo,
            detected_photo=det_photo,
            date=date
        )
        self.session.execute(ins)
        self.session.commit()

    def users_insert(self, username: str, tid: int):
        ins = insert(users).values(
            username=username,
            tid=tid
        )
        self.session.execute(ins)
        self.session.commit()

    def users_select(self, tid: int):
        sel = select(users).where(users.c.tid == tid)
        return self.session.execute(sel).first()

    def add_number(self, number: str, tid: int):
        up = update(users).values(number=number).where(users.c.tid == tid)
        self.session.execute(up)
        self.session.commit()

    def count_applications(self, tid: int):
        count = self.session.query(garbage_applications).where(garbage_applications.c.user_id == tid).count()
        return count

    def get_last_garbage_id_by_userid(self, user_id: int):
        last = self.session.query(garbage_applications.c.id).filter(garbage_applications.c.user_id == user_id).order_by(garbage_applications.c.id.desc()).first()
        return last[0]

    def get_all_garbage_by_userid(self, user_id: int):
        all = self.session.query(garbage_applications.c.id, garbage_applications.c.address, garbage_applications.c.date, garbage_applications.c.status).filter(garbage_applications.c.user_id == user_id).all()
        return all

    def get_all_username(self):
        usernames = self.session.query(users.c.username, users.c.tid).all()
        return usernames

    def update_status_garbage(self, id: int, new_status: str):
        s = update(garbage_applications).values(status=new_status).where(garbage_applications.c.id == id)
        self.session.execute(s)
        self.session.commit()

    def get_garbage_by_id(self, id: int):
        s = select(garbage_applications).where(garbage_applications.c.id == id)
        return self.session.execute(s).first()

    def get_role(self, id: int):
        s = select(users.c.role).where(users.c.tid == id)
        return self.session.execute(s).first()

    def get_all_coordinates(self):
        s = select(garbage_applications.c.latitude, garbage_applications.c.longtitude)
        return self.session.execute(s).all()

    def get_active_app_coordinates(self):
        s = select(garbage_applications.c.latitude, garbage_applications.c.longtitude, garbage_applications.c.id, garbage_applications.c.detected_photo, garbage_applications.c.status, garbage_applications.c.address, garbage_applications.c.date).where(
            or_(garbage_applications.c.status == "Выполняется 🔸", garbage_applications.c.status == "Рассматривается", garbage_applications.c.status == "Рассматривается 🔁")
        )
        return self.session.execute(s).all()

    def get_active_app_coordinates_user(self, user_id):
        s = select(garbage_applications.c.latitude, garbage_applications.c.longtitude, garbage_applications.c.id, garbage_applications.c.detected_photo, garbage_applications.c.status, garbage_applications.c.address, garbage_applications.c.date).where(
            and_(garbage_applications.c.user_id == user_id, or_(garbage_applications.c.status == "Выполняется 🔸", garbage_applications.c.status == "Рассматривается", garbage_applications.c.status == "Рассматривается 🔁"))
        )
        return self.session.execute(s).all()


if __name__ == '__main__':
    sql = SQL()

