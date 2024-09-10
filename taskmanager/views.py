from cmath import log
from datetime import datetime, timedelta
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils import timezone, dateformat
import xlwt
from django.db.models import Sum, Count

# import plotly.express as px

from knowledgebase.models import KnowledgeBase
from authentication.models import CustomUser
from .models import TaskManager, TaskHistory, TaskStepComentary, TaskType
from .forms import TMCreateForm, PrivateTMCreateForm, TaskReportForm
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied

from .sendMail import SendMail
from incidence_log.views import update_incidence_status
# Create your views here.

@login_required
def task_create(request):
    user = request.user
    if request.method == 'POST':
        task_add_form = TMCreateForm(request.POST)
        
        if task_add_form.is_valid():
            due_date = task_add_form.cleaned_data['due_date']
            ref_task = task_add_form.cleaned_data['reference_task']
            users = task_add_form.cleaned_data['assigned_to']
            task_status = task_add_form.cleaned_data['task_status']
            
            new_task = task_add_form.save()
            new_task.refresh_from_db()
            new_task.task_visibility = 1 # 1 for public, 2 for private 
            new_task.task_status = task_status
            if task_status == '2':
                new_task.completed_date = timezone.now()
            new_task.created_by = request.user
            new_task.created_at = timezone.now()
            new_task.save()

            history = TaskHistory(task=new_task,new_task_add=1,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
            history.save()

            history = TaskHistory(task=new_task,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()
            history.refresh_from_db()
            history.assigned_to.set(users)
            # history.assigned_by = request.user
            history.assigned_by = task_add_form.cleaned_data['assigned_by']
            history.save()

            history = TaskHistory(task=new_task,due_date=1,effective_date=due_date,insert_date=timezone.now(),insert_by=request.user)
            history.save()

            history = TaskHistory(task=new_task,changed_status=task_status,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()

            if ref_task:
                history = TaskHistory(task=ref_task,sub_task_add=new_task,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
                history.save()

                history = TaskHistory(task=new_task,ref_task_add=ref_task,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
                history.save()

            messages.success(request, 'New Task Has been Added Successfully!')

            ###########     Mail Sending          ################

            # all_user = CustomUser.objects.filter(is_active=1)
            # to_email = []
            # for i in new_task.:
            #     all_email.append(i.email)
            # message = render_to_string('mail_format/meeting-close-sent-mail-template.html', {
            #     'meetings': meetings,
            # }) 
            # subject = 'Meeting ' + str(meetings.number) + 'has been closed'    
            # email = EmailMessage(subject,message,settings.EMAIL_HOST_USER,all_email)
            # file_to_be_sent = os.path.join(settings.BASE_DIR, filename_2)
            # email.attach_file(file_to_be_sent)
            # email.content_subtype = "html" 
            # email.send()  
            ###########     Mail Sending          ################

            return redirect('add-task')

    else:
        task_add_form = TMCreateForm()


    context = {
        'task_add_form' : task_add_form,

    }
    return render(request, 'server/taskmanager/task_add.html', context) 


@login_required
def private_task_create(request):
    if request.method == 'POST':
        task_add_form = PrivateTMCreateForm(request.POST)
        
        if task_add_form.is_valid():
            due_date = task_add_form.cleaned_data['due_date']
            ref_task = task_add_form.cleaned_data['reference_task']
            # users = task_add_form.cleaned_data['assigned_to']
            

            new_task = task_add_form.save()
            new_task.refresh_from_db()
            new_task.task_visibility = 2 # 1 for public, 2 for private 
            new_task.assigned_to.add(request.user)
            new_task.assigned_by = request.user
            new_task.created_by = request.user
            new_task.created_at = timezone.now()
            new_task.save()

            history = TaskHistory(task=new_task,new_task_add=1,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
            history.save()

            # user_email = []
            # for user in users:
            #     user_email.append(user.email)
            # mail = SendMail()
            # subject = 'Task Assigned to you'
            # message = f"Task T-{new_task.id} ({new_task.task_title}) assigned to you.\nPlease login to portal for details."
            # mail.send(user_email, subject, message)

            history = TaskHistory(task=new_task,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()
            history.refresh_from_db()
            history.assigned_to.add(request.user)
            history.assigned_by = request.user
            history.save()

            history = TaskHistory(task=new_task,due_date=1,effective_date=due_date,insert_date=timezone.now(),insert_by=request.user)
            history.save()

            if ref_task:
                history = TaskHistory(task=ref_task,sub_task_add=new_task,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
                history.save()

                history = TaskHistory(task=new_task,ref_task_add=ref_task,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
                history.save()

            messages.success(request, 'New Task Has been Added Successfully!')
            return redirect('add-private-task')

    else:
        task_add_form = PrivateTMCreateForm()


    context = {
        'task_add_form' : task_add_form,

    }
    return render(request, 'server/taskmanager/task_add_private.html', context) 

@login_required
def task_list(request):
    task_lists = TaskManager.objects.filter(Q(delete_status=False) & ((Q(task_visibility=2) & Q(created_by=request.user)) | Q(task_visibility=1))).order_by('task_status','due_date')
    # today = timezone.now()

    context={
        "task_lists": task_lists,
        # "today":today
    }
    return render(request, 'server/taskmanager/view_task_list.html', context) 

@login_required
def task_view(request,pk):
    try:
        task_details = TaskManager.objects.get(pk=pk,delete_status=False)
    except:
        raise Http404("Selected task not found.")

    if task_details.task_visibility == 2 and task_details.created_by != request.user:
        raise PermissionDenied("You have no permission to view this task.")

    # kb_lists= KnowledgeBase.objects.filter( Q(status = 'published') | (Q(status = 'draft') | Q(status = 'protected') & Q(author = request.user)) ).order_by('-created_at')
    kb_lists= KnowledgeBase.objects.filter(status = 'published').order_by('-created_at')

    sub_tasks = TaskManager.objects.filter(reference_task=task_details)
    task_histories = TaskHistory.objects.filter(task=task_details).order_by('-effective_date')
    all_users = CustomUser.objects.filter(is_active=1)
    all_tasks = TaskManager.objects.filter(delete_status=False)
    context={
        "task_details": task_details,
        "sub_tasks" : sub_tasks,
        "task_histories" : task_histories,
        "all_users" : all_users,
        "all_tasks" : all_tasks,
        "kb_lists" : kb_lists
    }
    return render(request, 'server/taskmanager/view_single_task.html', context)

def get_summary_report(task_query):
    task_query = task_query.values('assigned_to__email','assigned_to__first_name','assigned_to__last_name','task_type__type').annotate(total_tasks=Count('task_type')).order_by('assigned_to__email','task_type__type')

    print(task_query)

    mydict = dict()
    task_types = set()
    for entry in task_query:
        full_name = f"{entry['assigned_to__first_name']} {entry['assigned_to__last_name']}"
        email = entry['assigned_to__email']
        task_type = entry['task_type__type']
        task_sum = entry['total_tasks']
        if not email in mydict:
            mydict[email] = {}
        mydict[email]['full_name'] = full_name
        mydict[email]['email'] = email
        if not 'tasks' in mydict[email]:
            mydict[email]['tasks']={}
        if not task_type in mydict[email]['tasks']:
            mydict[email]['tasks'][task_type]={}
        mydict[email]['tasks'][task_type] = task_sum
        task_types.add(task_type)
    task_types = sorted(task_types)
    for key in mydict:
        for task_type in task_types:
            if task_type not in mydict[key]['tasks'].keys():
                print(task_type)
                mydict[key]['tasks'][task_type]=0

    return mydict, task_types


@login_required
def search_task(request):
    all_users = CustomUser.objects.filter(is_active=True)
    all_task_type = TaskType.objects.all()
    # summary_report = False
    if request.method == 'POST':
        # task_add_form = TaskReportForm(request.POST)
        # for field in task_add_form:
        #     print("Field Error:", field.name,  field.errors)
        
        # if task_add_form.is_valid():
            # task_assigned_to = task_add_form.cleaned_data['assigned_to']

        task_assigned_to = request.POST.getlist('assigned_to')
        task_assigned_by = request.POST.getlist('assigned_by')
        task_status = request.POST.getlist('task_status')
        task_due = request.POST.getlist('task_due')
        # print(task_due)
        task_type = request.POST.getlist('task_type')
        summary_report = request.POST.getlist('summary_report')
        # print(summary_report)
        start_date = request.POST.get('start-date')
        end_or_due_date = request.POST.get('end-or-due-date')
        if start_date == '':
            start_date = '1970-01-01 00:00:00'
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            start_date = timezone.make_aware(start_date)
            print(start_date)
        else:
            start_date = start_date + ' 00:00:00'
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            start_date = timezone.make_aware(start_date)
            # print(start_date)

        if end_or_due_date == '':
            today = timezone.now()
            end_or_due_date = today + timedelta(days=365)
            print(end_or_due_date)
        else:
            end_or_due_date = end_or_due_date + ' 23:59:59'
            end_or_due_date = datetime.strptime(end_or_due_date, "%Y-%m-%d %H:%M:%S")
            end_or_due_date = timezone.make_aware(end_or_due_date)
            # print(end_or_due_date)        


        if not task_assigned_to or 'all' in task_assigned_to:
            task_assigned_to = CustomUser.objects.filter(is_active=True)
        if not task_assigned_by or 'all' in task_assigned_by:
            task_assigned_by = CustomUser.objects.filter(is_active=True)
        if not task_status or 'all' in task_status:
            task_status = ['1','2','3','4']
        if not task_type or 'all' in task_type:
            task_type = TaskType.objects.all()

        task_query = TaskManager.objects.filter(
            delete_status=0, 
            assigned_to__in = task_assigned_to, 
            assigned_by__in = task_assigned_by, 
            task_status__in = task_status,
            task_type__in = task_type,
            created_at__gt = start_date,
            ).order_by('task_status','due_date')
            # ).order_by('task_status','due_date').distinct()
        # print(task_query.count())

        
        # task_query = task_query.filter(
        #     Q(delete_status=False) & (
        #         (Q(task_visibility=2) & Q(created_by=request.user)) | Q(task_visibility=1)
        #     ) &
        #         ( Q(task_status__in=[1,3,4], due_date__lt = end_or_due_date) | Q(task_status__in=[2], completed_date__lt=end_or_due_date)) 
             
        #     ).order_by('task_status','due_date')

        task_query = task_query.filter(
            Q(delete_status=False) & (
                (Q(task_visibility=2) & Q(created_by=request.user)) | Q(task_visibility=1)
            ) &
                # ( Q(completed_date__lt=end_or_due_date) | Q(due_date__lt = end_or_due_date) )
                ( Q(task_status__in=[1,3,4], due_date__lt = end_or_due_date) | Q(task_status__in=[2], completed_date__lt=end_or_due_date)) 
             
            ).order_by('task_status','due_date')        
        
        print(task_query.query)
        if not task_query:
            messages.warning(request, 'No result found based on the criteria!')

        if 'show' in request.POST:
            if summary_report:
                mydict, task_types = get_summary_report(task_query)
                print(summary_report)

                context = {
                    'all_users':all_users,
                    'user_data': mydict,
                    'all_task_type': all_task_type,
                    'task_types': task_types,
                    'summary_report':summary_report,
                }
                return render(request, 'server/taskmanager/task_report.html', context)
            else:
                context = {
                    'all_users':all_users,
                    'task_query':task_query,
                    'all_task_type':all_task_type,
                    'summary_report':summary_report,
                }
                return render(request, 'server/taskmanager/task_report.html', context)
        
        elif 'download' in request.POST:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Task_Report.xls"'

            wb = xlwt.Workbook(encoding='utf-8')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            font_style = xlwt.XFStyle()
            font_style2 = xlwt.XFStyle()
            font_style2.num_format_str = 'dd/MM/yyyy'
            # dateformate = xlwt.XFStyle()
            # dateformate.num_format_str = 'DD-MMM-YYYY'
            wrap_style = xlwt.easyxf('alignment: wrap True')

            if summary_report:
                ws = wb.add_sheet('Task Summary Report')
                mydict, task_types = get_summary_report(task_query)
                columns = ['SL','User'] + task_types

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                
                for row in mydict:
                    row_num += 1
                    col_num = 1

                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, mydict[row]['full_name'], font_style)
                    # for i in columns:
                    
                    for task_type in task_types:
                        for i,j in mydict[row]['tasks'].items():
                            if task_type == i:
                                col_num += 1
                                ws.write(row_num, col_num, int(mydict[row]['tasks'][task_type]), font_style)



                


            else:
                ws = wb.add_sheet('Task Report')
                columns = ['SL', 'Task ID', 'Task Name', 'Description', 'Assigned To', 'Assigned By', 'Due Date',  'Completion Date',  'Task Status', 'Comments', 'Reference Task', 'Created By','Task Type']

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)


                # d_format = wb.add_format({'num_format': 'd-m-yyyy'})

                rows = task_query

                for row in rows:
                    row_num += 1
                    assigned_to_str=""
                    counter = 0
                    for i in row.assigned_to.all():
                        counter += 1
                        if counter < len(row.assigned_to.all()):
                            assigned_to_str += i.get_full_name()
                            assigned_to_str += "\n"
                        else:
                            assigned_to_str += i.get_full_name() 

                    comments_str = ""
                    counter2 = 0
                    for j in row.task_steps_commentary.all():
                        counter2 += 1
                        comments_str += "Name: "
                        comments_str += str(j.added_by)
                        comments_str += ","
                        comments_str += "Time: "
                        comments_str += str(j.add_time.strftime('%d/%m/%Y %I:%M%p'))
                        comments_str += ","
                        comments_str += "Comment: " 
                        comments_str += j.comment  
                        if counter2 < len(row.task_steps_commentary.all()):
                            comments_str += ";\n"   
                        

                    if row.reference_task:
                        ref_task = row.reference_task.task_title
                    else:
                        ref_task = "-"
                    if row.completed_date:
                        com_date = timezone.make_naive(row.completed_date).strftime('%d/%m/%Y %I:%M%p')
                    else:
                        com_date = "-"
                    if row.task_status == 1:
                        tsk_sts = "Incomplete"
                    elif row.task_status == 2:
                        tsk_sts = "Complete"
                    elif row.task_status == 3:
                        tsk_sts = "Pause"
                    elif row.task_status == 4:
                        tsk_sts = "Cancel"

                    if row.task_visibility == 1:
                        tsk_vis = "Public"
                    elif row.task_visibility == 2:
                        tsk_vis = "Private"
                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, "T-"+str(row.id), font_style)
                    ws.write(row_num, 2, row.task_title, font_style)
                    ws.write(row_num, 3, row.description, font_style)
                    ws.write(row_num, 4, assigned_to_str, wrap_style)
                    ws.write(row_num, 5, row.assigned_by.get_full_name(), font_style)
                    ws.write(row_num, 6, timezone.make_naive(row.due_date).strftime('%d/%m/%Y %I:%M%p'), font_style2)
                    ws.write(row_num, 7, com_date, font_style2)
                    ws.write(row_num, 8, tsk_sts, font_style)
                    ws.write(row_num, 9, comments_str, wrap_style)
                    ws.write(row_num, 10, ref_task, font_style)
                    ws.write(row_num, 11, row.created_by.get_full_name(), font_style)
                    ws.write(row_num, 12, tsk_vis, font_style)

            wb.save(response)
            return response
        # elif 'download' in request.POST:

    # # create gantt/timeline chart.
    # fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    # # shows charts in reversed, so last row of dataframe will show at bottom
    # fig.update_yaxes(autorange="reversed")
    # fig.show()
    # form = TaskReportForm()
    context = {
        # 'form':form
        'all_users':all_users,
        'all_task_type':all_task_type,

    }
    return render(request, 'server/taskmanager/task_report.html', context)

@login_required
def add_comment(request):
    if request.method == 'POST':
        if request.POST["comment"] != "":
            comment = request.POST["comment"]
            task_id = request.POST["task_id"]

            task = TaskManager.objects.get(pk=task_id)
            comment_instance = TaskStepComentary(comment=comment, added_by=request.user, add_time=timezone.now())
            comment_instance.save()

            task.task_steps_commentary.add(comment_instance)
            task.save()

            history = TaskHistory(task=task,comment_add=comment_instance,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()

            return JsonResponse({"status":"success","message": f"Comment added successfully"})

        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})
            
@login_required
def change_status(request):
    if request.method == 'POST':
        if request.POST["status_id"] != "":
            status_id = request.POST["status_id"]
            task_id = request.POST["task_id"]

            task = TaskManager.objects.get(pk=task_id)
            task.task_status = status_id
            
            if task.task_from_incidence:
                msg2 = update_incidence_status(request, task)

            if status_id == '2':
                # print(status_id)
                task.completed_date = timezone.now()
            else:
                task.completed_date = None
            task.save()

            history = TaskHistory(task=task,changed_status=status_id,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()

            if status_id == '1':
                msg = "Task has been activated successfully!"
            elif status_id == '2':
                msg = "Task has been marked as complete successfully!"
            elif status_id == '3':
                msg = "Task has been paused successfully!"
            elif status_id == '4':
                msg = "Task has been cancelled successfully!"

            if task.task_from_incidence:
                return JsonResponse({"status":"success","message": msg + msg2})
            else:
                return JsonResponse({"status":"success","message": msg})

        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def change_visibility(request):
    if request.method == 'POST':
        task_id = request.POST["task_id"]

        task = TaskManager.objects.get(pk=task_id)
        task.task_visibility = 1
        
        task.save()

        history = TaskHistory(task=task,task_visibility=1,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
        history.save()

        msg = "Task has been changed to public successfully!"

        return JsonResponse({"status":"success","message": msg})

@login_required
def change_assign_to(request):
    if request.method == 'POST':
        # user = request.POST.getlist('user[]')
        # print(user)
        if request.POST.getlist('user[]') != "":
            user = request.POST.getlist('user[]')
            task_id = request.POST["task_id"]

            users = CustomUser.objects.filter(pk__in = user)

            # print(users)

            task = TaskManager.objects.get(pk=task_id)
            task.assigned_to.set(users)
            task.save()

            user_email = ['samrat.ict@pubalibankbd.com', 'sazedur.ict@pubalibankbd.com']
            # for user in users:
            #     user_email.append(user.email)
            mail = SendMail()
            subject = 'Task Assigned to you'
            message = f"Task T-{task.id} ({task.task_title}) assigned to you.\nPlease login to portal for details."
            for email in user_email:
                mail.send(email, subject, message)

            history = TaskHistory(task=task,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()
            history.refresh_from_db()
            history.assigned_to.set(users)
            history.assigned_by = request.user
            history.save()

            return JsonResponse({"status":"success","message": f"Task assignment has been changed successfully"})

        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def change_ref_task(request):
    if request.method == 'POST':
        if request.POST["ref_task"] != "":
            ref_task = request.POST["ref_task"]
            task_id = request.POST["task_id"]

            ref_task = TaskManager.objects.get(pk=ref_task)

            task = TaskManager.objects.get(pk=task_id)
            task.reference_task = ref_task
            task.save()

            history = TaskHistory(task=ref_task,sub_task_add=task,effective_date=timezone.now(),insert_by=request.user,insert_date=timezone.now())
            history.save()

            history = TaskHistory(task=task,ref_task_add=ref_task,effective_date=timezone.now(),insert_by=request.user,insert_date=timezone.now())
            history.save()
            return JsonResponse({"status":"success","message": f"Reference task has been added successfully"})

        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def change_due_date(request):
    if request.method == 'POST':
        if request.POST["due_date"] != "":
            due_date = request.POST["due_date"]
            task_id = request.POST["task_id"]

            task = TaskManager.objects.get(pk=task_id)
            task.due_date = due_date
            task.save()

            due_date_count = TaskHistory.objects.filter(task=task, due_date__isnull = False).count()
            due_date_count+=1


            history = TaskHistory(task=task,due_date=due_date_count,effective_date=due_date,insert_by=request.user,insert_date=timezone.now())
            history.save()


            return JsonResponse({"status":"success","message": f"Due date changed successfully"})

        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})

@login_required
def change_kb(request):
    if request.method == 'POST':
        # user = request.POST.getlist('user[]')
        # print(user)
        if request.POST.getlist('kb[]') != "":
            kb = request.POST.getlist('kb[]')
            task_id = request.POST["task_id"]

            kbs = KnowledgeBase.objects.filter(pk__in = kb)

            

            # print(users)

            task = TaskManager.objects.get(pk=task_id)
            # for kb in kbs:
            #     if kb in task.task_procedure_or_kb.all():
            #         return JsonResponse({"status":"error","message": f"There is a KB already in task kb list."})

            task.task_procedure_or_kb.set(kbs)
            task.save()

            history = TaskHistory(task=task,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()
            history.refresh_from_db()
            history.task_procedure_or_kb.set(kbs)
            history.kb_insert_by = request.user
            history.save()

            return JsonResponse({"status":"success","message": f"KB has been changed successfully"})

        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})
        
@login_required    
def user_and_category_wise_report(request):
    return render(request, 'server/taskmanager/user_and_cat_wise_report.html')