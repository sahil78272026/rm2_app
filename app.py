# ==============================================================
# 🟢 SIMPLE FLASK MVP  (uses Flask‑SQLAlchemy ORM, no patterns)
# ==============================================================
# • One file: app.py  → copy‑paste and run.
# • Three tiny HTML templates embedded via render_template_string.
# • Database: SQLite via ORM (gated.db).
# ==============================================================

from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime, os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gated.db'
app.config['SECRET_KEY'] = 'change-me'

db = SQLAlchemy(app)

# ---------------- ORM MODELS ----------------
class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'))
    flat = db.relationship('Flat')

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    visiting_flat = db.Column(db.String(10), nullable=False)
    purpose = db.Column(db.String(200))
    approved = db.Column(db.Boolean, default=False)
    requested_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# create tables once
with app.app_context():
    db.create_all()

# ---------------- HTML TEMPLATES ----------------
HOME_HTML = """
<h1>Gated Society MVP (ORM)</h1>
<ul>
  <li><a href='/add_flat'>Register Flat</a></li>
  <li><a href='/add_resident'>Register Resident</a></li>
  <li><a href='/add_visitor'>Guard: Add Visitor</a></li>
</ul>
<h2>Pending Visitors per Flat</h2>
{% for f in flats %}
  <p>Flat {{f.number}} – <a href='/pending/{{f.number}}'>View</a></p>
{% endfor %}
"""

ADD_FLAT_HTML = """
<h2>Add Flat</h2>
<form method='post'>
  Flat Number: <input name='number' required>
  <button>Save</button>
</form>
<a href='/'>Home</a>
"""

ADD_RESIDENT_HTML = """
<h2>Add Resident</h2>
<form method='post'>
  Name: <input name='name' required><br>
  Flat:
  <select name='flat_id'>
    {% for f in flats %}<option value='{{f.id}}'>{{f.number}}</option>{% endfor %}
  </select>
  <button>Save</button>
</form>
<a href='/'>Home</a>
"""

ADD_VISITOR_HTML = """
<h2>Guard – Add Visitor</h2>
<form method='post'>
  Name: <input name='name' required><br>
  Contact: <input name='contact' required><br>
  Visiting Flat: <input name='visiting_flat' required><br>
  Purpose: <input name='purpose'><br>
  <button>Save</button>
</form>
<a href='/'>Home</a>
"""

PENDING_HTML = """
<h2>Pending Visitors for Flat {{flat}}</h2>
{% if visitors %}
  <ul>
  {% for v in visitors %}
    <li>{{v.name}} – {{v.purpose}} <a href='/approve/{{v.id}}/{{flat}}'>Approve</a></li>
  {% endfor %}
  </ul>
{% else %}
  <p>No pending visitors.</p>
{% endif %}
<a href='/'>Home</a>
"""

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    flats = Flat.query.order_by(Flat.number).all()
    return render_template_string(HOME_HTML, flats=flats)

@app.route('/add_flat', methods=['GET', 'POST'])
def add_flat():
    if request.method == 'POST':
        if not Flat.query.filter_by(number=request.form['number'].upper()).first():
            db.session.add(Flat(number=request.form['number'].upper()))
            db.session.commit()
        return redirect(url_for('home'))
    return render_template_string(ADD_FLAT_HTML)

@app.route('/add_resident', methods=['GET', 'POST'])
def add_resident():
    flats = Flat.query.order_by(Flat.number).all()
    if request.method == 'POST':
        db.session.add(Resident(name=request.form['name'], flat_id=request.form['flat_id']))
        db.session.commit()
        return redirect(url_for('home'))
    return render_template_string(ADD_RESIDENT_HTML, flats=flats)

@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        v = Visitor(name=request.form['name'], contact=request.form['contact'],
                     visiting_flat=request.form['visiting_flat'].upper(), purpose=request.form['purpose'])
        db.session.add(v); db.session.commit()
        return redirect(url_for('home'))
    return render_template_string(ADD_VISITOR_HTML)

@app.route('/pending/<flat>')
def pending(flat):
    visitors = Visitor.query.filter_by(visiting_flat=flat.upper(), approved=False).all()
    return render_template_string(PENDING_HTML, visitors=visitors, flat=flat)

@app.route('/approve/<int:vid>/<flat>')
def approve(vid, flat):
    v = Visitor.query.get_or_404(vid)
    v.approved = True
    db.session.commit()
    return redirect(url_for('pending', flat=flat))

if __name__ == '__main__':
    app.run(debug=True)
