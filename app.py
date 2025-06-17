from flask import Flask, render_template, request, redirect, session, url_for
from models import db, Equipo, Usuario
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Asegúrate de que sea en la raíz
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_supersecreta'
db.init_app(app)

# ✅ Crear automáticamente la base de datos en Render
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    filtro_ubicacion = request.args.get('ubicacion')
    filtro_modalidad = request.args.get('modalidad')

    query = Equipo.query
    if filtro_ubicacion:
        query = query.filter(Equipo.ubicacion.ilike(f'%{filtro_ubicacion}%'))
    if filtro_modalidad:
        query = query.filter(Equipo.modalidad.ilike(f'%{filtro_modalidad}%'))

    equipos = query.all()
    ubicaciones = sorted(set(e.ubicacion for e in Equipo.query.all() if e.ubicacion))
    modalidades = sorted(set(e.modalidad for e in Equipo.query.all() if e.modalidad))

    return render_template('index.html', equipos=equipos, logged_in='user' in session,
                           ubicaciones=ubicaciones, modalidades=modalidades)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        equipo = Equipo(
            nombre=request.form['nombre'],
            marca=request.form['marca'],
            modelo=request.form['modelo'],
            serie=request.form['serie'],
            ubicacion=request.form['ubicacion'],
            inventario=request.form['inventario'],
            modalidad=request.form['modalidad'],
            invima=request.form['invima']
        )
        db.session.add(equipo)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('registrar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    equipo = Equipo.query.get_or_404(id)

    if request.method == 'POST':
        equipo.nombre = request.form['nombre']
        equipo.marca = request.form['marca']
        equipo.modelo = request.form['modelo']
        equipo.serie = request.form['serie']
        equipo.ubicacion = request.form['ubicacion']
        equipo.inventario = request.form['inventario']
        equipo.modalidad = request.form['modalidad']
        equipo.invima = request.form['invima']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar.html', equipo=equipo)

if __name__ == '__main__':
    app.run(debug=True)
