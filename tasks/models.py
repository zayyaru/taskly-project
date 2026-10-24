from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "နိမ့်"
        MEDIUM = "medium", "အလယ်"
        HIGH = "high", "မြင့်"

    class Status(models.TextChoices):
        TODO = "todo", "လုပ်ရန်"
        DOING = "doing", "လုပ်နေသည်"
        DONE = "done", "ပြီးပြီ"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField("ခေါင်းစဉ်", max_length=200)
    details = models.TextField("အသေးစိတ်", blank=True)
    priority = models.CharField(
        "အရေးကြီးမှု",
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        "အခြေအနေ",
        max_length=10,
        choices=Status.choices,
        default=Status.TODO,
    )
    due_date = models.DateField("နောက်ဆုံးရက်", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "အလုပ်"
        verbose_name_plural = "အလုပ်များ"

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date is None or self.status == self.Status.DONE:
            return False
        return self.due_date < timezone.localdate()
