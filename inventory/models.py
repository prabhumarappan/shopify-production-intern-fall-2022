from django.db import models

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    located_at = models.CharField(max_length=50)

    def __str__(self):
        return self.name