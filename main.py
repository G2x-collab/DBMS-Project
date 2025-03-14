import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from postgres.database import add_os, delete_virus, get_os_by_id, get_virus_by_id, update_os, update_virus, add_virus

app = Flask(__name__)

load_dotenv()
DB_URL = os.getenv("DB_URL")
print(DB_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Define database models
class Virus(db.Model):
    __tablename__ = 'virus'
    virus_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    discovery_date = db.Column(db.Date)
    attack_vector = db.Column(db.Text)
    spread_rate = db.Column(db.Float)
    infection_method = db.Column(db.Text)
    damage_potential = db.Column(db.Text)

    behaviors = db.relationship('Behavior', backref='virus', lazy=True)
    effects = db.relationship('Effect', backref='virus', lazy=True)

class Effect(db.Model):
    __tablename__ = 'effect'
    effect_id = db.Column(db.Integer, primary_key=True)
    virus_id = db.Column(db.Integer, db.ForeignKey('virus.virus_id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    data_loss_risk = db.Column(db.Boolean, nullable=False, default=False)
    system_instability_level = db.Column(db.String(50), nullable=False)
    network_disruption_potential = db.Column(db.Boolean, nullable=False, default=False)

class OperatingSystem(db.Model):
    __tablename__ = 'operating_system'
    os_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50))
    architecture = db.Column(db.String(50))
    vulnerability_score = db.Column(db.Float)

    devices = db.relationship('Device', backref='operating_system', lazy=True)

class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(100))
    os_id = db.Column(db.Integer, db.ForeignKey('operating_system.os_id'))
    status = db.Column(db.String(50))
    infection_count = db.Column(db.Integer, default=0)

class Behavior(db.Model):
    __tablename__ = 'behavior'
    behavior_id = db.Column(db.Integer, primary_key=True)
    virus_id = db.Column(db.Integer, db.ForeignKey('virus.virus_id'), nullable=False)
    action = db.Column(db.Text)
    impact_level = db.Column(db.String(50))
    persistence_method = db.Column(db.Text)
    stealth_techniques = db.Column(db.Text)
    execution_method = db.Column(db.Text)


# Route to display data
@app.route('/')
def index():
    try:
        viruses = Virus.query.all()
        print(type(viruses[0]))
        operating_systems = OperatingSystem.query.all()
        devices = Device.query.all()
        behaviors = Behavior.query.all()
        effects = Effect.query.all()

        print(f"Fetched {len(viruses)} viruses, {len(operating_systems)} OS, {len(devices)} devices, {len(effects)} effects")

        return render_template('index.html', 
                               viruses=viruses, 
                               operating_systems=operating_systems,
                               devices=devices, 
                               behaviors=behaviors, 
                               effects=effects)
    except Exception as e:
        print(f"🔥 ERROR: {e}")
        return "Database error. Check the terminal for logs."

@app.route('/add_os', methods=['GET', 'POST'])
def add_os_page():
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        architecture = request.form['architecture']
        vulnerability_score = request.form['vulnerability_score']

        add_os(name, version, architecture, vulnerability_score)
        return redirect(url_for('index'))

    return render_template('osadd.html')


# Add new virus page
@app.route('/add', methods=['GET', 'POST'])
def add_virus_page():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        discovery_date = request.form['discovery_date']
        attack_vector = request.form['attack_vector']
        spread_rate = request.form['spread_rate']
        infection_method = request.form['infection_method']
        damage_potential = request.form['damage_potential']

        add_virus(name, category, discovery_date, attack_vector, spread_rate, infection_method, damage_potential)
        return redirect(url_for('index'))

    return render_template('add.html')    

@app.route('/api/delete/<int:virus_id>', methods=['DELETE'])
def delete_virus_api(virus_id):
    try:
        delete_virus(virus_id)  # Call the function
        return jsonify({"message": "Virus deleted successfully", "virus_id": virus_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 


if __name__ == '__main__':
    print("🚀 Server starting... Visit http://127.0.0.1:5000/")
    app.run(debug=True, host="0.0.0.0", port=5000)
