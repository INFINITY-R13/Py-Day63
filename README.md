# Flask Book Library

A secure and user-friendly web application for managing a personal book library built with Flask, SQLAlchemy, and SQLite.

## Features

- ✅ **Add Books**: Add new books with title, author, and rating (0-10)
- ✅ **View Library**: Browse all books in a clean, organized interface
- ✅ **Edit Ratings**: Update book ratings with validation
- ✅ **Delete Books**: Safely remove books with confirmation dialogs
- ✅ **Security**: CSRF protection on all forms
- ✅ **Validation**: Comprehensive input validation and error handling
- ✅ **Flash Messages**: User-friendly success and error notifications
- ✅ **Responsive Design**: Mobile-friendly interface

## Technology Stack

- **Backend**: Flask 3.1.2
- **Database**: SQLite with SQLAlchemy 2.0.44 ORM
- **Security**: Flask-WTF 1.2.2 for CSRF protection
- **Frontend**: HTML5, CSS3, JavaScript
- **Python**: Compatible with Python 3.14+

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Py-Day63
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure

```
Py-Day63/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── books.db               # SQLite database (created automatically)
└── templates/
    ├── index.html         # Home page template
    ├── add.html           # Add book form template
    └── edit_rating.html   # Edit rating form template
```

## Usage

### Adding a Book
1. Click "Add New Book" on the home page
2. Fill in the book title, author, and rating (0-10)
3. Click "Add Book" to save

### Editing a Rating
1. Click "Edit Rating" next to any book
2. Enter the new rating (0-10)
3. Click "Update Rating" to save changes

### Deleting a Book
1. Click "Delete" next to any book
2. Confirm the deletion in the popup dialog
3. The book will be permanently removed

## Security Features

- **CSRF Protection**: All forms include CSRF tokens to prevent cross-site request forgery
- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protects against SQL injection
- **Secure Delete**: Delete operations require POST requests and confirmation

## Database Schema

### Book Table
| Column | Type    | Constraints                    |
|--------|---------|--------------------------------|
| id     | Integer | Primary Key, Auto-increment    |
| title  | String  | Unique, Not Null, Max 250 chars |
| author | String  | Not Null, Max 250 chars       |
| rating | Float   | Not Null, Range 0-10          |

## Development

### Environment Variables
- `SECRET_KEY`: Set this in production for session security
  ```bash
  export SECRET_KEY="your-secret-key-here"
  ```

### Running in Development
The application runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error pages
- Debug toolbar

### Production Deployment
For production deployment:
1. Set `SECRET_KEY` environment variable
2. Set `debug=False` in `main.py`
3. Use a production WSGI server like Gunicorn
4. Consider using PostgreSQL instead of SQLite for better performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Python learning curriculum (Day 63) and is intended for educational purposes.

## Requirements

- Python 3.14+
- Flask 3.1.2
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.44
- Flask-WTF 1.2.2

## Changelog

### Latest Version
- ✅ Added CSRF protection to all forms
- ✅ Implemented comprehensive input validation
- ✅ Added flash messaging system
- ✅ Improved error handling with database rollbacks
- ✅ Enhanced UI with responsive design
- ✅ Added confirmation dialogs for delete operations
- ✅ Updated to latest dependency versions
- ✅ Added duplicate title prevention
- ✅ Improved form persistence on validation errors