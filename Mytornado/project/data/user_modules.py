from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .connect import Base, session


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(50))
    creatime = Column(DateTime, default=datetime.now)
    _locked = Column(Boolean, default=False, nullable=False)

    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return session.query(cls).filter_by(id=id).all()

    @classmethod
    def by_name(cls, name):
        return session.query(cls).filter_by(username=name).all()

    @property
    def locked(self):
        return self._locked

    def __repr__(self):
        return "<User (id='%s',username='%s',password='%s',creatime='%s',_locked_='%s')>" % (
            self.id,
            self.username,
            self.password,
            self.creatime,
            self._locked
        )


if __name__ == '__main__':
    Base.metadata.create_all()  # 如果模型存在，重复执行也不会再次更新数据表模型
