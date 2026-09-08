from django.db import models

class OTP(models.Model):
    contact = models.CharField(max_length=100)  # mobile or email
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact} - {self.otp}"
