"""Integration tests for user related endpoints"""
import os
import tempfile
import unittest
import base64
from app import create_app
from app.extensions import DB as db
from flask import json
from flask_jwt_extended import create_access_token


class UserIntegrationTestCase(unittest.TestCase):
    """Integration tests for user-related endpoints"""

    def setUp(self):
        """Set up test variables and initialize app"""
        # Create a temporary file to use as the database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create an admin user
            from app.models.user import AdminUser
            from uuid import uuid4
            from bcrypt import hashpw, gensalt
            password_bytes = 'adminpass'.encode('utf-8')
            hashed_password = hashpw(password_bytes, gensalt())
            hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
            admin_user = AdminUser(
                username='adminuser',
                password_hash=hashed_password_str,
                first_name='Admin',
                middle_name='',
                last_name='User',
                email='admin@example.com',
                phone_number='',
            )
            admin_user.id = str(uuid4())
            db.session.add(admin_user)
            db.session.commit()
            self.admin_user_id = admin_user.id

    def tearDown(self):
        """Teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        # Close and remove the temporary database
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def get_auth_headers(self, user_id):
        """Helper method to get authentication headers"""
        with self.app.app_context():
            access_token = create_access_token(identity=user_id)
        return {
            'Authorization': f'Bearer {access_token}'
        }

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('User registered successfully', data['message'])

    def test_user_login(self):
        """Test user login endpoint"""
        # Register a user first
        self.test_user_registration()
        # Then attempt to log in
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data['payload'])
        self.user_access_token = data['payload']['access_token']

    def test_get_users_as_admin(self):
        """Test getting user list as an admin"""
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.get('/users', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Users retrieved successfully', data['message'])

    def test_get_users_as_regular_user(self):
        """Test getting user list as a regular user (should fail)"""
        self.test_user_login()
        headers = {'Authorization': f'Bearer {self.user_access_token}'}
        response = self.client.get('/users', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_create_user_as_admin(self):
        """Test creating a new user as an admin"""
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.post('/users', headers=headers, json={
            'username': 'newuser',
            'password': 'newpass',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'role': 'regular'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('User created successfully', data['message'])

    def test_create_user_as_regular_user(self):
        """Test creating a new user as a regular user (should fail)"""
        self.test_user_login()
        headers = {'Authorization': f'Bearer {self.user_access_token}'}
        response = self.client.post('/users', headers=headers, json={
            'username': 'anotheruser',
            'password': 'anotherpass',
            'first_name': 'Another',
            'last_name': 'User',
            'email': 'anotheruser@example.com',
            'role': 'regular'
        })
        self.assertEqual(response.status_code, 403)

    def test_get_user_by_id_as_admin(self):
        """Test getting a user by ID as an admin"""
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.get(f'/users/{self.admin_user_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('User retrieved successfully', data['message'])

    def test_delete_user_as_admin(self):
        """Test deleting a user as an admin"""
        # Create a new user to delete
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.post('/users', headers=headers, json={
            'username': 'todelete',
            'password': 'deletepass',
            'first_name': 'To',
            'last_name': 'Delete',
            'email': 'todelete@example.com',
            'role': 'regular'
        })
        data = json.loads(response.data)
        user_id = data['payload']['id']
        # Delete the user
        response = self.client.delete(f'/users/{user_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('User deleted successfully', data['message'])

    def test_update_user_role_as_admin(self):
        """Test updating a user's role as an admin"""
        # Create a regular user
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.post('/users', headers=headers, json={
            'username': 'rolechange',
            'password': 'changepass',
            'first_name': 'Role',
            'last_name': 'Change',
            'email': 'rolechange@example.com',
            'role': 'regular'
        })
        data = json.loads(response.data)
        user_id = data['payload']['id']
        # Update user's role to editor
        response = self.client.put(f'/users/{user_id}', headers=headers, json={
            'role': 'editor'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('User role updated successfully', data['message'])
        self.assertEqual(data['payload']['role'], 'editor')

if __name__ == '__main__':
    unittest.main()