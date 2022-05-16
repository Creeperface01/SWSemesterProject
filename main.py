from app import app

app.run(debug=True, host='0.0.0.0')

# from flask import Flask
#
# app = Flask(__name__)
# app.config['TESTING'] = True
#
#
# @app.route('/')
# def index():
#     print('request')
#     return 'Hello, my name is Jan Bednar'
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=80)
