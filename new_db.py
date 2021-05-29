from affiliate_store import db

db.drop_all()
db.create_all()
db.session.commit()
