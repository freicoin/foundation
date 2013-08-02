from django.db import models

class FaucetSend(models.Model):
    ip_address = models.CharField(max_length=15)
    frc_address = models.CharField(max_length=34)
    tx_id = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
