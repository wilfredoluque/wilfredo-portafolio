from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from config import Config
from datetime import datetime

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/projects")
    def projects():
        return render_template("projects.html")

    @app.route("/fitness")
    def fitness():
        return render_template("fitness.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            nombre = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            if not nombre or not email or not message:
                flash("Completa todos los campos.", "danger")
                return redirect(url_for("contact"))

            try:
                msg = Message(
                    subject=f"Contacto desde Portafolio - {nombre}",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[app.config['MAIL_USERNAME']],
                    reply_to=email,
                    charset="utf-8"
                )
                msg.body = f"Nombre: {nombre}\nCorreo: {email}\nMensaje:\n{message}"
                mail.send(msg)
                flash("Mensaje enviado correctamente ✅", "success")
            except Exception as e:
                print("❌ Error enviando correo:", e)
                flash("Error enviando el mensaje. Revisa la configuración del correo.", "danger")

            return redirect(url_for("contact"))

        return render_template("contact.html")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

# ⚠ CREAR APP A NIVEL DE MÓDULO PARA GUNICORN
app = create_app()

# Solo correr localmente con Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
