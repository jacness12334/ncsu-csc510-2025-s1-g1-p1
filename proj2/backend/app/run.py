from app.app import get_app

app = get_app('development')

if __name__ == '__main__':
    app.run(debug=True)