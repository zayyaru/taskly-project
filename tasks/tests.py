from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


class TaskBoardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("aye", password="pass12345")
        self.other = User.objects.create_user("bo", password="pass12345")
        self.client.login(username="aye", password="pass12345")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_task_belongs_to_current_user(self):
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "စာကျက်ရန်",
                "details": "အခန်း ၃",
                "priority": Task.Priority.HIGH,
                "status": Task.Status.TODO,
                "due_date": "",
            },
        )
        self.assertRedirects(response, reverse("task_list"))
        task = Task.objects.get()
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.title, "စာကျက်ရန်")

    def test_cannot_open_another_users_task(self):
        task = Task.objects.create(owner=self.other, title="လျှို့ဝှက်")
        response = self.client.get(reverse("task_edit", args=[task.pk]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_marks_done_and_back(self):
        task = Task.objects.create(owner=self.user, title="ဈေးဝယ်ရန်")
        self.client.post(reverse("task_toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)
        self.client.post(reverse("task_toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.TODO)

    def test_filter_by_status(self):
        Task.objects.create(owner=self.user, title="စာကျက်ရန်-ဖွင့်", status=Task.Status.TODO)
        Task.objects.create(owner=self.user, title="စာကျက်ရန်-ပိတ်", status=Task.Status.DONE)
        response = self.client.get(reverse("task_list"), {"status": "done"})
        self.assertContains(response, "စာကျက်ရန်-ပိတ်")
        self.assertNotContains(response, "စာကျက်ရန်-ဖွင့်")

    def test_overdue_ignores_finished_tasks(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        open_task = Task.objects.create(
            owner=self.user, title="နောက်ကျ", due_date=yesterday
        )
        done_task = Task.objects.create(
            owner=self.user,
            title="ပြီးသွားပြီ",
            due_date=yesterday,
            status=Task.Status.DONE,
        )
        self.assertTrue(open_task.is_overdue)
        self.assertFalse(done_task.is_overdue)

    def test_signup_logs_in(self):
        self.client.logout()
        response = self.client.post(
            reverse("signup"),
            {
                "username": "cho",
                "password1": "a-strong-pass-99",
                "password2": "a-strong-pass-99",
            },
        )
        self.assertRedirects(response, reverse("task_list"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="cho").pk)
