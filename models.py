"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cupcake(db.Model):

    __tablename__ = 'cupcake'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    flavor = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, nullable=False, default="https://tinyurl.com/demo-cupcake")

    def serialize(self):
        """Returns a dict representation of cupcake which we can turn into JSON."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
    
    def __repr__(self):
        """Better representation of the object."""
        return f"<Cupcake id={self.id} flavor={self.flavor} size={self.size} rating={self.rating}>"

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
