from django.db import models

# Create your models here.


class listings(models.Model):
    added_date = models.DateTimeField()
    heading = models.CharField(max_length=1200)
    price = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    rooms = models.IntegerField(default=1)
    location = models.CharField(max_length=200)
    check12 = models.CharField(max_length=200)
    link = models.CharField(max_length=1200)
    image = models.CharField(max_length=1200)
    category = models.CharField(max_length=200)
    SubCategory = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.heading)

    class Meta:
        verbose_name_plural = 'listings'


class subscriptions(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    added_date = models.DateTimeField()
    email = models.EmailField(max_length=1200, default="empty")
    WAnumber = models.CharField(max_length=20, default="empty")
    ip = models.CharField(max_length=20, default="empty")
    name = models.CharField(max_length=200, default="empty")

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        verbose_name_plural = 'Subscriptions'

