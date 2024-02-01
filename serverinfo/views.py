from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.validators import validate_ipv4_address
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import json
import xlwt

from serverinfo.forms import ServerAddForm, ServerEditForm, ServerRackInfoAddForm, ServerRackInfoEditForm, ServiceAddForm, VMAddForm, VMEditForm, ServiceEditForm, ServiceAddFormModal
from serverinfo.models import OsType, OsVersion, PhysicalServer, Project, RunningServices, ServerRackInfo, ServiceType, ServiceGroup, VMLocationType, VirtualServer, Zone


@login_required
def add_server(request):
    if request.method == 'POST':
        server_add_form = ServerAddForm(request.POST)
        server_rack_info_form = ServerRackInfoAddForm(request.POST)
        service_add_form = ServiceAddForm()
        # print(server_rack_info_form)

        service_list = RunningServices.objects.all()
        # print(server_add_form.errors.as_data())
        # if server_add_form.is_valid():
        #     print("server")

        if server_add_form.is_valid() and server_rack_info_form.is_valid():
            server_loc = server_rack_info_form.cleaned_data['location']
            server_rack = server_rack_info_form.cleaned_data['rack']
            loc_in_rack = server_rack_info_form.cleaned_data['loc_in_rack']
            form_factor = server_rack_info_form.cleaned_data['form_factor']

            new_server = server_add_form.save() 
            new_server.refresh_from_db()
            new_server.update_by = request.user
            new_server.update_time = timezone.now()
            new_server.server_type = "Physical"
            new_server.save()
            server_rack = ServerRackInfo(server=new_server, location=server_loc, rack=server_rack, loc_in_rack=loc_in_rack, form_factor=form_factor)
            server_rack.save() 
            messages.success(request, 'New Server Has been Added Successfully!')
            return redirect('add-server')
        else:
            print("form invalid")

    else:
        server_add_form = ServerAddForm()
        server_rack_info_form = ServerRackInfoAddForm()
        service_add_form = ServiceAddForm()
        service_list = RunningServices.objects.all()

    context = {
        'server_add_form' : server_add_form,
        'server_rack_info_add_form' : server_rack_info_form,
        'service_add_form':service_add_form,
        'service_list' : service_list
    }
    return render(request, 'server/add_physical_server.html', context) 

@login_required
def edit_server(request, pk):
    server = get_object_or_404(PhysicalServer, pk=pk)
    server_rack = get_object_or_404(ServerRackInfo, server=server)
    if request.method == 'POST':
        server_add_form = ServerEditForm(pk, request.POST, instance=server)
        server_rack_info_form = ServerRackInfoEditForm(request.POST, instance=server_rack)
        service_add_form = ServiceAddForm()
        # service_add_form = ""
        if server_add_form.is_valid() and server_rack_info_form.is_valid():
            
            server = server_add_form.save()
            server.refresh_from_db()
            server.update_by = request.user
            server.update_time = timezone.now()
            server.server_type = "Physical"
            server.save()
            server_rack_info_form.save()            
            messages.success(request, 'Server info Successfully Updated.')
            return redirect('view-server')    
        else:
            print("ok")

    else:
        server_add_form = ServerEditForm(pk, instance=server)
        server_rack_info_form = ServerRackInfoEditForm(instance=server_rack)
        service_add_form = ServiceAddForm()

    context = {
        'server_add_form' : server_add_form,
        'server_rack_info_edit_form' : server_rack_info_form,
        'service_add_form' : service_add_form,
        'server':server,

    }
    return render(request, 'server/edit_physical_server.html', context) 

@login_required
def add_os(request):
    # import datetime
    if request.method == 'POST':
        if request.POST["os_name"] != "":
            # data = json.loads(request.body)
            # os_name = data.get("os_name", "")
            os_name = request.POST["os_name"]
            # print(os_name)
            if OsType.objects.filter(os_type=os_name):
                return JsonResponse({"status":"error","message": f"There is a OS named {os_name}"})
            else:
                os_instance = OsType(os_type=os_name, update_by=request.user, update_time=timezone.now())
                os_instance.save()
                all_os = OsType.objects.filter(delete_status=False).values()
                # print(list(all_os))
                return JsonResponse({"status":"success","message": f"OS name {os_name} has been created.","all_os": list(all_os)})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})  
    
@login_required
def add_service_type(request):
    # import datetime
    if request.method == 'POST':
        if request.POST["service_type"] != "":
            # data = json.loads(request.body)
            # os_name = data.get("os_name", "")
            service_type = request.POST["service_type"]
            print(service_type)
            if ServiceType.objects.filter(service_type_name=service_type):
                return JsonResponse({"status":"error","message": f"There is a Service type {service_type}"})
            else:
                service_type_instance = ServiceType(service_type_name=service_type, update_by=request.user, update_time=timezone.now())
                service_type_instance.save()
                all_service_type = ServiceType.objects.filter(delete_status=False).values()
                # print(list(all_service_type))
                return JsonResponse({"status":"success","message": f"Service Type {service_type} has been created.","all_service_type": list(all_service_type)})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})  

@login_required
def add_service_group(request):
    # import datetime
    if request.method == 'POST':
        if request.POST["service_group"] != "":
            # data = json.loads(request.body)
            # os_name = data.get("os_name", "")
            service_group = request.POST["service_group"]
            if ServiceGroup.objects.filter(service_group_name=service_group):
                return JsonResponse({"status":"error","message": f"There is a Service group named {service_group}"})
            else:
                service_group_instance = ServiceGroup(service_group_name=service_group, update_by=request.user, update_time=timezone.now())
                service_group_instance.save()
                all_service_group = ServiceGroup.objects.filter(delete_status=False).values()
                return JsonResponse({"status":"success","message": f"Service Group {service_group} has been created.","all_service_group": list(all_service_group)})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})  

@login_required
def add_os_version(request):
    import datetime
    if request.method == 'POST':
        if request.POST["os_version"] != "":
            # data = json.loads(request.body)
            # os_name = data.get("os_name", "")
            os_version = request.POST["os_version"]
            print(os_version)
            if OsVersion.objects.filter(os_version=os_version):
                return JsonResponse({"status":"error","message": f"There is a OS version named {os_version}"})
            else:
                os_version_instance = OsVersion(os_version=os_version, update_by=request.user, update_time=timezone.now())
                os_version_instance.save()
                all_os_version = OsVersion.objects.filter(delete_status=False).values()
                # print(list(all_os_version))
                return JsonResponse({"status":"success","message": f"OS version {os_version} has been created.","all_os_version": list(all_os_version)})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})        
        
@login_required
def add_zone(request):
    import datetime
    if request.method == 'POST':
        if request.POST["zone"] != "":
            zone = request.POST["zone"]
            print(zone)
            if Zone.objects.filter(zone=zone):
                return JsonResponse({"status":"error","message": f"There is a Zone named {zone}"})
            else:
                zone_instance = Zone(zone=zone, update_by=request.user, update_time=timezone.now())
                zone_instance.save()
                all_zone = Zone.objects.filter(delete_status=False).values()
                # print(list(all_zone))
                return JsonResponse({"status":"success","message": f"Zone {zone} has been created.","all_zone": list(all_zone)})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})
            
@login_required
def add_project(request):
    import datetime
    if request.method == 'POST':
        if request.POST["project"] != "":
            project = request.POST["project"]
            print(project)
            if Project.objects.filter(project=project):
                return JsonResponse({"status":"error","message": f"There is a Project named {project}"})
            else:
                project_instance = Project(project=project, update_by=request.user, update_time=timezone.now())
                project_instance.save()
                all_project = Project.objects.filter(delete_status=False).values()
                # print(list(all_project))
                return JsonResponse({"status":"success","message": f"Project {project} has been created.","all_project": list(all_project)}) 
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def add_service(request):
    errors=""
    if request.method == 'POST':
        service_add_form = ServiceAddForm(request.POST)
        if service_add_form.is_valid():
            new_service = service_add_form.save() 
            new_service.refresh_from_db()
            new_service.update_by = request.user
            new_service.update_time = timezone.now()
            new_service.save()
            messages.success(request, f'Service { service_add_form.cleaned_data["service_name"]} has been added Successfully.')
        # if service_add_form.errors:
        #     errors = service_add_form.errors
            return redirect('add-service')
    else:
        service_add_form = ServiceAddForm()
    context = {
        'service_add_form':service_add_form,
        'errors':errors
    }
    return render(request, 'server/add_service.html',context) 

@login_required
def add_service_modal(request):
    if request.method == 'POST':
        if request.POST["service_name"] != "" and request.POST["service_owner"] != "":
            # print(request.POST["server_id"]+request.POST["server_type"])
        # if request.is_ajax():
            if not RunningServices.objects.filter(service_name=request.POST["service_name"]):
                if request.POST["service_type"] != "" :
                    form = ServiceAddFormModal(request.POST)

                    if form.is_valid():
                        service_name = form.cleaned_data['service_name']
                        service_ip = form.cleaned_data.get('service_ip')
                        
                        if service_ip:
                            try:
                                validate_ipv4_address(service_ip)
                            except:
                                return JsonResponse({"status":"error","message": f"Please Enter Valid IP"})
                        if RunningServices.objects.filter(service_name=service_name):
                            return JsonResponse({"status":"error","message": f"There is a Service named {service_name}"})
                        else:

                            service_instance = form.save()

                            service_instance.refresh_from_db()

                            service_instance.update_by=request.user
                            service_instance.update_time = timezone.now()
                            service_instance.save()
                            
                            all_physical_server = PhysicalServer.objects.filter(delete_status=False)
                            all_vm_server = VirtualServer.objects.filter(delete_status=False)

                            all_service_list=[]
                            for i in all_physical_server:
                                if i.service_name.all():
                                    for j in i.service_name.all():
                                        all_service_list.append(j)
                            for i in all_vm_server:
                                if i.service_name.all():
                                    for j in i.service_name.all():
                                        all_service_list.append(j)        
                            #print(all_service_list) 
                            unused_service = RunningServices.objects.filter(delete_status=False).exclude(service_name__in=all_service_list).values()


                            # #all_service = RunningServices.objects.all().values()
                            return JsonResponse({"status":"success","message": f"Service {service_name} has been inserted.","all_service_list": list(unused_service)})
                
                    else:
                        return JsonResponse({"status":"error","message": f"Form is not valid."})
                else:
                    return JsonResponse({"status":"error","message": f"Service Type field is mandatory."})
            else:
                return JsonResponse({"status":"error","message": f"There is a Service named {request.POST['service_name']}"})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def view_service(request):
    if request.method == 'POST':
        if 'show' in request.POST:
            # machine_service = request.POST.get('machine_service')
            service_group = request.POST.getlist('service_group')
            service_type = request.POST.getlist('service_type')
            service_owner = request.POST.getlist('service_owner')
            service_name = request.POST.getlist('service_name')

            if not service_group:
                service_group = ServiceGroup.objects.filter(delete_status=False)
            if not service_type:
                service_type = ServiceType.objects.filter(delete_status=False)

            if not service_owner:
                service_owner = list(RunningServices.objects.filter(delete_status=False).values_list('service_owner', flat=True).distinct())

            if not service_name:
                service_list = RunningServices.objects.filter(delete_status=False, service_type__in=service_type, service_group__in=service_group, service_owner__in=service_owner)
            else:
                service_list= RunningServices.objects.filter(delete_status=False, pk__in=service_name, service_type__in=service_type, service_group__in=service_group, service_owner__in=service_owner)

            # service_list= RunningServices.objects.filter(delete_status=False)
            # if machine_service:
            #     service_list = service_list.exclude(service_type__service_type_name='Machine Identification Service')
            
            if not service_list:
                messages.warning(request,"No data found.")

            service_type = ServiceType.objects.filter(delete_status=False)
            service_group = ServiceGroup.objects.filter(delete_status=False)
            service_owner = RunningServices.objects.filter(delete_status=False).values('service_owner').distinct()
            service_names = RunningServices.objects.filter(delete_status=False)

            context={
                'service_list':service_list,
                'service_types': service_type,
                'service_groups':service_group,
                'service_owner': service_owner,
                'service_names': service_names
            }
            return render(request, 'server/view_service.html', context) 
        
        if 'download' in request.POST:
            # machine_service = request.POST.get('machine_service')
            service_group = request.POST.getlist('service_group')
            service_type = request.POST.getlist('service_type')
            service_owner = request.POST.getlist('service_owner')
            service_name = request.POST.getlist('service_name')

            if not service_group:
                service_group = ServiceGroup.objects.filter(delete_status=False)
            if not service_type:
                service_type = ServiceType.objects.filter(delete_status=False)

            if not service_owner:
                service_owner = list(RunningServices.objects.filter(delete_status=False).values_list('service_owner', flat=True).distinct())


            # service_list= RunningServices.objects.filter(delete_status=False, service_type__in=service_type, service_group__in=service_group, service_owner__in=service_owner)
            if not service_name:
                service_list = RunningServices.objects.filter(delete_status=False, service_type__in=service_type, service_group__in=service_group, service_owner__in=service_owner)
            else:
                service_list= RunningServices.objects.filter(delete_status=False, pk__in=service_name, service_type__in=service_type, service_group__in=service_group, service_owner__in=service_owner)

            # if machine_service:
            #     service_list = service_list.exclude(service_type__service_type_name='Machine Identification Service')
            
            if not service_list:
                messages.warning(request,"No data found.")
                service_type = ServiceType.objects.filter(delete_status=False)
                service_group = ServiceGroup.objects.filter(delete_status=False)
                service_owner = RunningServices.objects.filter(delete_status=False).values('service_owner').distinct()

                context={
                    'service_types': service_type,
                    'service_groups': service_group,
                    'service_owner': service_owner
                }
                return render(request, 'server/view_service.html', context) 

            else:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Service_list.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('sheet 1')
                row_num = 2

                columns = ['SL.', 'Service Name', 'Service Group', 'Service Type', 'Host Server', 'Service IP', 'Service Owner']

                style = xlwt.easyxf('font: bold on,height 320;align: wrap on,vert centre, horiz center;')
                ws.write_merge(0, 1, 0, len(columns)-1, 'Service List', style)

                style_column = xlwt.easyxf('font: bold on;align: wrap on,vert centre, horiz center;')

                for col_num in range(len(columns)):
                    ws.write(2, col_num, columns[col_num], style_column)
                
                font_style = xlwt.easyxf('align: wrap on,vert centre;')
                rows = service_list
                for row in rows:
                    row_num += 1
                    if row.physical_server.all():
                        for serv in row.physical_server.all():
                            host_server = serv.server_name
                    elif row.vm_runs_server.all():
                        for serv in row.vm_runs_server.all():
                            host_server = serv.server_name
                    else:
                        host_server = ''
                    
                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, row.service_name, font_style)
                    ws.write(row_num, 2, row.service_group.service_group_name, font_style)
                    ws.write(row_num, 3, row.service_type.service_type_name, font_style)
                    ws.write(row_num, 4, host_server, font_style)
                    ws.write(row_num, 5, row.service_ip, font_style)
                    ws.write(row_num, 6, row.service_owner, font_style)
                wb.save(response)
                return response

    else:
        service_type = ServiceType.objects.filter(delete_status=False)
        service_group = ServiceGroup.objects.filter(delete_status=False)
        service_owner = RunningServices.objects.filter(delete_status=False).values('service_owner').distinct()
        service_names = RunningServices.objects.filter(delete_status=False)

        context={
            "service_types": service_type,
            'service_groups': service_group,
            'service_owner': service_owner,
            'service_names': service_names
        }
        return render(request, 'server/view_service.html', context) 

@login_required
def view_single_service(request, pk):
    service_details = RunningServices.objects.get(pk=pk,delete_status=False)

    context = {
        'service_details' : service_details,
    }
    return render(request,'server/view_single_service.html', context )

@login_required
def edit_service(request, pk):
    errors=""
    service = get_object_or_404(RunningServices, pk=pk)
    if request.method == 'POST':
        service_edit_form = ServiceEditForm(pk, request.POST, instance=service)
        if service_edit_form.is_valid():
            service_name = service_edit_form.cleaned_data.get('service_name')
            
            # service_exist = RunningServices.objects.filter(Q(service_name=service_name) and ~Q(pk = pk))
            # if not service_exist:
            if service_edit_form.is_valid():
                # if request.POST["monitoring_enabled"]  == 1 and request.POST["service_log_loc"] == None:
                if service_edit_form.cleaned_data.get('monitoring_enabled') == 1 and service_edit_form.cleaned_data.get('service_log_loc') == None:
                    messages.error(request, 'Please enter log directory name when monitor is enabled')
                else:
                    service = service_edit_form.save()
                    service.refresh_from_db()
                    service.update_by = request.user
                    service.update_time = timezone.now()
                    service.save()           
                    messages.success(request, 'Service Successfully Updated.')
                    if service_edit_form.errors:
                        errors = service_edit_form.errors
                    return redirect('view-service')
            # else:
            #     if service_edit_form.errors:
            #         errors = service_edit_form.errors
            #     messages.error(request, f'Service with "{service_name}" already exist.')
    else:
        service_edit_form = ServiceEditForm(pk, instance=service)

    context = {
        'service_edit_form' : service_edit_form,
        'errors':errors

    }
    return render(request, 'server/edit_service.html', context) 

@login_required
def view_server(request):
    server_list = PhysicalServer.objects.filter(delete_status=False).order_by('server_rack_info__location','server_name')
    context={
        "server_list": server_list,
    }
    return render(request, 'server/view_physical_server.html', context) 

@login_required
def export_server_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Server.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Physical Server')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['SL', 'Server Name', 'DC/DR', 'Rack', 'Location in Rack', 'Form Factor', 'OS', 'OS Version', 'Service Name', 'iDrac IP', 'Primary IP', 'Secondary IP', 'Public IP', 'Zone', 'Brand', 'Model', 'Service Tag', 'Asset Tag', 'RAM', 'Proc Core', 'HD Count', 'Total Storage', 'Server Receive Date', 'Warranty Expiry Date', 'Project', 'Vendor', 'Comment', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    dateformate = xlwt.XFStyle()
    dateformate.num_format_str = 'DD-MMM-YYYY'
    wrap_style = xlwt.easyxf('alignment: wrap True')

    rows = PhysicalServer.objects.filter(delete_status=False)

    for row in rows:
        row_num += 1
        service_name_str=""
        rack_info=[]
        counter = 0
        for i in row.service_name.all():
            counter += 1
            if counter < len(row.service_name.all()):
                service_name_str += i.service_name
                service_name_str += "\n"
            else:
                service_name_str += i.service_name
        if row.server_rack_info.all():
            for rackinfo in row.server_rack_info.all():
                rack_info.append(rackinfo)
            rack_info_location=rack_info[0].location
            rack_info_rack=rack_info[0].rack
            rack_info_loc_in_rack=rack_info[0].loc_in_rack
            rack_info_form_factor=rack_info[0].form_factor        
        else:
            dist = {'location':'', 'rack': '', 'loc_in_rack':'', 'form_factor':''}
            rack_info.append(dist)
            rack_info_location=''
            rack_info_rack=''
            rack_info_loc_in_rack=''
            rack_info_form_factor=''

        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, row.server_name, font_style)
        ws.write(row_num, 2, rack_info_location, font_style)
        ws.write(row_num, 3, rack_info_rack, font_style)
        ws.write(row_num, 4, rack_info_loc_in_rack, font_style)
        ws.write(row_num, 5, rack_info_form_factor, font_style)
        ws.write(row_num, 6, row.os_type.os_type, font_style)
        ws.write(row_num, 7, row.os_version.os_version, font_style)
        ws.write(row_num, 8, service_name_str, wrap_style)
        ws.write(row_num, 9, row.idrac_ip, font_style)
        ws.write(row_num, 10, row.primary_ip, font_style)
        ws.write(row_num, 11, row.secondary_ip, font_style)
        ws.write(row_num, 12, row.public_ip, font_style)
        ws.write(row_num, 13, row.zone.zone, font_style)
        ws.write(row_num, 14, row.brand, font_style)
        ws.write(row_num, 15, row.model, font_style)
        ws.write(row_num, 16, row.service_tag, font_style)
        ws.write(row_num, 17, row.asset_code, font_style)
        ws.write(row_num, 18, row.ram, font_style)
        ws.write(row_num, 19, row.processor_core, font_style)
        ws.write(row_num, 20, row.no_of_hdd, font_style)
        ws.write(row_num, 21, row.total_storage, font_style)
        ws.write(row_num, 22, row.server_receive_date, dateformate)
        ws.write(row_num, 23, row.warranty_expiry_date, dateformate)
        # if row.project:
        ws.write(row_num, 24, row.project, font_style)
        
        ws.write(row_num, 25, row.vendor_name, font_style)
        ws.write(row_num, 26, row.comment, font_style)

    wb.save(response)
    return response

@login_required
def view_single_server(request, pk):
    server_details = PhysicalServer.objects.get(pk=pk)
    current_server = []
    current_server.append(server_details.server_name)
    qs_json=""
    servers=[]
    server_rack_qs = ServerRackInfo.objects.get(server=server_details)

    all_servers_in_rack = ServerRackInfo.objects.filter(location=server_rack_qs.location,rack=server_rack_qs.rack)


    # print(server_rack)
    for server in all_servers_in_rack:
        ser_en=[]
        ser_en.append(server.server.server_name)
        ser_en.append(server.rack)
        ser_en.append(server.loc_in_rack)
        ser_en.append(server.form_factor)
        ser_en.append(server.server.id)
        servers.append(ser_en)
    qs_json = json.dumps(servers)
    context = {
        'servers' : qs_json,
        'server_count': len(servers),
        'current_server' : json.dumps(current_server),
        'server': server_details,
    }
    return render(request,'server/view_single_server.html', context )

@login_required
def view_single_vm(request, pk):
    server_details = VirtualServer.objects.get(pk=pk)

    context = {
        'server': server_details,
    }
    return render(request,'server/view_single_vm.html', context )

@login_required
def view_single_rack(request):

    all_servers=PhysicalServer.objects.filter(delete_status=False)
    server_list = []
    if all_servers:
        for all_server in all_servers:
            server_list.append(all_server)
            
    all_racks = ServerRackInfo.objects.filter(server__in=server_list).values_list('location','rack').distinct().order_by('location','rack')
    print(all_racks)
    qs_json=""
    servers=[]
    if request.method == 'POST':

        if not request.POST.getlist('server_rack') or 'all' in request.POST.getlist('server_rack'):
            selected_rack=all_racks
        else:

            selected_rack=request.POST.getlist('server_rack')
            
        
        for srack in selected_rack:
            if isinstance(srack, str):
                srack = srack.replace('(', '').replace(')', '').replace('\'', '').split(', ')
            server_in=[]
            location = srack[0]
            rack = srack[1]
            server_rack = ServerRackInfo.objects.filter(location = location, rack=rack,server__in=server_list).order_by('location','rack')

            for server in server_rack:
                ser_en=[]
                ser_en.append(server.server.server_name)
                ser_en.append(server.rack)
                ser_en.append(server.loc_in_rack)
                ser_en.append(server.form_factor)
                ser_en.append(server.server.id)
                ser_en.append(server.get_location_display())
                # ser_en.append(server.server_run_status)

                server_in.append(ser_en)
            servers.append(server_in)
        qs_json = json.dumps(servers)
        # print(qs_json)
    context = {
        'servers' : qs_json,
        'server_count': len(servers),
        'n' : range(42),
        'all_racks': all_racks,
    }
    return render(request,'server/view_single_rack.html', context)

@login_required
def add_vm_loc(request):
    if request.method == 'POST':
        if request.POST["vm_loc"] != "":
            vm_loc = request.POST["vm_loc"]
            print(vm_loc)
            if VMLocationType.objects.filter(container=vm_loc):
                return JsonResponse({"status":"error","message": f"There is a VM Location Type named {vm_loc}"})
            else:
                vm_loc_instance = VMLocationType(container=vm_loc, update_by=request.user, update_time=timezone.now())
                vm_loc_instance.save()
                all_vm_loc = VMLocationType.objects.filter(delete_status=False).values()
                # print(list(all_vm_loc))
                return JsonResponse({"status":"success","message": f"VM Location Type {vm_loc} has been created.","all_vm_loc": list(all_vm_loc)}) 
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def add_vm(request):
    if request.method == 'POST':
        vm_add_form = VMAddForm(request.POST)
        service_add_form = ServiceAddForm()
        if vm_add_form.is_valid():
            new_server = vm_add_form.save() 
            new_server.refresh_from_db()
            new_server.update_by = request.user
            new_server.update_time = timezone.now()
            new_server.server_type = "VM"
            new_server.save()
            messages.success(request, 'New VM Has been Added Successfully!')
            return redirect('add-vm')

    else:
        vm_add_form = VMAddForm()
        service_add_form = ServiceAddForm()

    context = {
        'server_add_form' : vm_add_form,
        'service_add_form' : service_add_form,
    }
    return render(request, 'server/add_virtual_server.html', context) 

@login_required
def view_vm(request):
    vm_list = VirtualServer.objects.filter(delete_status=False)
    context={
        "server_list": vm_list,
    }
    return render(request, 'server/view_vm.html', context) 

def export_vm_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="VM.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('vm')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['SL', 'Server Name', 'DC/DR', 'Location Type', 'Location', 'OS', 'OS Version', 'Service Name',  'Primary IP', 'Secondary IP', 'Public IP', 'Zone', 'RAM', 'Proc Core', 'HD Count', 'Total Storage', 'Comment', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    # dateformate = xlwt.XFStyle()
    # dateformate.num_format_str = 'DD-MMM-YYYY'
    wrap_style = xlwt.easyxf('alignment: wrap True')

    rows = VirtualServer.objects.filter(delete_status=False)

    for row in rows:
        row_num += 1
        service_name_str=""
        counter = 0
        for i in row.service_name.all():
            counter += 1
            if counter < len(row.service_name.all()):
                service_name_str += i.service_name
                service_name_str += "\n"
            else:
                service_name_str += i.service_name
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, row.server_name, font_style)
        ws.write(row_num, 2, row.location, font_style)
        ws.write(row_num, 3, row.vm_location_type.container, font_style)
        ws.write(row_num, 4, row.vm_location, font_style)
        ws.write(row_num, 5, row.os_type.os_type, font_style)
        ws.write(row_num, 6, row.os_version.os_version, font_style)
        ws.write(row_num, 7, service_name_str, wrap_style)
        ws.write(row_num, 8, row.primary_ip, font_style)
        ws.write(row_num, 9, row.secondary_ip, font_style)
        ws.write(row_num, 10, row.public_ip, font_style)
        ws.write(row_num, 11, row.zone.zone, font_style)
        ws.write(row_num, 12, row.ram, font_style)
        ws.write(row_num, 13, row.processor_core, font_style)
        ws.write(row_num, 14, row.no_of_hdd, font_style)
        ws.write(row_num, 15, row.total_storage, font_style)
        ws.write(row_num, 16, row.comment, font_style)

    wb.save(response)
    return response

@login_required
def edit_vm(request, pk):
    server = get_object_or_404(VirtualServer, pk=pk)
    if request.method == 'POST':
        server_add_form = VMEditForm(pk, request.POST, instance=server)
        service_add_form = ServiceAddForm()
        if server_add_form.is_valid():

            server = server_add_form.save() 
            # service_from_form = server_add_form.cleaned_data['service_name']

            # # services = RunningServices.objects.filter(service_name__in=service_from_form)
            # print(service_from_form)
            # server.service_name.set(service_from_form)
            server.refresh_from_db()
            server.update_by = request.user
            server.update_time = timezone.now()
            server.server_type = "VM"
            server.save()
            messages.success(request, 'Server info Successfully Updated.')
            return redirect('view-vm')

    else:
        server_add_form = VMEditForm(pk,instance=server)
        service_add_form = ServiceAddForm()


    context = {
        'server_add_form' : server_add_form,
        'service_add_form' : service_add_form,
        'server':server,

    }
    return render(request, 'server/edit_virtual_server.html', context)

@login_required
def server_report(request):
    os_types = OsType.objects.filter(delete_status=False)
    service_types = ServiceType.objects.filter(delete_status=False)
    zones = Zone.objects.filter(delete_status=False)
    location_list = ServerRackInfo.objects.all().values_list('location', flat=True).distinct().order_by('location')
    # racks = ServerRackInfo.objects.all().values_list('rack', flat=True).distinct().order_by('rack')
    if request.method == 'POST':
        server_type=request.POST.getlist('server_type')

        os_type=request.POST.getlist('os_type')
        print(server_type,os_type)

        if not os_type or 'all' in os_type:
            os_type_object = OsType.objects.filter(delete_status=False)
        else:
            os_type_object = OsType.objects.filter(delete_status=False, os_type__in=os_type)

        service_type = request.POST.getlist('service_type')
        if not service_type or 'all' in service_type:
            # service_types_object = ServiceType.objects.filter(delete_status=False)
            service_types_object = RunningServices.objects.filter(delete_status=False)
        else:
            service_types_object = RunningServices.objects.filter(delete_status=False, service_type__service_type_name__in =service_type)
        zone = request.POST.getlist('zone')
        if not zone or 'all' in zone:
            zone_object = Zone.objects.filter(delete_status=False)
        else:
            zone_object = Zone.objects.filter(delete_status=False, zone__in = zone)

        location = request.POST.getlist('location')
        if not location or 'all' in location:
            rack_object = ServerRackInfo.objects.all()
        else:
            rack_object = ServerRackInfo.objects.filter(location__in=location)

        vm_location = list()
        if 'all' in location or not location:
            vm_location = ['dc','dr']
        else:
            vm_location = location
        # rack = request.POST.getlist('rack')
        # if not rack or 'all' in rack:
        #     rack_object = ServerRackInfo.objects.all()
        # else:
        #     rack_object = ServerRackInfo.objects.filter(rack__in=rack)

        if 'show' in request.POST:
            if not server_type or ('all' in server_type) or ('physical_server' in server_type and 'virtual_server' in server_type) :
                physical_server_list = PhysicalServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object) & Q(server_rack_info__in=rack_object)).distinct()

                # print(physical_server_list)
                
                # if not rack or 'all' in rack:

                virtual_server_list = VirtualServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object) & Q(location__in=vm_location)).distinct()
                print(virtual_server_list)

                server_list_merge_query =[]
                for i in range(0, len(physical_server_list)):
                    server_list_merge_query.append(physical_server_list[i])

                # if not rack or 'all' in rack:
                for i in range(0, len(virtual_server_list)):
                    server_list_merge_query.append(virtual_server_list[i])

                context = {
                    'os_types':os_types,
                    'service_types':service_types,
                    'zones':zones,
                    # 'racks':racks,
                    'locations':location_list,
                    'server_list_merge_query': server_list_merge_query,
                }

                return render(request, 'server/server_report.html',context)
            elif 'physical_server' in server_type and 'virtual_server' not in server_type:
                physical_server_list = PhysicalServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object) & Q(server_rack_info__in=rack_object)).distinct()

                server_list_merge_query =[]
                for i in range(0, len(physical_server_list)):
                    server_list_merge_query.append(physical_server_list[i])

                context = {
                    'os_types':os_types,
                    'service_types':service_types,
                    'zones':zones,
                    # 'racks':racks,
                    'only_physical':"only_physical",
                    'locations':location_list,
                    'server_list_merge_query': server_list_merge_query,
                }
                return render(request, 'server/server_report.html',context) 
            elif 'virtual_server' in server_type and 'physical_server' not in server_type:
                virtual_server_list = VirtualServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object) & Q(location__in=vm_location)).distinct()

                server_list_merge_query =[]
                for i in range(0, len(virtual_server_list)):
                    server_list_merge_query.append(virtual_server_list[i])

                context = {
                    'os_types':os_types,
                    'service_types':service_types,
                    'zones':zones,
                    # 'racks':racks,
                    'only_vm':"only_vm",
                    'locations':location,
                    'server_list_merge_query': server_list_merge_query,
                }
                return render(request, 'server/server_report.html',context) 
        
        elif 'download' in request.POST:
            if not server_type or ('all' in server_type) or ('physical_server' in server_type and 'virtual_server' in server_type) :
                physical_server_list = PhysicalServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object) & Q(server_rack_info__in=rack_object)).distinct()
                
                # if not rack or 'all' in rack:
                virtual_server_list = VirtualServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object)).distinct()

                server_list_merge_query =[]
                for i in range(0, len(physical_server_list)):
                    server_list_merge_query.append(physical_server_list[i])

                # if not rack or 'all' in rack:
                for i in range(0, len(virtual_server_list)):
                    server_list_merge_query.append(virtual_server_list[i])

                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Server_Report.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Server Report')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['SL', 'Server Name', 'Server Type', 'OS', 'OS Version', 'Service Name',  'Primary IP',  'Secondary IP', 'Public IP', 'Zone', 'RAM', 'Total Storage',]

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                # dateformate = xlwt.XFStyle()
                # dateformate.num_format_str = 'DD-MMM-YYYY'
                wrap_style = xlwt.easyxf('alignment: wrap True')

                rows = server_list_merge_query

                for row in rows:
                    row_num += 1
                    service_name_str=""
                    counter = 0
                    for i in row.service_name.all():
                        counter += 1
                        if counter < len(row.service_name.all()):
                            service_name_str += i.service_name
                            service_name_str += "\n"
                        else:
                            service_name_str += i.service_name  

                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, row.server_name, font_style)
                    ws.write(row_num, 2, row.server_type, font_style)
                    ws.write(row_num, 3, row.os_type.os_type, font_style)
                    ws.write(row_num, 4, row.os_version.os_version, font_style)
                    ws.write(row_num, 5, service_name_str, wrap_style)
                    ws.write(row_num, 6, row.primary_ip, font_style)
                    ws.write(row_num, 7, row.secondary_ip, font_style)
                    ws.write(row_num, 8, row.public_ip, font_style)
                    ws.write(row_num, 9, row.zone.zone, font_style)
                    ws.write(row_num, 10, row.ram, font_style)
                    ws.write(row_num, 11, row.total_storage, font_style)

                wb.save(response)
                return response
            elif 'physical_server' in server_type and 'virtual_server' not in server_type:
                physical_server_list = PhysicalServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object) & Q(server_rack_info__in=rack_object)).distinct()

                server_list_merge_query =[]
                for i in range(0, len(physical_server_list)):
                    server_list_merge_query.append(physical_server_list[i])

                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Server_Report.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Server Report')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['SL', 'Server Name', 'Server Type', 'DC/DR','Rack', 'Location in Rack', 'Form Factor', 'OS', 'OS Version', 'Service Name', 'Primary IP',  'Secondary IP', 'Public IP', 'Zone', 'RAM', 'Total Storage',]

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                # dateformate = xlwt.XFStyle()
                # dateformate.num_format_str = 'DD-MMM-YYYY'
                wrap_style = xlwt.easyxf('alignment: wrap True')

                rows = server_list_merge_query

                for row in rows:
                    row_num += 1
                    service_name_str=""
                    rack_info=[]
                    counter = 0
                    for i in row.service_name.all():
                        counter += 1
                        if counter < len(row.service_name.all()):
                            service_name_str += i.service_name
                            service_name_str += "\n"
                        else:
                            service_name_str += i.service_name  
                    for rackinfo in row.server_rack_info.all():
                        rack_info.append(rackinfo)
                    print(rack_info[0].rack)

                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, row.server_name, font_style)
                    ws.write(row_num, 2, row.server_type, font_style)
                    ws.write(row_num, 3, rack_info[0].location, font_style)
                    ws.write(row_num, 4, rack_info[0].rack, font_style)
                    ws.write(row_num, 5, rack_info[0].loc_in_rack, font_style)
                    ws.write(row_num, 6, rack_info[0].form_factor, font_style)
                    ws.write(row_num, 7, row.os_type.os_type, font_style)
                    ws.write(row_num, 8, row.os_version.os_version, font_style)
                    ws.write(row_num, 9, service_name_str, wrap_style)
                    ws.write(row_num, 10, row.primary_ip, font_style)
                    ws.write(row_num, 11, row.secondary_ip, font_style)
                    ws.write(row_num, 12, row.public_ip, font_style)
                    ws.write(row_num, 13, row.zone.zone, font_style)
                    ws.write(row_num, 14, row.ram, font_style)
                    ws.write(row_num, 15, row.total_storage, font_style)

                wb.save(response)
                return response
            elif 'virtual_server' in server_type and 'physical_server' not in server_type:
                virtual_server_list = VirtualServer.objects.filter(Q(delete_status=False) & Q(os_type__in=os_type_object) & Q(service_name__in=service_types_object) & Q(zone__in=zone_object)).distinct()

                server_list_merge_query =[]
                for i in range(0, len(virtual_server_list)):
                    server_list_merge_query.append(virtual_server_list[i])

                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Server_Report.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Server Report')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['SL', 'Server Name', 'Server Type', 'OS', 'OS Version', 'Service Name', 'Service Type', 'Primary IP',  'Secondary IP', 'Public IP', 'Zone', 'RAM', 'Total Storage',]

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                # dateformate = xlwt.XFStyle()
                # dateformate.num_format_str = 'DD-MMM-YYYY'
                wrap_style = xlwt.easyxf('alignment: wrap True')

                rows = server_list_merge_query

                for row in rows:
                    row_num += 1
                    service_name_str=""
                    counter = 0
                    for i in row.service_name.all():
                        counter += 1
                        if counter < len(row.service_name.all()):
                            service_name_str += i.service_name
                            service_name_str += "\n"
                        else:
                            service_name_str += i.service_name  

                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, row.server_name, font_style)
                    ws.write(row_num, 2, row.server_type, font_style)
                    ws.write(row_num, 3, row.os_type.os_type, font_style)
                    ws.write(row_num, 4, row.os_version.os_version, font_style)
                    ws.write(row_num, 5, service_name_str, wrap_style)
                    ws.write(row_num, 6, row.primary_ip, font_style)
                    ws.write(row_num, 7, row.secondary_ip, font_style)
                    ws.write(row_num, 8, row.public_ip, font_style)
                    ws.write(row_num, 9, row.zone.zone, font_style)
                    ws.write(row_num, 10, row.ram, font_style)
                    ws.write(row_num, 11, row.total_storage, font_style)

                wb.save(response)
                return response

    context = {
        'os_types':os_types,
        'service_types':service_types,
        'zones':zones,
        # 'racks':racks,
        'locations':location_list,
    }

    return render(request, 'server/server_report.html',context)



