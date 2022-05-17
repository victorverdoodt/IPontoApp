from app import app

app.secret_key = '<SOMETHING_SUPER_SECRET>'

if __name__ == '__main__':
    app.run(debug=True)
