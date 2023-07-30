from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.db.models import Max
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from django.utils import timezone
from datetime import datetime
import datetime as dt
from django.shortcuts import get_object_or_404
# Create your views here.


def send_email():
    receiver = CustomUser.objects.filter(is_active=1)
    all_email = []
    for i in all_user:
        all_email.append(i.email)
    message = render_to_string('mail_format/meeting-close-sent-mail-template.html', {
        'meetings': meetings,
    }) 
    subject = 'Meeting ' + str(meetings.number) + 'has been closed'    
    email = EmailMessage(subject,message,settings.EMAIL_HOST_USER,all_email)
    file_to_be_sent = os.path.join(settings.BASE_DIR, filename_2)
    email.attach_file(file_to_be_sent)
    email.content_subtype = "html" 
    email.send() 

@login_required
def monitoring_dashboard(request):

    services = Log.objects.raw('SELECT * FROM (SELECT * FROM serverinfo_runningservices left join monitoring_log where monitoring_log.service_id = serverinfo_runningservices.id and serverinfo_runningservices.monitoring_enabled=1 and serverinfo_runningservices.delete_status=0 ORDER BY insertion_date DESC) AS x GROUP BY service_id')

    monitoring_enabled_count = RunningServices.objects.filter(monitoring_enabled=1, delete_status=False).count()
    service_in_monitoring_count = len(list(services))

    
    context = {
        'services':services,
        'monitoring_enabled_count':monitoring_enabled_count,
        'service_in_monitoring_count':service_in_monitoring_count
    }
    return render(request, 'server/monitoring/dashboard.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



@csrf_exempt
def collection(request):
    if request.method == 'POST':
        received_data = json.loads(request.body.decode("utf-8"))

        all_data = received_data['all_service']

        service_inserted_to_db = []

        for data in all_data:
            service_folder = data['file']

            mod_time = data['file_date']
            client_ip_address = get_client_ip(request)
            mod_time = timezone.make_aware(datetime.fromtimestamp(mod_time))

            try:
                service = RunningServices.objects.get(service_log_loc=service_folder, monitoring_enabled = 1)
            except:
                service = None

            if service and service.service_ip == client_ip_address:
                service_inserted_to_db.append(service_folder)
                Log.objects.create(service = service, mod_time = mod_time, status_from = 'auto', server_ip = client_ip_address, insertion_date = timezone.now())

        return JsonResponse({'service_inserted_to_db':service_inserted_to_db})

    else:
        return StreamingHttpResponse("You can't access this link.")