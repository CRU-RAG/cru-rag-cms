"""Integration tests for user related endpoints"""

import json
import unittest
from app.extensions import DB as db
from app.tests.integration.base_test import BaseTestCase


class UserIntegrationTestCase(BaseTestCase):
    """Integration tests for user-related endpoints"""

    def setUp(self):
        """Set up test variables and initialize app"""
        super().setUp()
        admin_user = self.create_admin_user()
        db.session.add(admin_user)
        db.session.commit()
        self.admin_user_id = admin_user.id

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post(
            "/register",
            json={
                "username": "testuser",
                "password": "testpass",
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@example.com",
            },
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("User registered successfully", data["message"])

    def test_user_login(self):
        """Test user login endpoint"""
        # Register a user first
        self.test_user_registration()
        # Then attempt to log in
        response = self.client.post(
            "/login", json={"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data["payload"])
        self.user_access_token = data["payload"]["access_token"]

    def test_get_users_as_admin(self):
        """Test getting user list as an admin"""
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.get("/users", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("Users retrieved successfully", data["message"])

    def test_get_users_as_regular_user(self):
        """Test getting user list as a regular user (should fail)"""
        self.test_user_login()
        headers = {"Authorization": f"Bearer {self.user_access_token}"}
        response = self.client.get("/users", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_create_user_as_admin(self):
        """Test creating a new user as an admin"""
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.post(
            "/users",
            headers=headers,
            json={
                "username": "newuser",
                "password": "newpass",
                "first_name": "New",
                "last_name": "User",
                "email": "newuser@example.com",
                "role": "regular",
            },
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("User created successfully", data["message"])

    def test_create_user_as_regular_user(self):
        """Test creating a new user as a regular user (should fail)"""
        self.test_user_login()
        headers = {"Authorization": f"Bearer {self.user_access_token}"}
        response = self.client.post(
            "/users",
            headers=headers,
            json={
                "username": "anotheruser",
                "password": "anotherpass",
                "first_name": "Another",
                "last_name": "User",
                "email": "anotheruser@example.com",
                "role": "regular",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_get_user_by_id_as_admin(self):
        """Test getting a user by ID as an admin"""
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.get(f"/users/{self.admin_user_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("User retrieved successfully", data["message"])

    def test_delete_user_as_admin(self):
        """Test deleting a user as an admin"""
        # Create a new user to delete
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.post(
            "/users",
            headers=headers,
            json={
                "username": "todelete",
                "password": "deletepass",
                "first_name": "To",
                "last_name": "Delete",
                "email": "todelete@example.com",
                "role": "regular",
            },
        )
        data = json.loads(response.data)
        user_id = data["payload"]["id"]
        # Delete the user
        response = self.client.delete(f"/users/{user_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("User deleted successfully", data["message"])

    def test_update_user_role_as_admin(self):
        """Test updating a user's role as an admin"""
        # Create a regular user
        headers = self.get_auth_headers(self.admin_user_id)
        response = self.client.post(
            "/users",
            headers=headers,
            json={
                "username": "rolechange",
                "password": "changepass",
                "first_name": "Role",
                "last_name": "Change",
                "email": "rolechange@example.com",
                "role": "regular",
            },
        )
        data = json.loads(response.data)
        user_id = data["payload"]["id"]
        # Update user's role to editor
        response = self.client.put(
            f"/users/{user_id}", headers=headers, json={"role": "editor"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("User role updated successfully", data["message"])
        self.assertEqual(data["payload"]["role"], "editor")


if __name__ == "__main__":
    unittest.main()
