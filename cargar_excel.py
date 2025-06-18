import pandas as pd
from models import db, Equipo
from app import app

df = pd.read_excel("Tabla Equipos.xlsx")
df.columns = df.columns.str.strip()  # elimina espacios extra

print("Columnas encontradas:", df.columns.tolist())

with app.app_context():
    db.drop_all()
    db.create_all()

    for _, row in df.iterrows():
        equipo = Equipo(
            nombre=row['NOMBRE DE EQUIPO'],
            marca=row['MARCA'],
            modelo=row['MODELO'],
            serie=row['No. SERIE'],
            ubicacion=row['UBICACIÓN'],
            inventario=row['N° INVENTARIO NUEVO'],
            modalidad=row['MODALIDAD'],
            invima=row['INVIMA']
        )
        db.session.add(equipo)

    db.session.commit()
    print("✔ Base de datos creada y cargada con éxito")
