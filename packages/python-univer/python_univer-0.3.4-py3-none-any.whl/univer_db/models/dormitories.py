from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from univer_db.orm import get_base


Base = get_base()


class Dormitory(Base):
    """
    Модель "Общежитие"
    """
    __tablename__ = 'platonus_univer_dormitories'

    # Идентификатор
    id = Column('dormitoryID', Integer, primary_key=True)

    # Адрес общежития
    address = Column(String(256))

    # Статус
    status = Column(Integer)

    def __repr__(self):
        return '<Dormitory {} (id={} status={})>'.format(self, self.id, self.status)
    
    def __str__(self):
        return self.address


class DormitoryRoom(Base):
    """
    Модель "Комната общежития"
    """
    __tablename__ = 'univer_dormitory_rooms'

    # Идентификатор
    id = Column('dormitory_room_id', Integer, primary_key=True)

    # Общежитие
    dormitory_id = Column(ForeignKey('platonus_univer_dormitories.dormitoryID'))
    dormitory = relationship('Dormitory')

    # Этаж
    floor = Column('dormitory_room_floor', Integer)

    # Вместимость
    size = Column('dormitory_room_size', Integer)

    # Наименование
    number_ru = Column('dormitory_room_number_ru', String(30))
    number_kz = Column('dormitory_room_number_kz', String(30))
    number_en = Column('dormitory_room_number_en', String(30))

    # Статус
    status = Column(Integer)

    def __repr__(self):
        return '<DormitoryRoom {} (id={} dormitory_id={} floor={} size={} status={}>'.format(self, self.id, self.dormitory_id, self.floor, self.size, self.status)
    
    def __str__(self):
        return self.number_ru