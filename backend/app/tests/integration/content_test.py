"""Integration tests for content related endpoints"""
import unittest
import json
import base64
from uuid import uuid4
from app import create_app
from app.extensions import DB as db
from app.tests.integration.base_test import BaseTestCase
from app.models.user import AdminUser
from bcrypt import hashpw, gensalt
from flask_jwt_extended import create_access_token

class ContentIntegrationTestCase(BaseTestCase):
    """Integration tests for content-related endpoints"""

    def setUp(self):
        """Set up test variables and initialize app"""
         # Create a temporary file to use as the database
        # Create an admin user
        super().setUp()
        # Create admin user
        admin_user = self.create_admin_user()
        db.session.add(admin_user)
        db.session.commit()
        self.admin_user_id = admin_user.id
        # Create regular user
        regular_user = self.create_regular_user()
        db.session.add(regular_user)
        db.session.commit()
        self.regular_user_id = regular_user.id
        # Create an editor user
        editor_user = self.create_editor_user()
        db.session.add(editor_user)
        db.session.commit()
        self.editor_user_id = editor_user.id

    def test_get_all_contents(self):
        """Test retrieving all contents"""
        # Seed some contents
        with self.app.app_context():
            from app.models.content import Content
            content1 = Content(
                id=str(uuid4()),
                title='Content 1',
                content='This is the first content.'
            )
            content2 = Content(
                id=str(uuid4()),
                title='Content 2',
                content='This is the second content.'
            )
            db.session.add_all([content1, content2])
            db.session.commit()

        headers = self.get_auth_headers(self.regular_user_id)
        response = self.client.get('/contents', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Contents retrieved successfully', data['message'])
        self.assertEqual(len(data['payload']), 2)

    def test_create_content_as_editor(self):
        """Test creating content as an editor"""
        headers = self.get_auth_headers(self.editor_user_id)
        response = self.client.post('/contents', headers=headers, json={
            'title': 'New Content',
            'content': 'This is new content.'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('Content created successfully', data['message'])
        self.assertEqual(data['payload']['title'], 'New Content')

    def test_create_content_as_regular_user(self):
        """Test creating content as a regular user (should fail)"""
        headers = self.get_auth_headers(self.regular_user_id)
        response = self.client.post('/contents', headers=headers, json={
            'title': 'Unauthorized Content',
            'content': 'Should not be allowed.'
        })
        self.assertEqual(response.status_code, 403)

    def test_get_content_by_id(self):
        """Test retrieving a content by ID"""
        # Seed a content
        with self.app.app_context():
            from app.models.content import Content
            content = Content(
                id=str(uuid4()),
                title='Sample Content',
                content='This is a sample content.'
            )
            db.session.add(content)
            db.session.commit()
            content_id = content.id

        headers = self.get_auth_headers(self.regular_user_id)
        response = self.client.get(f'/contents/{content_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Content retrieved successfully', data['message'])
        self.assertEqual(data['payload']['title'], 'Sample Content')

    def test_update_content_as_editor(self):
        """Test updating a content as an editor"""
        # Seed a content
        with self.app.app_context():
            from app.models.content import Content
            content = Content(
                id=str(uuid4()),
                title='Old Title',
                content='Old content.'
            )
            db.session.add(content)
            db.session.commit()
            content_id = content.id

        headers = self.get_auth_headers(self.editor_user_id)
        response = self.client.put(f'/contents/{content_id}', headers=headers, json={
            'title': 'Updated Title',
            'content': 'Updated content.'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Content updated successfully', data['message'])
        self.assertEqual(data['payload']['title'], 'Updated Title')

    def test_update_content_as_regular_user(self):
        """Test updating a content as a regular user (should fail)"""
        # Seed a content
        with self.app.app_context():
            from app.models.content import Content
            content = Content(
                id=str(uuid4()),
                title='Unchangeable Content',
                content='Content that should not be updated by regular users.'
            )
            db.session.add(content)
            db.session.commit()
            content_id = content.id

        headers = self.get_auth_headers(self.regular_user_id)
        response = self.client.put(f'/contents/{content_id}', headers=headers, json={
            'title': 'Attempted Update',
            'content': 'This update should fail.'
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_content_as_admin(self):
        """Test deleting a content as an admin"""
        # Seed a content
        with self.app.app_context():
            from app.models.content import Content
            content = Content(
                id=str(uuid4()),
                title='Delete Me',
                content='Content to be deleted.'
            )
            db.session.add(content)
            db.session.commit()
            content_id = content.id

        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.delete(f'/contents/{content_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Content deleted successfully', data['message'])

    def test_delete_content_as_regular_user(self):
        """Test deleting content as a regular user (should fail)"""
        # Seed a content
        with self.app.app_context():
            from app.models.content import Content
            content = Content(
                id=str(uuid4()),
                title='Protected Content',
                content='Regular users should not delete this.'
            )
            db.session.add(content)
            db.session.commit()
            content_id = content.id

        headers = self.get_auth_headers(self.regular_user_id)
        response = self.client.delete(f'/contents/{content_id}', headers=headers)
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()