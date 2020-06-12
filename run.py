from app import create_app, db
app = create_app(env='prod')
if __name__ == "__main__":
    db.create_all()
