# Flashcard DSA Project

This project is a Flashcard application designed to help users learn data structures and algorithms (DSA) through quizzes. The application features two user roles: an admin and a regular user.

## Features

- **User Roles**:
  - **Admin**: Can manage subjects and questions through an admin panel.
  - **Regular User**: Can select a subject for quizzes and view results after completing quizzes.

- **Quiz Functionality**:
  - Users can choose from various subjects.
  - Each quiz consists of multiple-choice questions with four options, one of which is correct.
  - Users receive immediate feedback on their performance after completing a quiz.

## Project Structure

The project is structured as follows:

```
flashcard_dsa_project
├── flashcard_app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations
│   │   └── __init__.py
│   ├── templates
│   │   └── flashcard_app
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── quiz.html
│   │       ├── result.html
│   │       ├── admin_panel.html
│   │       ├── add_subject.html
│   │       └── add_question.html
│   └── static
│       └── flashcard_app
│           └── styles.css
├── flashcard_dsa_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flashcard_dsa_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install django
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Usage

- **For Regular Users**: Navigate to the home page to select a subject and start the quiz.
- **For Admin Users**: Access the admin panel to add new subjects and questions.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.