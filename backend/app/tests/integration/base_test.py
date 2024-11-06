"""Base test case for all test cases"""
import base64
import unittest
import os
import tempfile
from uuid import uuid4

from bcrypt import gensalt, hashpw
from app import create_app
from app.extensions import DB as db
from app.models.user import AdminUser, EditorUser, RegularUser

class BaseTestCase(unittest.TestCase):
    """Base TestCase that other test cases will inherit from"""

    def setUp(self):
        """Set up test variables and initialize app"""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Teardown all initialized variables."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        # Close and remove the temporary database
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def get_auth_headers(self, user_id):
        """Helper method to get authentication headers"""
        with self.app.app_context():
            from flask_jwt_extended import create_access_token
            access_token = create_access_token(identity=user_id)
        return {
            'Authorization': f'Bearer {access_token}'
        }
    
    def create_admin_user(self):
        """Create an admin user"""
        password_bytes = 'adminpass'.encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        admin_user = AdminUser(
            username=f'adminuser_{str(uuid4())}',
            password_hash=hashed_password_str,
            first_name='Admin',
            middle_name='',
            last_name='User',
            email=f'admin_{str(uuid4())}@example.com',
            phone_number='',
        )
        admin_user.id = str(uuid4())
        return admin_user
    
    def create_regular_user(self):
        """Create a regular user"""
        password_bytes = 'userpass'.encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        regular_user = RegularUser(
            username=f'testuser_{str(uuid4())}',
            password_hash=hashed_password_str,
            first_name='Test',
            middle_name='',
            last_name='User',
            email=f'testuser_{str(uuid4())}@example.com',
            phone_number=''
        )
        regular_user.id = str(uuid4())
        return regular_user
    
    def create_editor_user(self):
        """Create editor user"""
        password_bytes = 'editorpass'.encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        editor_user = EditorUser(
            username=f'editoruser_{str(uuid4())}',
            password_hash=hashed_password_str,
            first_name='Editor',
            middle_name='',
            last_name='User',
            email=f'editor_{str(uuid4())}@example.com',
            phone_number=''
        )
        editor_user.id = str(uuid4())
        return editor_user
