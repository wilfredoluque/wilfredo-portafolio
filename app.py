from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from config import Config
from datetime import datetime

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    # Esto mantiene la fecha actual disponible en las plantillas
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # ===== RUTAS =====

    @app.route("/")
    def index():
        projects_data = [
            {"title":"Demo 1","desc":"Proyecto demo","img":"projects/p1.jpg"},
            {"title":"Demo 2","desc":"Proyecto demo","img":"projects/p2.jpg"},
            {"title":"Demo 3","desc":"Proyecto demo","img":"projects/p3.jpg"},
        ]
        return render_template("index.html", projects=projects_data)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/projects")
    def projects():
        projects_data = [
            {"title":"Proyecto A","desc":"Descripción corta","img":"projects/p1.jpg"},
            {"title":"Proyecto B","desc":"Descripción corta","img":"projects/p2.jpg"},
            {"title":"Proyecto C","desc":"Descripción corta","img":"projects/p3.jpg"},
        ]
        return render_template("projects.html", projects=projects_data)

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
                    sender=app.config['MAIL_DEFAULT_SENDER'],   # IMPORTANTE: usar sender fijo
                    recipients=[app.config['MAIL_USERNAME']],   # tu correo real
                    reply_to=email,
                    charset="utf-8"
                )
                msg.body = f"Nombre: {nombre}\nCorreo: {email}\nMensaje:\n{message}"

                # Enviar el correo
                mail.send(msg)

                flash("Mensaje enviado correctamente ✅", "success")
            except Exception as e:
                # Imprime error real en consola para depuración
                print("❌ Error enviando correo:", e)
                flash("Error enviando el mensaje. Revisa la configuración del correo.", "danger")

            return redirect(url_for("contact"))

        return render_template("contact.html")

    # ===== ERROR 404 =====
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

# ===== RUN APP =====
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
