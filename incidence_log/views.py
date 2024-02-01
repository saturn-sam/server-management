from django.shortcuts import render

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import *

@login_required
def add_incidence(request):
    print('ok')
    if request.method == 'POST':
        incidence_form = AddIncidenceForm(request.POST)
        if incidence_form.is_valid():
            title = incidence_form.cleaned_data.get('title')
            urgency = incidence_form.cleaned_data.get('urgency')
            impact = incidence_form.cleaned_data.get('impact')
            status = incidence_form.cleaned_data.get('status')
            reported_by = incidence_form.cleaned_data.get('reported_by')
            triggered_time = incidence_form.cleaned_data.get('triggered_time')
            assigned_to = incidence_form.cleaned_data.get('assigned_to')
            responsed_at = incidence_form.cleaned_data.get('responsed_at')
            resolved_by = incidence_form.cleaned_data.get('resolved_by')
            resolved_at = incidence_form.cleaned_data.get('resolved_at')
            if status == 3: #resolved
                task_status = 2 #complete
                completed_date = resolved_at
            else:
                task_status = 1 #incomplete
                completed_date = resolved_at                
            # print(urgency, triggered_time)
            if urgency == 3:
                due_date = triggered_time + datetime.timedelta(days=1)
            if urgency == 2:
                due_date = triggered_time + datetime.timedelta(days=3)
            if urgency == 1:
                due_date = triggered_time + datetime.timedelta(days=7)
            task_manager_instance = TaskManager(task_title=title, description=f"Task from inceide -{title}", assigned_by=reported_by,task_visibility=1, due_date=due_date, task_from_incidence=True, created_by=reported_by)
            task_manager_instance.save()
            task_manager_instance.refresh_from_db()
            task_manager_instance.assigned_to.set(assigned_to)
            task_manager_instance.save()

            history = TaskHistory(task=task_manager_instance,insert_by=request.user,effective_date=timezone.now(),insert_date=timezone.now())
            history.save()
            history.refresh_from_db()
            history.assigned_to.add(request.user)
            history.assigned_by = request.user
            history.save()

            history = TaskHistory(task=task_manager_instance,due_date=1,effective_date=due_date,insert_date=timezone.now(),insert_by=request.user)
            history.save()

            incidence_instance = incidence_form.save()
            incidence_instance.refresh_from_db()
            incidence_instance.added_by = request.user
            incidence_instance.related_task = task_manager_instance
            incidence_instance.save()
            messages.success(request, f'Incidence added successfully. Update related KB time to time. Keep track to related task manager.')

            incidence_form = AddIncidenceForm()
    else:
         incidence_form = AddIncidenceForm()       


    context ={
        'form':incidence_form
    }
    return render(request, 'server/incidence/add_incidence.html', context)

# class AddIncidentView(LoginRequiredMixin, SuccessMessageMixin,CreateView):
#     form_class = AddIncidenceForm
#     template_name = "server/incidence/add_incidence.html"
#     success_message = "Incident added successfully!"
#     #success_url = reverse_lazy("core:index")

#     def form_valid(self, form):
#         if self.request.user.is_authenticated:
#             form.instance.reported_by = self.request.user.profile
#             form.instance.save()
#         return super().form_valid(form)