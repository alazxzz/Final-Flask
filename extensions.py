from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app


# фласк миграции плюс сгл алчеми(доработать)


db = SQLAlchemy(app)
migrate = Migrate(app, db)