from django.db import models
from django.contrib.auth.models import User

class ExpandedUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.deletion.CASCADE)
    is_admin = models.BooleanField(default=False)


class VKGroup(models.Model):
    vk_id = models.IntegerField(unique=True, primary_key=True)
    user_id = models.ForeignKey(to=User, on_delete=models.deletion.CASCADE)

class Home(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.deletion.CASCADE)
    group_id = models.ForeignKey(to=VKGroup, on_delete=models.deletion.CASCADE)
    address = models.CharField(max_length=300)
    space = models.IntegerField()
    flats_count = models.IntegerField()

class Flat(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.deletion.CASCADE)
    home_id = models.ForeignKey(to=Home, on_delete=models.deletion.CASCADE)
    number = models.IntegerField()
    space = models.IntegerField()


