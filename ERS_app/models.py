from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class ERSEvent(models.Model):
    # id = models.CharField(max_length=4, unique = true, blank=False, null=False)
    name = models.CharField(max_length=15, blank=False, null=False)
    start_date = models.DateField()
    end_date = models.DateField()
    #description = models.TextField(blank=True)
    organizers = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=20, blank=True)
    time = models.TimeField()
    limit = models.IntegerField(blank=True)
    fee = models.CharField(max_length=10)

class ERSQuestion(models.Model):
    event_id = models.ForeignKey(to=ERSEvent, on_delete=models.CASCADE)
    questionType = models.CharField(max_length=10, default='MCQ')
    question = models.TextField(max_length=75, blank=False)
    option1 = models.CharField(max_length=30, blank=True, null=True)
    option2 = models.CharField(max_length=30, blank=True, null=True)
    option3 = models.CharField(max_length=30, blank=True, null=True)
    option4 = models.CharField(max_length=30, blank=True, null=True)


class ERSSurvey(models.Model):
    event_id = models.ForeignKey(to=ERSEvent, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(to=ERSQuestion, on_delete=models.CASCADE)
    response = models.TextField(max_length=50,blank=False)
    date = models.DateTimeField(default=datetime.now, blank=True)

