import unittest
import os

from flask_testing import TestCase
from flask import abort, url_for
from app import create_app, db
from app.models import Employee, Department, Role

class TestBase(TestCase):

    def create_app(self):
        # pass in test config
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2017@localhost/flask_app_test'
        )

        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

        # create test admin user
        admin = Employee(username="admin", password="admin2017", is_admin=True)

        # create test non-admin user
        employee = Employee(username="test_user", password="test2017")

        # save user to db
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):
    def test_employee_model(self):
        """
        Test number of records in Employee table
        """
        self.assertEqual(Employee.query.count(), 2)

    def test_department_model(self):
        """
        Test number of records in department
        """

        # create test department
        department = Department(name="IT", description="The IT Department")

        #save department to the db
        db.session.add(department)
        db.session.commit()

        self.assertEqual(Department.query.count(), 1)

    def test_role_model(self):
        """
        Test number of records of in Role table
        """

        # create test role
        role = Role(name="CEO", description="Runs the company")

        # insert role into db
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):
    def test_homepage_view(self):
        """
        Test that the homepage is accessable without login
        """

        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that the login view is accessable without login    
        """

        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_views(self):
        """
        Test that logout link is inaccessable without login
        and redirects to login page then to logout
        """

        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessable without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessable without login
        and redirects to login page the to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_departments_view(self):
        """
        Test that departments page is inaccessable without login
        and redirects to login page then to departments page
        """
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_roles_view(self):
        """
        Test that roles is inaccessable without login
        and redirects to login page then to roles
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_employees_view(self):
        """
        Test that employees page is inaccessable without login
        and redirects to login page then to employees
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):
    def test_403_forbidden(self):
        # create route to abort the request with the 403 error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)    
    
    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)    

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data) 

if __name__ == '__main__':
    unittest.main()