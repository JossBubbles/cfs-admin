from db.connect import Base, engine


from db.template.user import User


def create_database():
    Base.metadata.create_all(bind = engine)
    print("✅ Tablas creadas correctamente")