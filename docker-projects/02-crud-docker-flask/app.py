from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from os import environ

# Configuración de Flask y SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo: Dueño
class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'vehicles': [vehicle.simple_json() for vehicle in self.vehicles]
        }

# Modelo: Vehículo
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    specifications = db.Column(db.JSON, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=True)

    def json(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'specifications': self.specifications or {},
            'owner': self.owner.json() if self.owner else None
        }

    def simple_json(self):
        return {'id': self.id, 'brand': self.brand, 'model': self.model}

# Inicialización de la base de datos
with app.app_context():
    db.create_all()

# Rutas CRUD para dueños
@app.route('/owners', methods=['POST'])
def create_owner():
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('email'):
            return make_response(jsonify({'message': 'Name and email are required'}), 400)
        new_owner = Owner(name=data['name'], email=data['email'])
        db.session.add(new_owner)
        db.session.commit()
        return make_response(jsonify({'message': 'Owner created', 'owner': new_owner.json()}), 201)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'Database error: {str(e)}'}), 500)

@app.route('/owners/<int:id>', methods=['GET'])
def get_owner(id):
    try:
        owner = Owner.query.get(id)
        if not owner:
            return make_response(jsonify({'message': 'Owner not found'}), 404)
        return make_response(jsonify({'owner': owner.json()}), 200)
    except Exception as e:
        return make_response(jsonify({'message': f'Error retrieving owner: {str(e)}'}), 500)

# Rutas CRUD para vehículos
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    try:
        data = request.get_json()
        if not data.get('brand') or not data.get('model') or not data.get('year'):
            return make_response(jsonify({'message': 'Brand, model, and year are required'}), 400)

        new_vehicle = Vehicle(
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            specifications=data.get('specifications'),
            owner_id=data.get('owner_id')
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return make_response(jsonify({'message': 'Vehicle created', 'vehicle': new_vehicle.json()}), 201)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'Database error: {str(e)}'}), 500)

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles = Vehicle.query.all()
        return make_response(jsonify([vehicle.json() for vehicle in vehicles]), 200)
    except Exception as e:
        return make_response(jsonify({'message': f'Error retrieving vehicles: {str(e)}'}), 500)

@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    try:
        vehicle = Vehicle.query.get(id)
        if not vehicle:
            return make_response(jsonify({'message': 'Vehicle not found'}), 404)

        data = request.get_json()
        vehicle.brand = data.get('brand', vehicle.brand)
        vehicle.model = data.get('model', vehicle.model)
        vehicle.year = data.get('year', vehicle.year)
        vehicle.specifications = data.get('specifications', vehicle.specifications)
        vehicle.owner_id = data.get('owner_id', vehicle.owner_id)
        db.session.commit()
        return make_response(jsonify({'message': 'Vehicle updated', 'vehicle': vehicle.json()}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'Database error: {str(e)}'}), 500)

# Ruta para borrar un vehículo
@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    try:
        vehicle = Vehicle.query.get(id)
        if not vehicle:
            return make_response(jsonify({'message': 'Vehicle not found'}), 404)

        db.session.delete(vehicle)
        db.session.commit()
        return make_response(jsonify({'message': 'Vehicle deleted'}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'Database error: {str(e)}'}), 500)

# Ruta de prueba
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'Test route works!'}), 200)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
