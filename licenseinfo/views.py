from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.formats import localize
from django.db.models import Q, Sum
import xlwt
from licenseinfo.forms import LicenseAddForm, LicenseEditForm, M365AddForm
from licenseinfo.models import LicenseInfo, LicenseType, M365License
# Create your views here.
@login_required
def insert_license(request):
    if request.method == 'POST':
        license_add_form = LicenseAddForm(request.POST)

        if license_add_form.is_valid():
            new_license = license_add_form.save()
            new_license.refresh_from_db()
            if new_license.end_date <= timezone.now():
                new_license.license_status = False
            new_license.created_by = request.user
            new_license.update_by = request.user

            new_license.save()
            messages.success(request, 'License info Has been Added Successfully!')
            return redirect('insert-license')
    else:
        license_add_form = LicenseAddForm()
        context = {
            'license_add_form' : license_add_form,
        }
        return render(request, 'server/license/license_add.html', context)

@login_required
def view_license(request):
    if request.method == 'POST':
        if 'show' in request.POST:
            l_type = request.POST.getlist('l_type')
            l_validity = request.POST.getlist('l_validity')

            if not l_type:
                l_type = LicenseType.objects.filter(delete_status=False)

            if not l_validity:
                l_validity = [0,1]

            licenses = LicenseInfo.objects.filter(delete_status=False, license_type__in=l_type, license_status__in=l_validity).order_by('license_type')

            if not licenses:
                messages.warning(request,"No data found.")

            license_type = LicenseType.objects.filter(delete_status=False)
            context={
                'license_type':license_type,
                'licenses':licenses
            }
            return render(request, 'server/license/license_view.html',context)

        if 'download' in request.POST:
            l_type = request.POST.get('l_type')
            l_validity = request.POST.get('l_validity')

            if not l_type:
                l_type = LicenseType.objects.filter(delete_status=False)

            if not l_validity:
                l_validity = [0,1]

            licenses = LicenseInfo.objects.filter(delete_status=False, license_type__in=l_type, license_status__in=l_validity).order_by('license_type')

            if not licenses:
                messages.warning(request,"No data found.")
                license_type = LicenseType.objects.filter(delete_status=False)
                context={
                    # 're_form':LicenseFilterForm(),
                    'license_type':license_type
                }
                return render(request, 'server/license/license_view.html', context) 
            else:
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="license_info.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('sheet 1')
                row_num = 2

                columns = ['SL.', 'License Name', 'License Number', 'Effective Quantity', 'License Type', 'Service Name', 'Service Group', 'Start Date', 'End Date', 'Validity']

                style = xlwt.easyxf('font: bold on,height 320;align: wrap on,vert centre, horiz center;')
                ws.write_merge(0, 1, 0, len(columns)-1, 'License Information', style)

                style_column = xlwt.easyxf('font: bold on;align: wrap on,vert centre, horiz center;')

                for col_num in range(len(columns)):
                    ws.write(2, col_num, columns[col_num], style_column)
                
                font_style = xlwt.easyxf('align: wrap on,vert centre;')
                rows = licenses
                for row in rows:
                    row_num += 1
                    local_start = localize(timezone.localtime(row.start_date))
                    local_end = localize(timezone.localtime(row.end_date))
                    if row.license_status == 1:
                        license_status = 'Valid'
                    else:
                        license_status = 'Expired'

                    if row.service_name:
                        service_name = row.service_name.service_name
                    else:
                        service_name = ''
                    if row.service_group:
                        service_group = row.service_group.service_group_name
                    else:
                        service_group = ''
                    
                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, row.license_name, font_style)
                    ws.write(row_num, 2, row.license_number, font_style)
                    ws.write(row_num, 3, row.effective_quantity, font_style)
                    ws.write(row_num, 4, row.license_type.type_name, font_style)
                    ws.write(row_num, 5, service_name, font_style)
                    ws.write(row_num, 6, service_group, font_style)
                    ws.write(row_num, 7, local_start, font_style)
                    ws.write(row_num, 8, local_end, font_style)
                    ws.write(row_num, 9, license_status, font_style)
                wb.save(response)
                return response

    else:
        license_type = LicenseType.objects.filter(delete_status=False)

        context={
            # 're_form':LicenseFilterForm(),
            'license_type':license_type
        }
        return render(request, 'server/license/license_view.html', context) 

@login_required
def download_license_list(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="license_info.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet 1')
    row_num = 2

    columns = ['SL.', 'License Name', 'License Number', 'Effective Quantity', 'License Type', 'Service Name', 'Service Group', 'Start Date', 'End Date']

    style = xlwt.easyxf('font: bold on,height 320;align: wrap on,vert centre, horiz center;')
    ws.write_merge(0, 1, 0, len(columns)-1, 'License Information', style)

    style_column = xlwt.easyxf('font: bold on;align: wrap on,vert centre, horiz center;')

    for col_num in range(len(columns)):
        ws.write(2, col_num, columns[col_num], style_column)
    
    font_style = xlwt.easyxf('align: wrap on,vert centre;')
    rows = LicenseInfo.objects.filter(delete_status=False)
    for row in rows:
        row_num += 1
        local_start = localize(timezone.localtime(row.start_date))
        local_end = localize(timezone.localtime(row.end_date))
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, row.license_name, font_style)
        ws.write(row_num, 2, row.license_number, font_style)
        ws.write(row_num, 3, row.effective_quantity, font_style)
        ws.write(row_num, 4, row.license_type.type_name, font_style)
        ws.write(row_num, 5, row.service_name, font_style)
        ws.write(row_num, 6, row.service_group, font_style)
        ws.write(row_num, 7, local_start, font_style)
        ws.write(row_num, 8, local_end, font_style)
    wb.save(response)
    return response
        
@login_required
def add_license_type(request):
    if request.method == 'POST':
        if request.POST["license_type"] != "":
            license_type = request.POST["license_type"]
            if LicenseType.objects.filter(type_name=license_type):
                return JsonResponse({"status":"error","message": f"There is a License Type named {license_type}"})
            else:
                os_instance = LicenseType(type_name=license_type)
                os_instance.save()
                all_license_type = LicenseType.objects.filter(delete_status=False).values()
                # print(list(all_os))
                return JsonResponse({"status":"success","message": f"License Type {license_type} has been created.","all_license_type": list(all_license_type)})
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})  

@login_required
def view_license_summary(request):
    licenses = LicenseInfo.objects.filter(delete_status=False, license_status=True ).values('license_type__type_name').order_by('license_type__type_name').annotate(total=Sum('effective_quantity'))

    context ={
        'licenses':licenses
    }
    return render(request, 'server/license/license_summary_view.html', context) 

@login_required
def download_license_summary(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="license_summary_report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet 1')
    row_num = 2
    sl_counter = 0

    columns = ['SL.', 'License Type', 'Total Quantity']

    style = xlwt.easyxf('font: bold on,height 200;align: wrap on,vert centre, horiz center;')
    ws.write_merge(0, 1, 0, len(columns)-1, 'License Information Summary', style)

    style_column = xlwt.easyxf('font: bold on;align: wrap on,vert centre, horiz center;')

    for col_num in range(len(columns)):
        ws.write(2, col_num, columns[col_num], style_column)
    
    font_style = xlwt.easyxf('align: wrap on,vert centre;')
    # rows = LicenseInfo.objects.filter(Q(delete_status=False) & Q(end_date=None) | Q(end_date__gte=timezone.now())).values('license_type__type_name').order_by('license_type__type_name').annotate(total=Sum('effective_quantity'))
    rows = LicenseInfo.objects.filter(delete_status=False, license_status=True ).values('license_type__type_name').order_by('license_type__type_name').annotate(total=Sum('effective_quantity'))
    # print(rows)
    for row in rows:
        print(row)
        row_num += 1
        sl_counter += 1
        ws.write(row_num, 0, sl_counter, font_style)
        ws.write(row_num, 1, row['license_type__type_name'], font_style)
        ws.write(row_num, 2, row['total'], font_style)
    wb.save(response)
    return response

@login_required
def edit_license(request, pk):
    license = get_object_or_404(LicenseInfo, pk=pk)
    if request.method == 'POST':
        license_edit_form = LicenseEditForm(pk, request.POST, instance=license)
        if license_edit_form.is_valid():
            license_ins = license_edit_form.save()
            license_ins.refresh_from_db()
            if license_ins.end_date <= timezone.now():
                license_ins.license_status = False
            if license_ins.end_date >= timezone.now():
                license_ins.license_status = True
            license_ins.update_by = request.user
            license_ins.save()
            messages.success(request, 'License info Has been Updated Successfully!')

            return redirect('view-license')

    else:
        license_edit_form = LicenseEditForm(pk, instance=license)

    context = {
        'license_edit_form' : license_edit_form,
    }
    return render(request, 'server/license/license_edit.html', context) 

@login_required
def add_m365_license(request):
    if request.method == 'POST':
        m365_add_form = M365AddForm(request.POST)

        if m365_add_form.is_valid():
            try:
                new_license = m365_add_form.save()
                new_license.refresh_from_db()
                new_license.created_by = request.user
                new_license.update_by = request.user

                new_license.save()
                messages.success(request, 'License info Has been Added Successfully!')
                return redirect('add-m365-license')
            except Exception as e:
                messages.error(request, e)
                context = {
                    'license_add_form' : m365_add_form,
                }
                return render(request, 'server/license/m365_add.html', context)
        else:
            context = {
                'license_add_form' : m365_add_form,
            }
            return render(request, 'server/license/m365_add.html', context)
    else:
        m365_add_form = M365AddForm()
        context = {
            'license_add_form' : m365_add_form,
        }
        return render(request, 'server/license/m365_add.html', context)
    
def view_m365_license(request):

    licenses = M365License.objects.filter(delete_status=False).order_by('branch')

    if not licenses:
        messages.warning(request,"No data found.")

    total_used_license = LicenseType.objects.filter(delete_status=False).count()
    context={
        'total_used_license':total_used_license,
        'licenses':licenses
    }
    return render(request, 'server/license/m365_view.html', context) 

    # if request.method == 'POST':
    #     if 'show' in request.POST:
    #         l_type = request.POST.getlist('l_type')
    #         l_validity = request.POST.getlist('l_validity')

    #         if not l_type:
    #             l_type = LicenseType.objects.filter(delete_status=False)

    #         if not l_validity:
    #             l_validity = [0,1]

    #         licenses = LicenseInfo.objects.filter(delete_status=False, license_type__in=l_type, license_status__in=l_validity).order_by('license_type')

    #         if not licenses:
    #             messages.warning(request,"No data found.")

    #         license_type = LicenseType.objects.filter(delete_status=False)
    #         context={
    #             'license_type':license_type,
    #             'licenses':licenses
    #         }
    #         return render(request, 'server/license/license_view.html',context)

    #     if 'download' in request.POST:
    #         l_type = request.POST.get('l_type')
    #         l_validity = request.POST.get('l_validity')

    #         if not l_type:
    #             l_type = LicenseType.objects.filter(delete_status=False)

    #         if not l_validity:
    #             l_validity = [0,1]

    #         licenses = LicenseInfo.objects.filter(delete_status=False, license_type__in=l_type, license_status__in=l_validity).order_by('license_type')

    #         if not licenses:
    #             messages.warning(request,"No data found.")
    #             license_type = LicenseType.objects.filter(delete_status=False)
    #             context={
    #                 # 're_form':LicenseFilterForm(),
    #                 'license_type':license_type
    #             }
    #             return render(request, 'server/license/license_view.html', context) 
    #         else:
    #             response = HttpResponse(content_type='application/ms-excel')
    #             response['Content-Disposition'] = 'attachment; filename="license_info.xls"'

    #             wb = xlwt.Workbook(encoding='utf-8')
    #             ws = wb.add_sheet('sheet 1')
    #             row_num = 2

    #             columns = ['SL.', 'License Name', 'License Number', 'Effective Quantity', 'License Type', 'Service Name', 'Service Group', 'Start Date', 'End Date', 'Validity']

    #             style = xlwt.easyxf('font: bold on,height 320;align: wrap on,vert centre, horiz center;')
    #             ws.write_merge(0, 1, 0, len(columns)-1, 'License Information', style)

    #             style_column = xlwt.easyxf('font: bold on;align: wrap on,vert centre, horiz center;')

    #             for col_num in range(len(columns)):
    #                 ws.write(2, col_num, columns[col_num], style_column)
                
    #             font_style = xlwt.easyxf('align: wrap on,vert centre;')
    #             rows = licenses
    #             for row in rows:
    #                 row_num += 1
    #                 local_start = localize(timezone.localtime(row.start_date))
    #                 local_end = localize(timezone.localtime(row.end_date))
    #                 if row.license_status == 1:
    #                     license_status = 'Valid'
    #                 else:
    #                     license_status = 'Expired'

    #                 if row.service_name:
    #                     service_name = row.service_name.service_name
    #                 else:
    #                     service_name = ''
    #                 if row.service_group:
    #                     service_group = row.service_group.service_group_name
    #                 else:
    #                     service_group = ''
                    
    #                 ws.write(row_num, 0, row_num, font_style)
    #                 ws.write(row_num, 1, row.license_name, font_style)
    #                 ws.write(row_num, 2, row.license_number, font_style)
    #                 ws.write(row_num, 3, row.effective_quantity, font_style)
    #                 ws.write(row_num, 4, row.license_type.type_name, font_style)
    #                 ws.write(row_num, 5, service_name, font_style)
    #                 ws.write(row_num, 6, service_group, font_style)
    #                 ws.write(row_num, 7, local_start, font_style)
    #                 ws.write(row_num, 8, local_end, font_style)
    #                 ws.write(row_num, 9, license_status, font_style)
    #             wb.save(response)
    #             return response

    # else:
    #     license_type = LicenseType.objects.filter(delete_status=False)

    #     context={
    #         # 're_form':LicenseFilterForm(),
    #         'license_type':license_type
    #     }
    #     return render(request, 'server/license/license_view.html', context) 



def delete_m365_license(request):
    if request.method == 'POST':
        if request.POST["license_id"]:
            license_id = request.POST["license_id"]
            license_ins = get_object_or_404(M365License, pk=license_id)
            print('ok')
            if license_ins:
                if license_ins.created_by != request.user:
                    return JsonResponse({"status":"error","message": f"You are not authorized to delete the license entry."})  
                license_ins.delete_status = True
                license_ins.deleted_date = timezone.now()
                license_ins.deleted_by = request.user
                license_ins.save()
                return JsonResponse({"status":"success","message": f"License info Has been deleted Successfully!"})
                #messages.success(request, 'License info Has been deleted Successfully!')
                #return redirect('view-m365-license')

        else:
            return JsonResponse({"status":"error","message": f"Something went wrong. Contact with adminstrator."}) 