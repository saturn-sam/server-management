from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.formats import localize
from licenseinfo.models import LicenseInfo



class Command(BaseCommand):
    help = 'Activate deactivate license based on date'

    def handle(self, *args, **options):
        licenses = LicenseInfo.objects.filter(delete_status=False)
        for license in licenses:
            if license.end_date and license.end_date <= timezone.now() and license.license_status == True:
                license.license_status = False
                license.save()
                print(f"{localize(timezone.localtime(timezone.now()))} - Expired - {license.license_name} - {license.license_number}")
            if license.end_date and license.end_date >= timezone.now() and license.license_status == False:
                license.license_status = True
                license.save()
                print(f"{localize(timezone.localtime(timezone.now()))} - Activate - {license.license_name} - {license.license_number}")
        # print(license)

