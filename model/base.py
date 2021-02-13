from app import db
from sqlalchemy.dialects.postgresql import UUID

class Base(db.Model):
    __abstract__ = True

    uid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    created_at = db.Column('created_at', db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True), default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def create(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()

    def update(self):
        db.session.commit()
        db.session.flush()

    def bulk_insert(self, data):
        db.session.bulk_insert_mappings(self, data)
        db.session.commit()
        db.session.flush()

    def last_updated_id(self, class_name):
        return db.session.query(class_name).order_by(class_name.id.desc()).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def merge(cls, obj):
        db.session.merge(obj)
        db.session.commit()
