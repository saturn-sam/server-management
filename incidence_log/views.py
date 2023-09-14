from django.shortcuts import render

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import *

@login_required
def add_incidence(request):
    form = AddIncidenceForm()
    context ={
        'form':form
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