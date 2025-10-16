# Import necessary modules from Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os

# --- Basic Flask App Setup ---
app = Flask(__name__)

# Security configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
csrf = CSRFProtect(app)

# --- Database Configuration ---

# Define a base class for declarative models
class Base(DeclarativeBase):
    pass

# Configure the database URI. Creates books.db in the project folder
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# Initialize the SQLAlchemy extension, linking it to our Flask app and model base class
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# --- Define the Database Model (Table) ---

# The Book class represents the 'book' table in our database.
# It inherits from db.Model, which gives it SQLAlchemy's ORM (Object Relational Mapper) capabilities.
class Book(db.Model):
    # Each attribute represents a column in the table.
    # Mapped[*] defines the data type for the column in Python.
    # mapped_column(*) sets the database column type and constraints.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


# --- Create the Database Table ---

# This block ensures that the table defined above is created in the database file.
# It needs an 'application context' to know which Flask app's configuration to use.
with app.app_context():
    db.create_all()


# --- Application Routes ---

# The home route ('/') displays all books in the library.
@app.route('/')
def home():
    # READ ALL RECORDS
    # 1. Construct a query to select all records from the Book table, ordered by title.
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # 2. .scalars() gets the individual Book objects from the query result. .all() fetches them as a list.
    all_books = result.scalars().all()
    # 3. Render the index.html template, passing the list of books to be displayed.
    return render_template("index.html", books=all_books)


# The '/add' route allows users to add a new book to the library.
# It accepts both GET (to show the form) and POST (to submit the form) requests.
@app.route("/add", methods=["GET", "POST"])
def add():
    # This block runs only when the user submits the form (a POST request).
    if request.method == "POST":
        # Validate form data
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        rating_str = request.form.get("rating", "").strip()
        
        # Check for missing fields
        if not title or not author or not rating_str:
            flash("All fields are required.", "error")
            return render_template("add.html")
        
        # Validate rating
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                flash("Rating must be between 0 and 10.", "error")
                return render_template("add.html")
        except ValueError:
            flash("Rating must be a valid number.", "error")
            return render_template("add.html")
        
        # Check for duplicate title
        existing_book = db.session.execute(db.select(Book).where(Book.title == title)).scalar_one_or_none()
        if existing_book:
            flash("A book with this title already exists.", "error")
            return render_template("add.html")
        
        # CREATE A NEW RECORD
        try:
            new_book = Book(
                title=title,
                author=author,
                rating=rating
            )
            # Add the new_book object to the database session.
            db.session.add(new_book)
            # Commit the session to permanently save the changes to the database.
            db.session.commit()
            flash("Book added successfully!", "success")
            # Redirect the user back to the home page to see the new book.
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding the book.", "error")
            return render_template("add.html")
    
    # If it's a GET request, just show the add.html page with the form.
    return render_template("add.html")


# The '/edit' route allows users to update a book's rating.
@app.route("/edit", methods=["GET", "POST"])
def edit():
    # This block runs when the user submits the rating change form.
    if request.method == "POST":
        # UPDATE THE RECORD
        # 1. Get the book's ID from the hidden input in the form.
        book_id = request.form.get("id")
        if not book_id:
            flash("Invalid book ID.", "error")
            return redirect(url_for('home'))
            
        # 2. Fetch the corresponding book from the database.
        book_to_update = db.get_or_404(Book, book_id)
        
        # Validate rating
        rating_str = request.form.get("rating", "").strip()
        if not rating_str:
            flash("Rating is required.", "error")
            return render_template("edit_rating.html", book=book_to_update)
        
        try:
            # 3. Update the rating with the new value from the form.
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                flash("Rating must be between 0 and 10.", "error")
                return render_template("edit_rating.html", book=book_to_update)
            book_to_update.rating = rating
        except ValueError:
            flash("Rating must be a valid number.", "error")
            return render_template("edit_rating.html", book=book_to_update)

        try:
            # 4. Commit the change to the database.
            db.session.commit()
            flash("Rating updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the rating.", "error")
        
        # 5. Redirect to the home page.
        return redirect(url_for('home'))

    # This block runs when the user clicks the "Edit Rating" link (a GET request).
    # 1. Get the book's ID from the URL query string (e.g., /edit?id=1).
    book_id = request.args.get('id')
    if not book_id:
        flash("Invalid book ID.", "error")
        return redirect(url_for('home'))
    # 2. Fetch the book from the database.
    book_selected = db.get_or_404(Book, book_id)
    # 3. Render the editing page, passing in the selected book's data.
    return render_template("edit_rating.html", book=book_selected)


# The '/delete' route removes a book from the library.
# Changed to POST method for security
@app.route("/delete", methods=["POST"])
def delete():
    # 1. Get the book's ID from the form data.
    book_id = request.form.get('id')
    if not book_id:
        flash("Invalid book ID.", "error")
        return redirect(url_for('home'))
    
    # 2. Find the book by its ID.
    book_to_delete = db.get_or_404(Book, book_id)
    
    try:
        # 3. Delete the record from the session.
        db.session.delete(book_to_delete)
        # 4. Commit the deletion to the database.
        db.session.commit()
        flash(f"'{book_to_delete.title}' has been deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the book.", "error")
    
    # 5. Redirect to the home page.
    return redirect(url_for('home'))


# This allows the script to be run directly. debug=True enables auto-reloading on code changes.
if __name__ == "__main__":
    app.run(debug=True)