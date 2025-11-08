'''
Devices repository
'''

from . import db
from sqlalchemy.dialects.postgresql import ARRAY


class Device(db.Model):
    __tablename__ = "devices"

    address = db.Column(db.String(), primary_key=True, nullable=False)
    provider = db.Column(db.String(), primary_key=True, nullable=False)
    protocol = db.Column(db.String(), primary_key=True, nullable=False)
    kind = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)
    serialnum = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    tags = db.Column(ARRAY(db.String(), dimensions=1))
