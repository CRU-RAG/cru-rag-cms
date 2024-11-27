"""Integration tests for comment-related endpoints"""

import unittest
import json
from app.models.content import Content
from app.extensions import DB as db
from app.tests.integration.base_test_class import BaseTestCase


class CommentIntegrationTestCase(BaseTestCase):
    """Integration tests for comment-related endpoints"""

    def setUp(self):
        """Set up test variables and initialize app"""
        super().setUp()
        with self.app.app_context():
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
            # Create another regular user
            another_user = self.create_regular_user()
            db.session.add(another_user)
            db.session.commit()
            self.another_user_id = another_user.id
            # Create content
            content = Content(title="Test Content", body="Content for testing.")
            db.session.add(content)
            db.session.commit()
            self.content_id = content.id

    def create_comment(self):
        """Helper method to create comment"""
        headers = self.get_auth_headers(self.regular_user_id)
        response = self.client.post(
            "/comments",
            headers=headers,
            json={
                "content_id": self.content_id,
                "comment_text": "This is a test comment.",
            },
        )
        data = json.loads(response.data)
        self.comment_id = data["payload"]["id"]

    def test_create_comment(self):
        """Test creating a comment"""
        with self.client:
            headers = self.get_auth_headers(self.regular_user_id)
            response = self.client.post(
                "/comments",
                headers=headers,
                json={
                    "content_id": self.content_id,
                    "comment_text": "This is a test comment.",
                },
            )
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertIn("Comment created successfully", data["message"])
            self.assertEqual(data["payload"]["comment_text"], "This is a test comment.")
            self.assertEqual(data["payload"]["user_id"], self.regular_user_id)
            self.comment_id = data["payload"]["id"]

    def test_update_comment_by_owner(self):
        """Test updating a comment by the owner"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.regular_user_id)
            response = self.client.put(
                f"/comments/{self.comment_id}",
                headers=headers,
                json={"comment_text": "Updated comment text."},
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("Comment updated successfully", data["message"])
            self.assertEqual(data["payload"]["comment_text"], "Updated comment text.")

    def test_update_comment_by_non_owner(self):
        """Test updating a comment by a non-owner (should fail)"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.another_user_id)
            response = self.client.put(
                f"/comments/{self.comment_id}",
                headers=headers,
                json={"comment_text": "Malicious update."},
            )
            self.assertEqual(response.status_code, 403)

    def test_delete_comment_by_owner(self):
        """Test deleting a comment by the owner"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.regular_user_id)
            response = self.client.delete(
                f"/comments/{self.comment_id}", headers=headers
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("Comment deleted successfully", data["message"])

    def test_delete_comment_by_non_owner(self):
        """Test deleting a comment by a non-owner (should fail)"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.another_user_id)
            response = self.client.delete(
                f"/comments/{self.comment_id}", headers=headers
            )
            self.assertEqual(response.status_code, 403)

    def test_delete_comment_by_admin(self):
        """Test deleting a comment by an admin"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.admin_user_id)
            response = self.client.delete(
                f"/comments/{self.comment_id}", headers=headers
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("Comment deleted successfully", data["message"])

    def test_get_content_with_comments(self):
        """Test retrieving a content with its comments"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.regular_user_id)
            response = self.client.get(f"/contents/{self.content_id}", headers=headers)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("Content retrieved successfully", data["message"])
            self.assertEqual(len(data["payload"]["comments"]), 1)
            self.assertEqual(
                data["payload"]["comments"][0]["comment_text"],
                "This is a test comment.",
            )

    def test_get_all_contents_with_comments(self):
        """Test retrieving all contents with their comments"""
        with self.client:
            # First, create a comment
            self.create_comment()
            headers = self.get_auth_headers(self.regular_user_id)
            response = self.client.get("/contents", headers=headers)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("Contents retrieved successfully", data["message"])
            self.assertGreaterEqual(len(data["payload"]), 1)
            content = next(
                (item for item in data["payload"] if item["id"] == self.content_id),
                None,
            )
            self.assertIsNotNone(content)
            self.assertEqual(len(content["comments"]), 1)
            self.assertEqual(
                content["comments"][0]["comment_text"], "This is a test comment."
            )


if __name__ == "__main__":
    unittest.main()
