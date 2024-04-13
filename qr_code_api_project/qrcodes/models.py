from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name   
    
    
class QRCode(models.Model):
    TYPE_CHOICES = [
        ('URL', 'URL'),
        ('TEXT', 'Text'),
        ('WIFI', 'Wi-Fi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"QR Code ({self.type}) - Created by {self.user.username}"
     
