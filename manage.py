import sys
import unittest
from flask_script import Manager
from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand
from app import application, db, manager
from flask import Flask


# adds the python manage.py db init, db migrate, db upgrade commands
manager.add_command("db", MigrateCommand)
cli = FlaskGroup(application)

@cli.command('runserver')
def runserver():
    application.run(debug=True, host="0.0.0.0", port=5000)


@cli.command()
def runworker():
    application.run(debug=False)


@cli.command('recreate_db')
def recreate_db():
    """
    Recreates a database. This should only be used once
    when there's a new database instance. This shouldn't be
    used when you migrate your database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='moses', email="moses@gmail.com", fnmae="moses", lname="okemwa"))
    db.session.commit()

if __name__ == "__main__":
    cli()