import random
from unittest import TestCase
from django.test import Client
from string import ascii_letters, printable


# Create your tests here.
class UserAuthTestCase(TestCase):
    def test_register_exist_user(self):
        client = Client()
        req = client.post(
            "/api/v1/register/",
            {"username": "arsolovov", "password": "12345678"},
        )
        self.assertDictEqual(
            req.json(),
            {"username": ["Пользователь с таким именем уже существует."]},
        )
        assert req.status_code != 404

    def test_register_login_delete_user(self):
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
            "/api/v1/token/", {"username": "arsolovov", "password": "12345678"}
        )
        login_res = login.json()

        assert "access" in login_res.keys()

        self.headers = {"Authorization": f'Bearer {login_res["access"]}'}
        self.status_name = "".join(
            random.choice(ascii_letters) for _ in range(12)
        )

    def Test_status_create(self):
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

    def Test_status_change(self):
        client = self.client
        new_name = "".join(random.choice(ascii_letters) for _ in range(12))
        print(new_name)
        req = client.put(
            f"/api/v1/task-status/{int(self.status_id)}/",
            {"name": str(new_name)},
            headers=self.headers,
            content_type="application/json",
        )
        print(req.json())
        self.assertEqual(req.status_code, 200)

        req = client.put(
            f"/api/v1/task-status/{int(self.status_id)}/",
            {
                "name": str(self.status_name),
            },
            headers=self.headers,
            content_type="application/json",
        )

        self.assertEqual(req.status_code, 200)

    def Test_status_delete(self):
        client = self.client

        req = client.delete(
            f"/api/v1/task-status/{self.status_id}/",
            headers=self.headers,
        )

        self.assertEqual(req.status_code, 204)

    def test_status(self):
        self.Test_status_create()
        self.Test_status_change()
        self.Test_status_delete()
