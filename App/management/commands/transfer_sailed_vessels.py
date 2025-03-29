from django.core.management.base import BaseCommand
from django.db import transaction
from App.models import LineUpForm, SailedData

class Command(BaseCommand):
    help = 'Transfers sailed vessels from LineUpForm to SailedData'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():  # Ensure atomicity
                sailed_vessels = LineUpForm.objects.filter(CurrentStatus="Sailed")
                transferred_count = 0

                sailed_data_objects = [
                    SailedData(
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

                # Bulk create records in SailedData
                SailedData.objects.bulk_create(sailed_data_objects)
                transferred_count = len(sailed_data_objects)

                # Bulk delete LineUpForm records
                sailed_vessels.delete()

            self.stdout.write(self.style.SUCCESS(f'Successfully transferred {transferred_count} records to SailedData.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

        