import os
import random
from unittest import TestCase

from django.test import Client
from string import ascii_letters, printable

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get("USER_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")


# Create your tests here.
class UserAuthTestCase(TestCase):
    def test_register_exist_user(self):
        client = Client()
        req = client.post(
            "/api/v1/register/",
            {"username": USERNAME, "password": USER_PASSWORD},
        )
        self.assertDictEqual(
            req.json(),
            {"username": ["Пользователь с таким именем уже существует."]},
        )
        assert req.status_code != 404

    def test_user(self):
        client = Client()
        letters = printable.replace(" \t\n\r\v\f", "")

        username = "".join(random.choice(ascii_letters) for _ in range(10))
        password = "".join(random.choice(letters) for _ in range(12))

        req = client.post(
            "/api/v1/register/",
            {"username": username, "password": password},
        )

        res = req.json()
        assert res != {
            "username": ["Пользователь с таким именем уже существует."]
        }

        login = client.post(
            "/api/v1/token/", {"username": username, "password": password}
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        token = login_res["access"]
        headers = {"Authorization": f"Bearer {token}"}
        uid = None

        for i in client.get("/api/v1/users/").json():
            if i["username"] == username:
                uid = i["id"]
                break
        else:
            self.assertIsNotNone(uid)

        req = client.delete(
            f"/api/v1/users/{uid}/",
            headers=headers,
        )

        self.assertEqual(req.status_code, 204)


class TaskStatusTestCase(TestCase):
    def setUp(self):
        self.client = Client(headers={"Content-Type": "application/json"})
        login = self.client.post(
            "/api/v1/token/",
            {"username": USERNAME, "password": USER_PASSWORD},
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        self.headers = {"Authorization": f'Bearer {login_res["access"]}'}
        self.status_name = "".join(
            random.choice(ascii_letters) for _ in range(12)
        )

    def Test_create(self):
        client = self.client

        req = client.post(
            "/api/v1/task-status/",
            {
                "name": str(self.status_name),
            },
            headers=self.headers,
        )
        res = req.json()

        self.assertEqual(req.status_code, 201)
        self.assertIn("name", res)
        self.assertEqual(self.status_name, res["name"])

        self.status_id = res["id"]

    def Test_change(self):
        client = self.client
        new_name = "".join(random.choice(ascii_letters) for _ in range(12))
        print(new_name)
        req = client.patch(
            f"/api/v1/task-status/{int(self.status_id)}/",
            {"name": str(new_name)},
            headers=self.headers,
            content_type="application/json",
        )
        print(req.json())
        self.assertEqual(req.status_code, 200)

        req = client.patch(
            f"/api/v1/task-status/{int(self.status_id)}/",
            {
                "name": str(self.status_name),
            },
            headers=self.headers,
            content_type="application/json",
        )

        self.assertEqual(req.status_code, 200)

    def Test_delete(self):
        client = self.client

        req = client.delete(
            f"/api/v1/task-status/{self.status_id}/",
            headers=self.headers,
        )

        self.assertEqual(req.status_code, 204)

    def test_status(self):
        self.Test_create()
        self.Test_change()
        self.Test_delete()


class TaskPriorityTestCase(TestCase):
    def setUp(self):
        self.client = Client(headers={"Content-Type": "application/json"})
        login = self.client.post(
            "/api/v1/token/",
            {"username": USERNAME, "password": USER_PASSWORD},
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        self.headers = {"Authorization": f'Bearer {login_res["access"]}'}
        self.priority_name = "".join(
            random.choice(ascii_letters) for _ in range(12)
        )

    def Test_create(self):
        client = self.client

        req = client.post(
            "/api/v1/task-priority/",
            {
                "name": str(self.priority_name),
            },
            headers=self.headers,
        )
        res = req.json()

        self.assertEqual(req.status_code, 201)
        self.assertIn("name", res)
        self.assertEqual(self.priority_name, res["name"])

        self.status_id = res["id"]

    def Test_change(self):
        client = self.client
        new_name = "".join(random.choice(ascii_letters) for _ in range(12))
        req = client.patch(
            f"/api/v1/task-priority/{int(self.status_id)}/",
            {"name": str(new_name)},
            headers=self.headers,
            content_type="application/json",
        )
        self.assertEqual(req.status_code, 200)

        req = client.patch(
            f"/api/v1/task-priority/{int(self.status_id)}/",
            {
                "name": str(self.priority_name),
            },
            headers=self.headers,
            content_type="application/json",
        )

        self.assertEqual(req.status_code, 200)

    def Test_delete(self):
        client = self.client

        req = client.delete(
            f"/api/v1/task-priority/{self.status_id}/",
            headers=self.headers,
        )

        self.assertEqual(req.status_code, 204)

    def test_priority(self):
        self.Test_create()
        self.Test_change()
        self.Test_delete()


class RoleTestCase(TestCase):
    def setUp(self):
        self.client = Client(headers={"Content-Type": "application/json"})
        login = self.client.post(
            "/api/v1/token/",
            {"username": USERNAME, "password": USER_PASSWORD},
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        self.headers = {"Authorization": f'Bearer {login_res["access"]}'}
        self.role_name = "".join(
            random.choice(ascii_letters) for _ in range(12)
        )

    def Test_create(self):
        client = self.client

        req = client.post(
            "/api/v1/roles/",
            {
                "name": str(self.role_name),
            },
            headers=self.headers,
        )
        res = req.json()

        self.assertEqual(req.status_code, 201)
        self.assertIn("name", res)
        self.assertEqual(self.role_name, res["name"])

        self.status_id = res["id"]

    def Test_change(self):
        client = self.client
        new_name = "".join(random.choice(ascii_letters) for _ in range(12))
        req = client.patch(
            f"/api/v1/roles/{int(self.status_id)}/",
            {"name": str(new_name)},
            headers=self.headers,
            content_type="application/json",
        )
        self.assertEqual(req.status_code, 200)

        req = client.patch(
            f"/api/v1/roles/{int(self.status_id)}/",
            {
                "name": str(self.role_name),
            },
            headers=self.headers,
            content_type="application/json",
        )

        self.assertEqual(req.status_code, 200)

    def Test_delete(self):
        client = self.client

        req = client.delete(
            f"/api/v1/roles/{self.status_id}/",
            headers=self.headers,
        )

        self.assertEqual(req.status_code, 204)

    def test_role(self):
        self.Test_create()
        self.Test_change()
        self.Test_delete()


class TaskCommentTestCase(TestCase):
    def setUp(self):
        self.client = Client(headers={"Content-Type": "application/json"})
        login = self.client.post(
            "/api/v1/token/",
            {"username": USERNAME, "password": USER_PASSWORD},
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        self.headers = {"Authorization": f'Bearer {login_res["access"]}'}
        self.comment_task = "".join(
            random.choice(ascii_letters) for _ in range(12)
        )

        self.project = self.client.post(
            "/api/v1/projects/",
            {"title": "title", "status": "active"},
            headers=self.headers,
        ).json()

        self.task = self.client.post(
            "/api/v1/tasks/",
            {
                "title": "title",
                "project": self.project["id"],
                "status": 1,
                "priority": 1,
            },
            headers=self.headers,
        ).json()

    def Test_create(self):
        client = self.client

        req = client.post(
            "/api/v1/comments/",
            {
                "task": self.task["id"],
                "author": 1,
                "text": "text",
            },
            headers=self.headers,
        )

        self.assertEqual(req.status_code, 201)
        self.comment = req.json()

    def Test_update(self):
        client = self.client

        req = client.patch(
            f'/api/v1/comments/{self.comment["id"]}/',
            {"text": "new_text"},
            content_type="application/json",
            headers=self.headers,
        )
        print(req.json())
        self.assertEqual(req.json()["text"], "new_text")

    def Test_delete(self):
        client = self.client

        req = client.delete(
            f'/api/v1/comments/{self.comment["id"]}/', headers=self.headers
        )

        self.assertEqual(req.status_code, 204)

    def test_comments(self):
        self.Test_create()
        self.Test_update()
        self.Test_delete()

    def tearDown(self):
        self.client.delete(
            f'/api/v1/projects/{self.project["id"]}/', headers=self.headers
        )


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client(headers={"Content-Type": "application/json"})
        login = self.client.post(
            "/api/v1/token/",
            {"username": USERNAME, "password": USER_PASSWORD},
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        self.headers = {"Authorization": f'Bearer {login_res["access"]}'}
        self.project_name = "".join(
            random.choice(ascii_letters) for _ in range(12)
        )

    def Test_create(self):
        client = self.client

        req = client.post(
            "/api/v1/projects/",
            {"title": self.project_name, "status": "active"},
            headers=self.headers,
        )
        res = req.json()

        self.assertEqual(req.status_code, 201)

        self.project = res

    def Test_update(self):
        client = self.client

        req = client.patch(
            f"/api/v1/projects/{self.project['id']}/",
            {"title": "new_title"},
            headers=self.headers,
            content_type="application/json",
        )
        res = req.json()
        print(res)
        self.assertEqual(res["title"], "new_title")

    def Test_delete(self):
        client = self.client
        req = client.delete(
            f'/api/v1/projects/{self.project["id"]}/', headers=self.headers
        )
        self.assertEqual(req.status_code, 204)

    def test_projects(self):
        self.Test_create()
        self.Test_update()
        self.Test_delete()

    def tearDown(self):
        self.client.delete(
            f'/api/v1/projects/{self.project["id"]}/', headers=self.headers
        )
