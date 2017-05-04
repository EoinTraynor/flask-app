import unittest

from flask_testing import TestCase

from app import create_app, db
from app.models import Employee

class TestBase(TestCase):

    def create_app(self):
        # pass in test config
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2017@localhost/flask_app_test'
        )

        return app

    def setUp(self)
    """
    Will be called before every test
    """
    db.create_all()

    # create test admin user
    admin = Employee(username="admin", password="admin2017", is_admin=True)