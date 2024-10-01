from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine

app = Flask(__name__)

# Setup the connection to the database
db = SQLAlchemy()   
db_uri = create_engine('mysql://root:movie123@database:3306/movies')
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

try:
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
except Exception as e:
    print(f"Error connecting to the database: {e}")

def get_movies():
    """
    Retrieves all movies from the database.
    """
    movies = []
    with db.engine.begin() as conn:
        for row in conn.execute(text("SELECT * FROM movies")).fetchall():
            movies.append({"name": row[0], "rating": row[1]})

    print(f"Retrieved {len(movies)} movies from the database.")
    return movies

def render_movie_li(movies):
    """
    Creates a HTML list (<li>) of all movies.
    """
    html = ""
    for movie in movies:
        html += f"""
            <li class="list-group-item">
                <span class="badge">{movie["rating"]}
                    <span class="glyphicon glyphicon-star"></span>
                </span>
                {movie["name"]}
            </li>
        """
    return html

@app.route("/")
def index():
    """
    This method is called upon opening the webapp.
    """
    movies = get_movies()
    movies_li = render_movie_li(movies)

    # Read the index.html and add the movies_li to it.
    try:
        with open("index.html") as f:
            return f.read() % (movies_li)
    except FileNotFoundError:
        return "Error: index.html not found.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
