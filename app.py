from flask import Flask

from flask_migrate import Migrate


from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


with app.app_context():
    from models import db
    db.init_app(app)
    migrate = Migrate(app, db)

