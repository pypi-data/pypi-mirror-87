from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from univer_db.orm import get_base


Base = get_base()


class User(Base):
    """
    Модель "Пользователи"
    Статус: Выполняется
    """

    __tablename__ = 'univer_users'

    # Идентификатор
    id = Column('user_id', Integer, primary_key=True)

    # Логин
    username = Column('user_login', String(50))

    def __repr__(self):
        return '<User {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.username


class Student(Base):
    """
    Модель "Студенты"
    Статус: Выполняется
    """

    __tablename__ = 'univer_students'

    # Идентификатор
    id = Column('students_id', Integer, primary_key=True)

    # Пользователь
    user_id = Column('user_id', ForeignKey('univer_users.user_id'))
    user = relationship('User')

    # Статус
    status = Column('status', Integer)

    # Дата регистрации
    reg_date = Column('student_reg_date', DateTime)

    # Ступень обучения
    stage_id = Column(ForeignKey('univer_stage.stage_id'))
    stage = relationship('Stage')

    # Уровень обучения
    edu_level_id = Column('edu_levels_id', ForeignKey('univer_edu_levels.edu_level_id'))
    edu_level = relationship('EduLevel')

    # Форма обучения
    education_form_id = Column(ForeignKey('univer_education_form.education_form_id'))
    education_form = relationship('EducationForm')

    # Тип поступления
    enrollment_type_id = Column(ForeignKey('univer_enrollment_type.enrollment_type_id'))
    enrollment_type = relationship('EnrollmentType')

    # Пол
    sex = Column('students_sex', Integer)

    # Дата рождения
    birth_date = Column('students_birth_date', DateTime)

    # ФИО студента
    last_name = Column('students_sname', String(100))
    first_name = Column('students_name', String(100))
    middle_name = Column('students_father_name', String(100))

    # Фамилия и Имя студента транслитом
    last_name_translit = Column('students_sname_intern', String(100))
    first_name_translit = Column('students_name_intern', String(100))

    # Электронная почта
    email = Column('students_email', String(25))

    # Документ
    document_identity_type_id = Column('students_document_identity_type', ForeignKey('univer_document_identity.document_identity_type'))
    document_identity_type = relationship('DocumentIdentity')
    document_identity_number = Column('students_document_identity_number', String(50))
    document_identity_date = Column('students_document_identity_date', DateTime)
    document_identity_issued = Column('students_document_identity_issued', String(100))

    # ИИН студента
    identify_code = Column('students_identify_code', String(50))

    # Данные об окончании учебного заведения перед поступлением в университет
    graduate_info_id = Column(ForeignKey('univer_graduate_info.graduate_info_id'))
    graduate_info = relationship('GraduateInfo')

    # Факультет
    faculty_id = Column(ForeignKey('univer_faculty.faculty_id'))
    faculty = relationship('Faculty')

    # ОП
    speciality_id = Column(ForeignKey('univer_speciality.speciality_id'))
    speciality = relationship('Speciality')

    # Год начала действия учебного плана
    educ_plan_adm_year = Column(Integer)

    def __repr__(self):
        return '<Student {} (id={} user={} status={})>'.format(self, self.id, self.user_id, self.status)
    
    def __str__(self):
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class Personnel(Base):
    """
    Модель "Сотрудники"
    Статус: Выполняется
    """

    __tablename__ = 'univer_personal'

    # Идентификатор
    id = Column('personal_id', Integer, primary_key=True)

    # Пользователь
    user_id = Column('user_id', ForeignKey('univer_users.user_id'))
    user = relationship('User')

    # Статус
    status = Column('status', Integer)

    # ФИО персонала
    last_name = Column('personal_sname', String(200))
    first_name = Column('personal_name', String(100))
    middle_name = Column('personal_father_name', String(100))

    # Фамилия и Имя персонала транслитом
    last_name_translit = Column('personal_translit_sname', String(100))
    first_name_translit = Column('personal_translit_name', String(100))

    # Электронная почта
    work_email = Column('personal_work_email', String(50))

    # ИИН сотрудника
    identify_code = Column('personal_identification_number', String(150))

    def __repr__(self):
        return '<Personnel {} (id={} user={} status={})>'.format(self, self.user_id, self.status)
    
    def __str__(self):
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class Teacher(Base):
    """
    Модель "Преподаватели"
    Статус: Выполняется
    """

    __tablename__ = 'univer_teacher'

    # Идентификатор
    id = Column('teacher_id', Integer, primary_key=True)

    # Сотрудник
    personnel_id = Column('personal_id', ForeignKey('univer_personal.personal_id'))
    personnel = relationship('Personnel')

    # Статус
    status = Column('status', Integer)

    def __repr__(self):
        return '<Teacher {} (id={} personnel={} status={})>'.format(self, self.id, self.personnel_id, self.status)
    
    def __str__(self):
        return str(self.personnel)