from app.app import create_app

# Retrieve Flask app from app.py
app = create_app('development')

# Run application with debugging
if __name__ == '__main__':
    app.run(debug=True)