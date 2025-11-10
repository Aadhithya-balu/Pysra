# Models package initialization
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance is created here to avoid circular imports.
# Import this `db` from model modules and initialize it with the Flask
# app in `app.py` using `db.init_app(app)`.
db = SQLAlchemy()
