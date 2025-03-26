from celery import shared_task
from django.utils import timezone
from App.models import LineUpForm, SailedData

@shared_task
def archive_Sailed_vessels():
    sailed_vessels = LineUpForm.objects.filter(
        CurrentStatus="SAILED"
    ).exclude(
        id__in=SailedData.objects.values_list("original_id", flat=True)
    )
    
    Sailed_Data = [
        SailedData(
            original_id=vessel.id,
            LineUp_Date=vessel.LineUp_Date,
            Port=vessel.Port,
            Berth=vessel.Berth,
            IMO_No=vessel.IMO_No,
            Slt=vessel.Slt,
            Vessel=vessel.Vessel,
            LOA=vessel.LOA,
            Beam=vessel.Beam,
            Draft=vessel.Draft,
            ETA_ATA_Date=vessel.ETA_ATA_Date,
            ETA_ATA_Time=vessel.ETA_ATA_Time,
            ETB_ATB_Date=vessel.ETB_ATB_Date,
            ETB_ATB_Time=vessel.ETB_ATB_Time,
            ETD_ATD_Date=vessel.ETD_ATD_Date,
            ETD_ATD_Time=vessel.ETD_ATD_Time,
            Cargo1=vessel.Cargo1,
            CargoQty1=vessel.CargoQty1,
            CargoUnits1=vessel.CargoUnits1,
            Cargo2=vessel.Cargo2,
            CargoQty2=vessel.CargoQty2,
            CargoUnits2=vessel.CargoUnits2,
            Cargo3=vessel.Cargo3,
            CargoQty3=vessel.CargoQty3,
            CargoUnits3=vessel.CargoUnits3,
            VesselType=vessel.VesselType,
            Operations=vessel.Operations,
            Shipper=vessel.Shipper,
            Receiver=vessel.Receiver,
            Principal=vessel.Principal,
            Owner=vessel.Owner,
            C_F=vessel.C_F,
            LastPort=vessel.LastPort,
            NextPort=vessel.NextPort,
            LoadPort=vessel.LoadPort,
            DischargePort=vessel.DischargePort,
            ChartererAgent=vessel.ChartererAgent,
            OwnersAgent=vessel.OwnersAgent,
            CurrentStatus=vessel.CurrentStatus,
            Remarks=vessel.Remarks,
        )
        for vessel in sailed_vessels
    ]
    SailedData.objects.bulk_create(Sailed_Data)


    
from celery import shared_task
from .models import LineUpForm, TempSailedData

@shared_task
def archive_sailed_vessels():
    # Get vessels marked "SAILED" that aren't already archived
    new_sailed_vessels = LineUpForm.objects.filter(
        CurrentStatus="SAILED"
    ).exclude(
        id__in=SailedData.objects.values_list("original_id", flat=True)
    )

    # Bulk-create archived records (faster than looping)
    SailedData.objects.bulk_create([
        SailedData(
            original_id=vessel.id,
            LineUp_Date=vessel.LineUp_Date,
            Port=vessel.Port,
            Berth=vessel.Berth,
            IMO_No=vessel.IMO_No,
            # ... (copy all other fields)
            CurrentStatus=vessel.CurrentStatus,
        )
        for vessel in new_sailed_vessels
    ])

    return f"Archived {new_sailed_vessels.count()} new sailed vessels."