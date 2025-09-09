# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    selected= Earthquake.query.filter_by(id=id).first()
    if selected:
        response_body= {
                "id":selected.id,
                "location":selected.location,
                "magnitude":selected.magnitude,
                "year":selected.year
                }
        status_code=200
    else:
        response_body={
            "message": f"Earthquake {id} not found."
                }
        status_code=404
        
    return make_response(jsonify(response_body),status_code)

@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_magnitude(magnitude):
    selected= Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if selected:
        response_body={
            "count": len(selected),
            "quakes":[quake.to_dict() for quake in selected]
        }
        status_code= 200
    else:
        response_body={
            "count": 0,
            "quakes": []
        }
        status_code= 200
    return make_response(jsonify(response_body), status_code)
if __name__ == '__main__':
    app.run(port=5555, debug=True)
