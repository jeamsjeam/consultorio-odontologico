from src import app, db

#app._got_first_request
def create_tables():
    print("Creating database tables...")
    db.create_all()
    print("Done!")

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)