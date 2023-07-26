from django.db import models

# you should set max_length for CharFileds if you use Django<4 or SQLite

class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField() 
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'UserTokens'

    def __str__(self) -> str:
        return "User with id: " + str(self.user_id)  
    