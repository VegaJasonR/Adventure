Adventure Project

Description
This Flask application combines user authentication and adventure management features. Users can register, login, view their dashboard, view specific users, add, update, mark as completed/not completed, and delete adventures. The application includes password hashing for secure authentication using bcrypt.

Installation
Clone the repository
git clone https://github.com/your_repository.git

Install the required dependencies
pip install -r requirements.txt

Usage
Run the Flask application
flask run

Access the application in your browser at http://localhost:5000

Routes
Homepage (/): Displays the homepage.
User Registration (/register): Allows users to register.
User Login (/login): Handles user login functionality.
User Dashboard (/dashboard): Displays user details and adventures.
View a Specific User (/users/<int:id>): Shows specific user details and adventures.
User Logout (/logout): Logs the user out and clears the session.
Models
User: Manages user-related operations.
Adventure: Handles adventure-related operations.
Dependencies
Flask
Flask-Bcrypt
Contributing
Contributions are welcome. Feel free to fork the repository and submit pull requests.
