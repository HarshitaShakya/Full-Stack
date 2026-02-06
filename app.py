from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Employee Model
class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Employee {self.name}>"

# Create database
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        desc = request.form.get("desc")

        employee = Employee(name=name, email=email, desc=desc)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for("home"))

    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    employee = Employee.query.filter_by(sno=sno).first()

    if request.method == "POST":
        employee.name = request.form["name"]
        employee.email = request.form["email"]
        db.session.commit()
        return redirect("/")

    return render_template("update.html", employee=employee)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8069)

