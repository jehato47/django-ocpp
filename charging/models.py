from django.db import models

# Create your models here.
# models.py

from django.db import models

class ChargePoint(models.Model):
    charge_point_id = models.CharField(max_length=100, unique=True)
    vendor = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    last_heartbeat = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.charge_point_id


class Transaction(models.Model):
    transaction_id = models.IntegerField(unique=True)
    charge_point = models.ForeignKey(ChargePoint, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField(null=True, blank=True)
    meter_start = models.IntegerField()
    meter_stop = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.charge_point.charge_point_id}"