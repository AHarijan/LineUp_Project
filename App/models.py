from django.db import models
from django.contrib.auth.models import User
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    

class LineUpForm(models.Model):
    LineUp_Date=models.CharField(max_length=20,default="")
    Port=models.CharField(max_length=20,default="")
    Berth=models.CharField(max_length=20,default="")
    IMO_No=models.CharField(max_length=20,default="")
    Slt=models.CharField(max_length=20,default="")
    Vessel=models.CharField(max_length=20,default="")
    LOA=models.IntegerField(max_length=20,default="")
    Beam=models.IntegerField(max_length=20,default="")
    Draft=models.IntegerField(max_length=20,default="")
    
    # ETA_ATA_Date=models.CharField(max_length=20,null=True, blank=True)
    # ETA_ATA_Time=models.CharField(max_length=20,null=True, blank=True)
    # ETB_ATB_Date=models.CharField(max_length=20,null=True, blank=True)
    # ETB_ATB_Time=models.CharField(max_length=20,null=True, blank=True)
    # ETD_ATD_Date=models.CharField(max_length=20,null=True, blank=True)
    # ETD_ATD_Time=models.CharField(max_length=20,null=True, blank=True)

    ETA_ATA_Date=models.DateField(null=True, blank=True)
    ETA_ATA_Time=models.TimeField(null=True, blank=True)
    ETB_ATB_Date=models.DateField(null=True, blank=True)
    ETB_ATB_Time=models.TimeField(null=True, blank=True)
    ETD_ATD_Date=models.DateField(null=True, blank=True)
    ETD_ATD_Time=models.TimeField(null=True, blank=True)
    Cargo1=models.CharField(max_length=20,default="")
    CargoQty1=models.IntegerField(max_length=20,default="")
    CargoUnits1=models.CharField(max_length=20,default="")
    Cargo2=models.CharField(max_length=20,default="")
    CargoQty2=models.IntegerField(default=0)
    CargoUnits2=models.CharField(max_length=20,default="")
    Cargo3=models.CharField(max_length=20,default="")
    CargoQty3=models.IntegerField(default=0)
    CargoUnits3=models.CharField(max_length=20,default="")
    VesselType=models.CharField(max_length=20,default="")
    Operations=models.CharField(max_length=20,default="")
    Shipper=models.CharField(max_length=20,default="")
    Receiver=models.CharField(max_length=20,default="")
    Principal=models.CharField(max_length=20,default="")
    Owner=models.CharField(max_length=20,default="")
    C_F=models.CharField(max_length=20,default="")
    LastPort=models.CharField(max_length=20,default="")
    NextPort=models.CharField(max_length=20,default="")
    LoadPort=models.CharField(max_length=20,default="")
    DischargePort=models.CharField(max_length=20,default="")
    ChartererAgent=models.CharField(max_length=20,default="")
    OwnersAgent=models.CharField(max_length=20,default="")
    CurrentStatus=models.CharField(max_length=20,default="")
    Remarks=models.CharField(max_length=200,default="")


class Port_Berth_Form(models.Model):
    Country=models.CharField(max_length=20,default="")
    Port=models.CharField(max_length=20,default="")
    Berth=models.CharField(max_length=20,default="")
    Berth_Type=models.CharField(max_length=20,default="")
    Cargos_Handled_on_Berth=models.CharField(max_length=200,default="")
    Terminal=models.CharField(max_length=20,default="")