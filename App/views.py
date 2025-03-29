from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
import logging

def set_cookies(request):
    cokis = HttpResponse("Cookies is Set")
    cokis.set_cookie('my_cookie', 'cookie_value', max_age=3600, secure=True)
    return cokis

def index_pg(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('lineupform')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('signin')

    return render (request, 'Authentication/signin.html')

def signup_pg(request):
    if request.method == 'POST':

        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        userName=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=userName).exists():
            user_data_has_error = True
            messages.error(request, "User already exists.")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "email already taken.")

        if user_data_has_error:
            return redirect('signup')
        else:
            new_user = User.objects.create_user(
                
                first_name=first_name,
                last_name=last_name,
                username=userName,
                email=email,
                password=password
            )
            messages.success(request, "Account created successfully, please login")
            return redirect('signin')

    return render(request, 'Authentication/signup.html')

def forgotpass_pg(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('resetpass', kwargs={'reset_id': new_password_reset.reset_id})
            email_body = f'Reset your password using the link below:\n\n\n http://127.0.0.1:8000{password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )
          
            email_message.fail_silently = True
            email_message.send()

            # return redirect('resetpasssent')
            return redirect('resetpasssent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            # messages.error(request, "No user with email found")
            messages.error(request, 'Username does not exist. Please register.')
            return redirect('signin')

    return render (request,'Authentication/Forgotpassword.html')

def resetpass_pg(request, reset_id):

    try:
        reset_id  = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':

            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            expiration_time = reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:

                reset_id.delete()

                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

            if not passwords_have_error:
                user = reset_id.user
                user.set_password(password)
                user.save()
                
                # delete reset id after use
                reset_id.delete()

                # redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('signin')

            else:
                # redirect back to password reset page and display errors
                return redirect('resetpass', reset_id=reset_id)
    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgotpass')

    return render (request,'Authentication/passwordReset.html')

def resetpasssent_pg(request, reset_id):

        if PasswordReset.objects.filter(reset_id=reset_id).exists():
            return render(request, 'Authentication/passwordResetSent.html')
        else:
            # redirect to forgot password page if code does not exist
            messages.error(request, 'Invalid reset id')
            return redirect('forgotpass')
        
@login_required 
def LineupForm_pg(request):

    ports = Port_Berth_Form.objects.values_list('Port', flat=True).distinct().order_by('Port')
    
    if request.method=="POST":
        lineup_date=request.POST['lineupdate']
        port=request.POST['port']
        berth=request.POST['berth']
        imo_no=request.POST['imono']
        slt=request.POST['vesselSlt']
        vessel=request.POST['vessel']
        loa=request.POST['loa']
        beam=request.POST['beam']
        draft=request.POST['draft']
        eta_ata_date=request.POST['etadate'] if request.POST['etadate'] else None
        eta_ata_time=request.POST['etatime'] if request.POST['etatime'] else None
        etb_atb_date=request.POST['etbdate'] if request.POST['etbdate'] else None
        etb_atb_time=request.POST['etbtime'] if request.POST['etbtime'] else None
        etd_atd_date=request.POST['etcdate'] if request.POST['etcdate'] else None
        etd_atd_time=request.POST['etctime'] if request.POST['etctime'] else None
        cargo1=request.POST['cargo1']
        cargoqty1=request.POST['cargoqty1']
        cargounits1=request.POST['cargoqtyU1']
        cargo2=request.POST['cargo2']
        cargoqty2=request.POST.get('cargoqty2', 0)
        cargounits2=request.POST['cargoqtyU2']
        cargo3=request.POST['cargo3']
        cargoqty3=request.POST.get('cargoqty3',0)
        cargounits3=request.POST['cargoqtyU3']
        vesseltype=request.POST['vesseltype']
        operations=request.POST['operation']
        shipper=request.POST['shipper']
        receiver=request.POST['receiver']
        principal=request.POST['principal']
        owner=request.POST['owner']
        c_f=request.POST['C/F']
        lastport=request.POST['lastport']
        nextport=request.POST['nextport']
        loadport=request.POST['loadPort']
        dischargeport=request.POST['dischargePort']
        chartereragent=request.POST['cAgent']
        ownersagent=request.POST['agent']
        currentstatus=request.POST['status']
        remarks=request.POST.get('textarea')

        obj=LineUpForm(LineUp_Date=lineup_date, Port=port, Berth=berth, IMO_No=imo_no, Slt=slt, Vessel=vessel, LOA=loa, Beam=beam, Draft=draft, ETA_ATA_Date=eta_ata_date, ETA_ATA_Time=eta_ata_time, ETB_ATB_Date=etb_atb_date, ETB_ATB_Time=etb_atb_time, ETD_ATD_Date=etd_atd_date, ETD_ATD_Time=etd_atd_time, Cargo1=cargo1, CargoQty1=cargoqty1, CargoUnits1=cargounits1, Cargo2=cargo2, CargoQty2=cargoqty2, CargoUnits2=cargounits2, Cargo3=cargo3, CargoQty3=cargoqty3, CargoUnits3=cargounits3, VesselType=vesseltype, Operations=operations, Shipper=shipper, Receiver=receiver, Principal=principal, Owner=owner, C_F=c_f, LastPort=lastport, NextPort=nextport, LoadPort=loadport, DischargePort=dischargeport, ChartererAgent=chartereragent, OwnersAgent=ownersagent, CurrentStatus=currentstatus, Remarks=remarks)
        obj.save()

        return redirect('lineupform')

    objs=LineUpForm.objects.all().order_by('CurrentStatus')
    return render(request, 'Pages/lineupForm.html',{'datas':objs, 'ports': ports})

@login_required 
def ExtractData_pg(request):

    ports = Port_Berth_Form.objects.values_list('Port', flat=True).distinct().order_by('Port')
    cargos = SailedData.objects.values_list('Cargo1', flat=True).distinct().order_by('Cargo1')
    sailed_vessel = SailedData.objects.all().order_by('Port', '-ETD_ATD_Date')
    
    context = {
        'ports': ports,
        'cargos':cargos,
        'sailed_Vessel': sailed_vessel,
        'title':'Archived Sailed Vessels'
    }

    return render(request, 'Pages/extractData.html', context)


@login_required 
def UpdateLineup_pg(request,id):
    update=LineUpForm.objects.get(id=id)
    data = {
            "ETA_ATA_Date": update.ETA_ATA_Date.strftime("%Y-%m-%d") if update.ETA_ATA_Date else "",
            "ETB_ATB_Date": update.ETB_ATB_Date.strftime("%Y-%m-%d") if update.ETB_ATB_Date else "",
            "ETD_ATD_Date": update.ETD_ATD_Date.strftime("%Y-%m-%d") if update.ETD_ATD_Date else "",
            "ETA_ATA_Time": update.ETA_ATA_Time.strftime("%H:%M") if update.ETA_ATA_Time else "",
            "ETB_ATB_Time": update.ETB_ATB_Time.strftime("%H:%M") if update.ETB_ATB_Time else "",
            "ETD_ATD_Time": update.ETD_ATD_Time.strftime("%H:%M") if update.ETD_ATD_Time else "",
        }
    if request.method=='POST':
        lineup_date=request.POST['lineupdate']
        port=request.POST['port']
        berth=request.POST['berth']
        imo_no=request.POST['imono']
        slt=request.POST['vesselSlt']
        vessel=request.POST['vessel']
        loa=request.POST['loa']
        beam=request.POST['beam']
        draft=request.POST['draft']
        eta_ata_date=request.POST['etadate'] if request.POST['etadate'] else None
        eta_ata_time=request.POST['etatime'] if request.POST['etatime'] else None
        etb_atb_date=request.POST['etbdate'] if request.POST['etbdate'] else None
        etb_atb_time=request.POST['etbtime'] if request.POST['etbtime'] else None
        etd_atd_date=request.POST['etcdate'] if request.POST['etcdate'] else None
        etd_atd_time=request.POST['etctime'] if request.POST['etctime'] else None
        cargo1=request.POST['cargo1']
        cargoqty1=request.POST['cargoqty1']
        cargounits1=request.POST['cargoqtyU1']
        cargo2=request.POST['cargo2']
        cargoqty2=request.POST['cargoqty2']
        cargounits2=request.POST['cargoqtyU2']
        cargo3=request.POST['cargo3']
        cargoqty3=request.POST['cargoqty3']
        cargounits3=request.POST['cargoqtyU3']
        vesseltype=request.POST['vesseltype']
        operations=request.POST['operation']
        shipper=request.POST['shipper']
        receiver=request.POST['receiver']
        principal=request.POST['principal']
        owner=request.POST['owner']
        c_f=request.POST['C/F']
        lastport=request.POST['lastport']
        nextport=request.POST['nextport']
        loadport=request.POST['loadPort']
        dischargeport=request.POST['dischargePort']
        chartereragent=request.POST['cAgent']
        ownersagent=request.POST['agent']
        currentstatus=request.POST['status']
        remarks=request.POST['textarea']
        

        update.LineUp_Date=lineup_date
        update.Port=port
        update.Berth=berth
        update.IMO_No=imo_no
        update.Slt=slt
        update.Vessel=vessel
        update.LOA=loa
        update.Beam=beam
        update.Draft=draft
        update.ETA_ATA_Date=eta_ata_date
        update.ETA_ATA_Time=eta_ata_time
        update.ETB_ATB_Date=etb_atb_date
        update.ETB_ATB_Time=etb_atb_time
        update.ETD_ATD_Date=etd_atd_date
        update.ETD_ATD_Time=etd_atd_time
        update.Cargo1=cargo1
        update.CargoQty1=cargoqty1
        update.CargoUnits1=cargounits1
        update.Cargo2=cargo2
        update.CargoQty2=cargoqty2
        update.CargoUnits2=cargounits2
        update.Cargo3=cargo3
        update.CargoQty3=cargoqty3
        update.CargoUnits3=cargounits3
        update.VesselType=vesseltype
        update.Operations=operations
        update.Shipper=shipper
        update.Receiver=receiver
        update.Principal=principal
        update.Owner=owner
        update.C_F=c_f
        update.LastPort=lastport
        update.NextPort=nextport
        update.LoadPort=loadport
        update.DischargePort=dischargeport
        update.ChartererAgent=chartereragent
        update.OwnersAgent=ownersagent
        update.CurrentStatus=currentstatus
        update.Remarks=remarks
        update.save()
        return redirect('lineupform')


    return render(request, 'Pages/updatelineup.html',{'data': data, 'update': update})




def DeleteLineup_pg(request,id):
    deldata=LineUpForm.objects.get(id=id)
    deldata.delete()
    return redirect('lineupform')



@login_required 
def AddPortBerth_pg(request):
    if request.method == 'POST':
        # Extract Section 1 data (Country and Port)
        country = request.POST.get('country')
        port = request.POST.get('port')

        # Extract Section 2 data (multiple entries)
        berths = request.POST.getlist('berth')
        berth_types = request.POST.getlist('berthType')
        cargos_handled = request.POST.getlist('cargoType')
        terminals = request.POST.getlist('terminal')

        # Validate that all fields are present
        if country and port and berths and berth_types and cargos_handled and terminals:
            # Save each Berth entry
            for i in range(len(berths)):
                Port_Berth_Form.objects.create(
                    Country=country,
                    Port=port,
                    Berth=berths[i],
                    Berth_Type=berth_types[i],
                    Cargos_Handled_on_Berth=cargos_handled[i],
                    Terminal=terminals[i]
                )
            return redirect('addportberth')  # Redirect to a success page
        else:
            # Handle validation error
            return render(request, 'Pages/addPortBerth.html', {'error': 'Please fill all fields.'})

    # Render the form for GET requests
    return render(request, 'Pages/addPortBerth.html')


def get_berths(request):
    port = request.GET.get('port')  # Get the selected port from the request
    if port:
        # Fetch all berths for the selected port
        berths = Port_Berth_Form.objects.filter(Port=port).values_list('Berth', flat=True).distinct()
        berths_list = list(berths)  # Convert QuerySet to a list
        return JsonResponse({'berths': berths_list})
    return JsonResponse({'berths': []})


def get_updated_berths(request):
    port = request.GET.get('port', None)
    if port:
        # Get unique berths for the selected port
        Uberths = Port_Berth_Form.objects.filter(Port=port).values_list('Berth', flat=True).distinct()
        Uberths_list = list(Uberths)  # Convert QuerySet to a list
        return JsonResponse({'Uberths': Uberths_list})
    return JsonResponse({'Uberths': []})


def get_autocomplete_suggestions(request):
    query = request.GET.get('query', '')  # Get the search term from the URL
    field = request.GET.get('field', '')  # Get the field name from the URL (e.g., 'Shipper', 'Receiver')
    
    if field and hasattr(SailedData, field):  # Check if the field exists in the model
        suggestions = SailedData.objects.filter(**{f"{field}__icontains": query}).values_list(field, flat=True).distinct()
        return JsonResponse(list(suggestions), safe=False)
    else:
        return JsonResponse([], safe=False)
    


# def ExtractData_pg(request):
#     sailed_Vessel = SailedData.objects.all().order_by('Port', '-ETD_ATD_Date') #change LineUpForm to SailedData
#     context = {
#         'sailed_Vessel':sailed_Vessel,
#         'title':'Archived Sailed Vessels'
#     }
#     return render(request, 'Pages/extractData.html', context)



def move_sailed_data():

    sailed_record = LineUpForm.objects.filter(CurrentStatus="SAILED")

    for record in sailed_record:
        SailedData.objects.create(
            LineUp_Date=record.LineUp_Date,
            Port=record.Port,
            Berth=record.Berth,
            IMO_No=record.IMO_No,
            Slt=record.Slt,
            Vessel=record.Vessel,
            LOA=record.LOA,
            Beam=record.Beam,
            Draft=record.Draft,
            ETA_ATA_Date=record.ETA_ATA_Date,
            ETA_ATA_Time=record.ETA_ATA_Time,
            ETB_ATB_Date=record.ETB_ATB_Date,
            ETB_ATB_Time=record.ETB_ATB_Time,
            ETD_ATD_Date=record.ETD_ATD_Date,
            ETD_ATD_Time=record.ETD_ATD_Time,
            Cargo1=record.Cargo1,
            CargoQty1=record.CargoQty1,
            CargoUnits1=record.CargoUnits1,
            Cargo2=record.Cargo2,
            CargoQty2=record.CargoQty2,
            CargoUnits2=record.CargoUnits2,
            Cargo3=record.Cargo3,
            CargoQty3=record.CargoQty3,
            CargoUnits3=record.CargoUnits3,
            VesselType=record.VesselType,
            Operations=record.Operations,
            Shipper=record.Shipper,
            Receiver=record.Receiver,
            Principal=record.Principal,
            Owner=record.Owner,
            C_F=record.C_F,
            LastPort=record.LastPort,
            NextPort=record.NextPort,
            LoadPort=record.LoadPort,
            DischargePort=record.DischargePort,
            ChartererAgent=record.ChartererAgent,
            OwnersAgent=record.OwnersAgent,
            CurrentStatus=record.CurrentStatus,
            Remarks=record.Remarks,
        )
    sailed_record.delete()

def filter_sailed_data(request):
    # Start with all objects
    queryset = SailedData.objects.all()
    
    if request.method == 'POST':
        # Get form data
        port = request.POST.get('port')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDatei')
        cargo = request.POST.get('cargo')
        vessel_type = request.POST.get('vesseltype')
        operation = request.POST.get('operation')
        load_port = request.POST.get('loadport')
        discharge_port = request.POST.get('dischargeport')
        agent = request.POST.get('agent')
        
        # Apply filters based on form inputs
        if port:
            queryset = queryset.filter(Port=port)
            
        if start_date and end_date:
            # Convert string dates to date objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(
                Q(ETA_ATA_Date__range=[start_date, end_date]) |
                Q(ETB_ATB_Date__range=[start_date, end_date]) |
                Q(ETD_ATD_Date__range=[start_date, end_date])
            )
            
        if cargo:
            queryset = queryset.filter(
                Q(Cargo1__icontains=cargo) |
                Q(Cargo2__icontains=cargo) |
                Q(Cargo3__icontains=cargo)
            )
            
        if vessel_type:
            queryset = queryset.filter(VesselType__icontains=vessel_type)
            
        if operation:
            queryset = queryset.filter(Operations__icontains=operation)
            
        if load_port:
            queryset = queryset.filter(LoadPort__icontains=load_port)
            
        if discharge_port:
            queryset = queryset.filter(DischargePort__icontains=discharge_port)
            
        if agent:
            queryset = queryset.filter(
                Q(ChartererAgent__icontains=agent) |
                Q(OwnersAgent__icontains=agent)
            )
    
    context = {
        'sailed_data': queryset,
        'ports': ['Port1', 'Port2', 'Port3']  # Replace with your actual ports
    }

    return render(request, 'Pages/extractData.html', context)