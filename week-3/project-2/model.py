from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
    db.app = app
    db.init_app(app)
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.String(255))

    def __repr__(self):
        return f"<{self.id}: {self.title}"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.desc,
        }
