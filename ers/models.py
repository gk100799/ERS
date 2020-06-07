from django.db import models
from datetime import datetime
from django.db import connection




class Events(models.Model):
    event_id = models.CharField(primary_key=True, max_length=4)
    event_name = models.CharField(max_length=30)
    description = models.TextField()
    organizers = models.CharField(max_length=40)
    venue = models.CharField(max_length=20)
    time = models.TimeField()
    date = models.DateField()
    limit_max = models.CharField(max_length=5)
    fee = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class Questions(models.Model):
    question_id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(Events, models.DO_NOTHING)
    question = models.TextField()
    option1 = models.CharField(max_length=30, blank=True, null=True)
    option2 = models.CharField(max_length=30, blank=True, null=True)
    option3 = models.CharField(max_length=30, blank=True, null=True)
    option4 = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questions'
        unique_together = (('question_id', 'event'),)


class Registers(models.Model):
    user_id = models.CharField(primary_key=True, max_length=15)
    registered_on = models.DateField(blank=True, null=True)
    event = models.ForeignKey(Events, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'registers'
        unique_together = (('user_id', 'event'),)


class SurResponse(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, primary_key=True)
    event_id = models.CharField(max_length=4)
    question = models.ForeignKey(Questions, models.DO_NOTHING)
    response = models.TextField()

    class Meta:
        managed = False
        db_table = 'sur_response'
        unique_together = (('user', 'event_id', 'question'),)


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=15)
    password = models.CharField(max_length=15)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=11)
    branch = models.CharField(max_length=5)
    is_admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'



class Survey(models.Model):
    date = models.DateTimeField(primary_key=True)
    event_id_id = models.ForeignKey(Registers, on_delete=models.DO_NOTHING)
    user_id_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'ers_survey'



class viewresponse(models.Model):
    user_id = models.CharField(max_length=15,primary_key=True)
    question_id = models.IntegerField()
    eventid = models.CharField(max_length=4)
    question = models.TextField(max_length=75, blank=False)
    option1 = models.CharField(max_length=30, blank=True, null=True)
    option2 = models.CharField(max_length=30, blank=True, null=True)
    option3 = models.CharField(max_length=30, blank=True, null=True)
    option4 = models.CharField(max_length=30, blank=True, null=True)
    response = models.TextField(max_length=50,blank=False)
    class Meta:
        managed = False
        db_table = 'ers_responseview'


class count(models.Model):
    event_id=models.CharField(max_length=15,primary_key=True)
    count=models.IntegerField()
    class Meta:
        managed=False
        db_table='count'



class Response(models.Model):
    event_id = models.CharField(max_length=15, primary_key=True)
    question_id = models.CharField(max_length=5)
    question=models.CharField(max_length=20)
    option=models.CharField(max_length=20)
    count=models.IntegerField()
    percent=models.IntegerField()
    class Meta:
        managed=False
        db_table='response'
    



class MY_UTIL():

    def getstudents(self, control_in, message_in):
        cursor = connection.cursor()
        ret = cursor.callproc("MY_UTIL.getstudents", (control_in, message_in))
        cursor.close()
        return ret
