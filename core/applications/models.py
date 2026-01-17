from django.db import models
from users.models import Citizen
from panchayat.models import Panchayat

class Application(models.Model):

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('correction', 'Correction Required'),
        ('manual', 'Manual Visit Required'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    DELIVERY_CHOICES = [
        ('panchayat', 'Pickup from Panchayat'),
        ('taluka', 'Pickup from Taluka'),
        ('courier', 'Courier Delivery'),
    ]
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)


    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    panchayat = models.ForeignKey(Panchayat, on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=100)
    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default='panchayat'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.certificate_type} - {self.citizen.name}"
    
    def notification_message(self):
        if self.status == 'approved':
            return (
                f"Tamaro {self.certificate_type} certificate approve thai gayo chhe. "
                f"Tame {self.get_delivery_type_display()} thi lai shako chho."
            )

        if self.status == 'rejected':
            return (
                f"Tamari application reject thai chhe. Reason: {self.remarks}. "
                f"Details sudhari ne fari apply karo."
            )

        if self.status == 'correction':
            return (
                f"Tamari application ma sudharo jaruri chhe. "
                f"Message: {self.remarks}"
            )

        return "Tamari application process ma chhe."



class Document(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
