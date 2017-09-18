from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out 

# class UserProfile(models.Model):
#     user   = models.OneToOneField(User)
#     avatar = models.ImageField(upload_to='/images/')

class LoggedUsers(models.Model):
    user = models.ForeignKey(User, primary_key=True)

    def __unicode__(self):
        return '{}{}{}'.format(self.user.first_name + " ",  self.user.last_name  + " (", self.user.username + ")")
        #return '%s %s %s %s' % (self.user.id, self.user.username, self.user.first_name, self.user.last_name)


def login_user(sender, request, user, **kwargs):
        LoggedUsers(user=user).save()

def logout_user(sender, request, user, **kwargs):
        try:
            u = LoggedUsers.objects.get(user=user)
            u.delete()
        except LoggedUsers.DoesNotExist:
            pass

user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)