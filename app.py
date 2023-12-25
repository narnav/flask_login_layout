from flask import Flask, render_template, request, redirect, url_for
import json

api = Flask(__name__)

users = [
    # {"userName": "itay", "pwd": "123"},
    # {"userName": "maya", "pwd": "123"},
    # {"userName": "itzik", "pwd": "123"}
]

# Load users from the JSON file
file_path = 'users.json'
try:
    with open(file_path, 'r') as file:
        users = json.load(file)
except:print("file not exist - all good")


@api.route('/')
def hello():
    return render_template("main.html") 

@api.route('/test')
def test():
    return render_template("main.html") 

@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print(username ,password)
        # Check if username and password match
        for user in users:
            if user['userName'] == username and user['pwd'] == password:
                # Here you might set up a session for the logged-in user
                # For simplicity, let's just redirect to a success page
                return redirect(url_for('success',user=username))
        
        # If the loop finishes without finding a matching user, show an error
        error = 'Invalid credentials. Please try again.'
        return render_template("login.html", error=error)

    # If it's a GET request, render the login form
    return render_template("login.html")

@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password =request.form['password']  # Assuming password is an integer

        # Check if the username already exists
        for user in users:
            if user['userName'] == new_username:
                error = 'Username already exists. Please choose a different one.'
                return render_template("register.html", error=error)

        # If the username doesn't exist, create a new user entry
        users.append({"userName": new_username, "pwd": new_password})
        with open(file_path, 'w') as file:
            json.dump(users, file)
        # Redirect to a success page or login page
        return redirect(url_for('login'))

    # If it's a GET request, render the registration form
    return render_template("register.html")

@api.route('/success/<user>')
def success(user=""):
    return f"Login Successful! {user}"

if __name__ == '__main__':
    api.run(debug=True)
