import sqlalchemy as sa
from sqlalchemy import Identity

from src.db.database import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'user'

    id = sa.Column(sa.BigInteger, Identity(always=True, cache=5), primary_key=True)
    first_name = sa.Column(sa.VARCHAR(100), unique=False)
    last_name = sa.Column(sa.VARCHAR(100), unique=False)
    phone_number = sa.Column(sa.Text, unique=False)
    email = sa.Column(sa.VARCHAR(70), unique=True)
    balance = sa.Column(sa.DECIMAL, server_default="0")
    username = sa.Column(sa.VARCHAR(70), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f"User ({self.telegram_id} - {self.full_name})"
