from django.shortcuts import render

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import *

@login_required
def add_incidence(request):
    if request.method == 'POST':
        incidence_form = AddIncidenceForm(request.POST)
        if incidence_form.is_valid():
            if incidence_form.cleaned_data.get('status') == 3:
                resolution_form = AddResolutionForm(request.POST)
                if resolution_form.is_valid():
                    incidence_instance = incidence_form.save()
                    incidence_instance.refresh_from_db()
                    incidence_instance.added_by = request.user
                    incidence_instance.save()

                    resolution = resolution_form.cleaned_data['resolution']
                    related_kb = resolution_form.cleaned_data['related_kb']
                    resolved_by = resolution_form.cleaned_data['resolved_by']
                    resolved_at = resolution_form.cleaned_data['resolved_at']

                    resolution_ins = Resolution(incidence = incidence_instance, resolution=resolution, related_kb=related_kb, resolved_by=resolved_by, resolved_at=resolved_at, added_by =request.user)
                    resolution_ins.save()
            
            else:
                pass
                
     


        # incidence_form = AddIncidenceForm(request.POST)


    incidence_form = AddIncidenceForm()
    resolution_form = AddResolutionForm()
    context ={
        'form':incidence_form,
        'resolution_form':resolution_form
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