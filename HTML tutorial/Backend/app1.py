from flask import Flask

# Create a Flask app instance 
app = Flask(__name__)
# Define a route and a view function
@app.route('/')
def hello():
   return 'Hello, World!'
# Run the app if this file is executed
if __name__  ==  '__main__':# type: ignore
   app.run(debug=True)



