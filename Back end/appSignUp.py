import eel

eel.init('web')  # Specify the directory containing your HTML, CSS, and JS files

@eel.expose
def signup():
    # Handle signup logic here
    # Example: This function would typically interact with a database or backend service
    print("Sign up functionality executed")

@eel.expose
def showLogin():
    eel.load_page('signin.html')  # Redirect to login page

eel.start('signup.html', size=(600, 700))  # Start with the signup.html page
