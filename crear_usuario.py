from models import db, Usuario
from werkzeug.security import generate_password_hash
from flask import Flask

# Configurar la app temporalmente solo para este script
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear el usuario dentro del contexto de la app
with app.app_context():
    username = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ").strip()

    # Encriptar la contraseña
    hashed = generate_password_hash(password)

    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(username=username).first():
        print("❌ El usuario ya existe.")
    else:
        nuevo_usuario = Usuario(username=username, password=hashed)
        db.session.add(nuevo_usuario)
        db.session.commit()
        print("✅ Usuario creado exitosamente.")
