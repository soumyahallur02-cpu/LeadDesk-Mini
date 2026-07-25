from io import StringIO

from flask import Flask, Response, render_template, request, redirect, flash, url_for
import csv
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config
from models import db, Lead, Admin

app = Flask(__name__)
app.config.from_object(Config)



db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


with app.app_context():

    db.create_all()

    if not Admin.query.filter_by(username="admin").first():

        admin = Admin(
            username="admin",
            password=generate_password_hash("admin123")
        )

        db.session.add(admin)
        db.session.commit()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    email = request.form.get("email")
    budget = request.form.get("budget")
    message = request.form.get("message")

    # Server-side validation
    if not name or not email or not budget or not message:
        flash("Please fill all the fields.", "error")
        return redirect("/")

    new_lead = Lead(
        name=name,
        email=email,
        budget=budget,
        message=message
    )

    db.session.add(new_lead)
    db.session.commit()

    flash("Lead submitted successfully!", "success")
    return redirect("/")
@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect("/admin")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            login_user(admin)

            flash("Login Successful!", "success")

            return redirect("/admin")

        flash("Invalid Username or Password", "error")

    return render_template("login.html")
@app.route("/admin")
@login_required
def admin():

    search = request.args.get("search", "")

    if search:
        leads = Lead.query.filter(
            (Lead.name.contains(search)) |
            (Lead.email.contains(search))
        ).all()
    else:
        leads = Lead.query.order_by(
            Lead.created_at.desc()
        ).all()

    total = Lead.query.count()
    new = Lead.query.filter_by(status="New").count()
    contacted = Lead.query.filter_by(status="Contacted").count()
    closed = Lead.query.filter_by(status="Closed").count()

    return render_template(
        "admin.html",
        leads=leads,
        total=total,
        new=new,
        contacted=contacted,
        closed=closed,
        search=search
    )

@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update_status(id):

    lead = Lead.query.get_or_404(id)

    lead.status = request.form["status"]

    db.session.commit()

    flash("Status Updated Successfully!", "success")

    return redirect("/admin")


@app.route("/delete/<int:id>")
@login_required
def delete_lead(id):

    lead = Lead.query.get_or_404(id)

    db.session.delete(lead)

    db.session.commit()

    flash("Lead Deleted Successfully!", "success")

    return redirect("/admin")
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("login"))

@app.route("/export")
@login_required
def export_csv():

    leads = Lead.query.order_by(Lead.created_at.desc()).all()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Name",
        "Email",
        "Budget",
        "Message",
        "Status",
        "Created At"
    ])

    for lead in leads:
        writer.writerow([
            lead.id,
            lead.name,
            lead.email,
            lead.budget,
            lead.message,
            lead.status,
            lead.created_at
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=leads.csv"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)