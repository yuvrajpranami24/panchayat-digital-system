from django.db import models

class Panchayat(models.Model):
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.village} ({self.taluka})"
