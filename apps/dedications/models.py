from django.db import models
from ..users.models import User

# Create your models here.
class Task(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=False)
    name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'({self.code}) {self.name}'

class Occupation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user} - {self.task}'

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'task'], name='unique_user_task')
        ]
    
    def __str__(self):
        return f'{self.user} - {self.task}'