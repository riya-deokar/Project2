from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import re

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        if not self.validate_password(password):
            raise ValueError("Password does not meet the security requirements")
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_email(email):
        # Regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        return False

    @staticmethod
    def validate_password(password):
        # Minimum eight characters, at least one letter, one number and one special character:
        regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.fullmatch(regex, password)

    @classmethod
    def create_user(cls, email, password):
        if not cls.validate_email(email):
            raise ValueError("Invalid email format")
        user = cls(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user