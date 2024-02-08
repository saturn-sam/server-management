from django.shortcuts import render

from django.contrib import messages
from django.http import Http404

from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import *
# from taskmanager.views import incidence_task_create

@login_required
def add_incidence(request):
    if request.method == 'POST':
        incidence_form = AddIncidenceForm(request.POST)
        if incidence_form.is_valid():
            title = incidence_form.cleaned_data.get('title')
            urgency = incidence_form.cleaned_data.get('urgency')
            impact = incidence_form.cleaned_data.get('impact')
            status = incidence_form.cleaned_data.get('status')
            reported_by = incidence_form.cleaned_data.get('reported_by')
            triggered_time = incidence_form.cleaned_data.get('triggered_time')
            responsed_at = incidence_form.cleaned_data.get('responsed_at')
            resolved_at = incidence_form.cleaned_data.get('resolved_at')
            related_kb = incidence_form.cleaned_data.get('related_kb')
            print(related_kb)

            if urgency == 3:
                due_date = triggered_time + datetime.timedelta(days=1)
            if urgency == 2:
                due_date = triggered_time + datetime.timedelta(days=3)
            if urgency == 1:
                due_date = triggered_time + datetime.timedelta(days=7)
                
            if status == 3: #resolved
                task_status = 2 #complete
                resolved_by = incidence_form.cleaned_data.get('resolved_by')
                completed_date = resolved_at
                task_manager_instance = incidence_task_create(request, title=title, reported_by=reported_by, assigned_to = resolved_by, task_procedure_or_kb = related_kb, task_visibility=1, due_date=due_date, task_status=task_status, task_from_incidence=True, created_by=reported_by,completed_date=completed_date)
            else:
                task_status = 1 #incomplete  
                assigned_to = incidence_form.cleaned_data.get('assigned_to')   
                task_manager_instance = incidence_task_create(request, title=title, reported_by=reported_by, assigned_to = assigned_to, task_procedure_or_kb = related_kb, task_visibility=1, due_date=due_date, task_status=task_status, task_from_incidence=True, created_by=reported_by)           

            if task_manager_instance:

                incidence_instance = incidence_form.save()
                incidence_instance.refresh_from_db()
                incidence_instance.added_by = request.user
                incidence_instance.related_task = task_manager_instance
                incidence_instance.save()
                messages.success(request, f'Incidence added successfully. Update related KB time to time.')
                messages.success(request, f'A task has been created regarding this incidence. Please keep track to related task from task manager.')

                incidence_form = AddIncidenceForm()

    else:
         incidence_form = AddIncidenceForm()       


    context ={
        'form':incidence_form
    }
    return render(request, 'server/incidence/add_incidence.html', context)

@login_required
def incidence_list(request):
    incidence_lists = Incidence.objects.filter(delete_status=False)
    # today = timezone.now()

    context={
        "incidence_lists": incidence_lists,
        # "today":today
    }
    return render(request, 'server/incidence/view_incidence_list.html', context) 

@login_required
def incidence_task_create(request,**kwargs):

    if kwargs["task_status"] == 2:
        task_manager_instance = TaskManager(task_title=kwargs["title"], 
                                            description=f"Task from incidence -{kwargs['title']}", 
                                            assigned_by=kwargs["reported_by"],
                                            task_visibility=kwargs["task_visibility"], 
                                            due_date=kwargs["due_date"], 
                                            task_status=kwargs["task_status"], 
                                            task_from_incidence=True, 
                                            completed_date=kwargs["completed_date"], 
                                            created_by=kwargs["reported_by"])
    elif kwargs["task_status"] == 1:
        task_manager_instance = TaskManager(task_title=kwargs["title"], 
                                            description=f"Task from incidence -{kwargs['title']}", 
                                            assigned_by=kwargs["reported_by"],
                                            task_visibility=kwargs["task_visibility"], 
                                            due_date=kwargs["due_date"], 
                                            task_status=kwargs["task_status"], 
                                            task_from_incidence=True, 
                                            created_by=kwargs["reported_by"])       
    task_manager_instance.save()
    task_manager_instance.refresh_from_db()
    task_manager_instance.assigned_to.set(kwargs["assigned_to"])
    # for kb in kwargs["task_procedure_or_kb"]:
    # task_manager_instance.task_procedure_or_kb.set(kb)
    task_manager_instance.task_procedure_or_kb.set(kwargs["task_procedure_or_kb"])
    task_manager_instance.save()

    history = TaskHistory(task=task_manager_instance,new_task_add=1,effective_date=timezone.now(),insert_date=timezone.now(),insert_by=request.user)
    history.save()

    history = TaskHistory(task=task_manager_instance,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
    history.save()
    history.refresh_from_db()
    history.assigned_to.set(kwargs["assigned_to"])
    history.assigned_by = kwargs["reported_by"]
    history.save()

    if kwargs["task_status"] == 2:
        history = TaskHistory(task=task_manager_instance, changed_status=kwargs["task_status"],insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
        history.save()

    history = TaskHistory(task=task_manager_instance,due_date=1,effective_date=kwargs["due_date"],insert_date=timezone.now(),insert_by=request.user)
    history.save()



    return task_manager_instance



@login_required
def view_incidence(request, pk):
    try:
        incidence_details = Incidence.objects.get(pk=pk,delete_status=False)
    except:
        raise Http404("Selected task not found.")


    # sub_tasks = TaskManager.objects.filter(reference_task=task_details)
    task_histories = TaskHistory.objects.filter(task=incidence_details.related_task).order_by('-effective_date')
    # all_users = CustomUser.objects.filter(is_active=1)
    # all_tasks = TaskManager.objects.filter(delete_status=False)
    context={
        "incidence_details": incidence_details,
        # "sub_tasks" : sub_tasks,
        "task_histories" : task_histories,
        # "all_users" : all_users,
        # "all_tasks" : all_tasks,
        # "kb_lists" : kb_lists
    }
    return render(request, 'server/incidence/view_single_incidence.html', context)

@login_required
def update_incidence_status(request, task):
    try:
        incidence_instance = Incidence.objects.get(related_task=task)
        incidence_instance.status = 3
        incidence_instance.updated_by = request.user
        if incidence_instance.assigned_to.all():
            for assigned in incidence_instance.assigned_to.all():
                incidence_instance.resolved_by.add(assigned)
        else:
            incidence_instance.resolved_by.add(incidence_instance.reported_by)
        incidence_instance.updated_by = request.user
        incidence_instance.resolved_at = timezone.now()
        incidence_instance.save()
        # messages.success(request, f'Incidence status has been updated.')
        return "\nIncidence status has been updated."
    except Exception as e:
        print(e)
        return "\nIncidence related to this task not found."


    

