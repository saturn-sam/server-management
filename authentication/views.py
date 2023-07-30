from serverinfo.models import PhysicalServer, RunningServices, VirtualServer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Count, Q, Sum, FilteredRelation
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site

from django.utils import timezone
from datetime import timedelta

from .forms import UserUpdateForm, ProfileUpdateForm, UserAdminCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView

from knowledgebase.models import KnowledgeBase, KBTopic
from authentication.models import CustomUser, Profile
from licenseinfo.models import LicenseInfo

# from accounting.models import Deposite, Earning, Expenditure, Subscriptionof

# Create your views here.


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'server/login.html'
    success_message = 'Successfully Logged In.'

def signup_view(request):
    if request.method  == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            messages.error(request, 'Account has been created! Please wait until your account become verified by an admin. You will receive an email on approval.')
            return redirect('registration')
    else:
        form = UserAdminCreationForm()
    return render(request, 'server/registration.html', {'form': form})

@login_required
def home_page(request):
    total_user = CustomUser.objects.filter(is_active=1).count()
    total_physical_server = PhysicalServer.objects.filter(delete_status=False).count()
    total_vm = VirtualServer.objects.filter(delete_status=False).count()
    total_service = RunningServices.objects.filter(Q(delete_status=False) and ~Q(service_type__service_type_name='Machine Identification Service')).count()
    total_kb = KnowledgeBase.objects.filter(delete_status=False).count()
    total_kb_topic = KBTopic.objects.filter(delete_status=False).count()
    active_license = LicenseInfo.objects.filter(delete_status=False, license_status=True).count()
    expire_soon = LicenseInfo.objects.filter(delete_status=False, license_status=True, end_date__lte = timezone.now() + timedelta(days=90), end_date__gte = timezone.now()).count()
    expired = LicenseInfo.objects.filter(delete_status=False, license_status=False).count()
    context ={
        'total_user':total_user,
        'total_physical_server':total_physical_server,
        'total_vm':total_vm,
        'total_service':total_service,
        'total_kb':total_kb,
        'total_kb_topic':total_kb_topic,
        'active_license':active_license,
        'expire_soon':expire_soon,
        'expired':expired
    }
    return render(request, 'server/index.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('login')

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['image', 'designation','bio']
    template_name = 'server/profile_edit.html'

    def get_success_url(self):
        messages.success(self.request, 'Profile Saved Successfully.')
        return reverse('home')

# @login_required
# def dashboard(request):
#     total_user = CustomUser.objects.filter(is_active=1).count()
#     total_deposit_all = Deposite.objects.filter(Q(approve_status=1)).aggregate(Sum('amount'))
#     if not total_deposit_all['amount__sum']:
#         total_deposit_all['amount__sum']=0

#     total_earning_all = Earning.objects.filter(Q(approve_status=1)).aggregate(Sum('amount'))
#     total_earning_other = Earning.objects.filter(~Q(earning_source = 1) & Q(approve_status = 1)).aggregate(Sum('amount'))
#     if not total_earning_other['amount__sum']:
#         total_earning_other['amount__sum']=0

#     total_expenditure = Expenditure.objects.filter(Q(approve_status = 1)).aggregate(Sum('amount'))
#     total_expenditure_other_than_savings = Expenditure.objects.filter(Q(approve_status = 1) & ~Q(expenditure_type = 2)).aggregate(Sum('amount'))
#     if not total_expenditure_other_than_savings['amount__sum']:
#         total_expenditure_other_than_savings['amount__sum']=0

#     total_savings = Expenditure.objects.filter(Q(approve_status = 1) & Q(expenditure_type = 1)).aggregate(Sum('amount'))
#     if not total_savings['amount__sum']:
#         total_savings['amount__sum']=0

#     if not total_expenditure['amount__sum']:
#         total_expenditure['amount__sum']=0
#     liquid_cash_on_hand = 0
#     if not total_earning_all['amount__sum']:   
#         total_earning_all['amount__sum']=0 
#     liquid_cash_on_hand = total_earning_all['amount__sum'] - total_expenditure['amount__sum']



#     ###########For all Members Due Count##########

#     all_users = CustomUser.objects.all()
#     month_wise_deposit_all = Subscriptionof.objects.annotate(deposite_user=FilteredRelation('deposite', condition=Q(deposite__approve_status=1))).values('subs_of', 'deposite_user__member_name__first_name', 'deposite_user__member_name__id').order_by('-id')

#     all_subs_of = Subscriptionof.objects.all()

    
#     new_dict = {}
#     for i in all_users:
#         new_list = []
#         user_due  = []

#         for j in all_subs_of:
            
#             for k in month_wise_deposit_all:
#                 if i.id == k['deposite_user__member_name__id'] :
#                     new_list.append(k["subs_of"])
#             counter = 0
#             for m in new_list:
#                 if m == str(j.subs_of):
#                     counter += 1
#             if counter == 0:
#                 user_due.append(j.subs_of)
#         user_full_name = i.first_name+" "+i.last_name
#         new_dict[user_full_name] = user_due
#     # print(new_dict)   
#     ###########For all Members Due Count########## 


#     member_deposit_labels = []
#     member_deposit_data = []
#     queryset = Deposite.objects.values('member_name__first_name','member_name__last_name').annotate(total_deposit=Sum('amount')).filter(approve_status = 1).order_by('-total_deposit')
#     for member in queryset:
#         member_name = member['member_name__first_name'] + " " + member['member_name__last_name']
#         member_deposit_labels.append(member_name)
#         member_deposit_data.append(member['total_deposit']) 

#     context={
#         'user_count' : total_user,
#         'total_deposit_all' : total_deposit_all,
#         'total_earning_other' : total_earning_other,
#         'total_expenditure' : total_expenditure,
#         'total_expenditure_other_than_savings' : total_expenditure_other_than_savings,
#         'total_savings' : total_savings,
#         'total_earning_all' : total_earning_all,
#         'liquid_cash_on_hand' : liquid_cash_on_hand,
#         'member_deposit_labels' : member_deposit_labels,
#         'member_deposit_data' : member_deposit_data,
#         'new_dict' : new_dict
#         #'post_count' : total_post,
#         #'post_published' : total_published,
#         #'post_draft' : total_post - total_published
#     }
#     return render(request, 'dashboard/uttaran/index.html',context)


# @login_required
# def profileedit(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)  

#     context = {
#         'u_form' : u_form,
#         'p_form' : p_form
#     }
#     return render(request, 'dashboard/uttaran/profile-edit.html', context)



