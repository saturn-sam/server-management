from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .aesutil import *

from .forms import *
from .models import *
from .utils import *

# Create your views here.
@login_required
def add_master_pass(request):
    errors=""
    if request.method == 'POST':
        master_key_add_form = MasterKeyAddForm(request.POST)
        if master_key_add_form.is_valid():
            master_key_name = master_key_add_form.cleaned_data.get('master_key_name')
            master_key = master_key_add_form.cleaned_data.get('master_key')
            
            hashed_mp = hashlib.sha256(master_key.encode()).hexdigest()

            ds = generateDeviceSecret()
            master_passwd = Secret(user_id=request.user, master_key_name=master_key_name, masterkey_hash=hashed_mp, device_secret=ds)
            master_passwd.save() 
            messages.success(request, f'Master Key Saved Successfully.')
            return redirect('my_master_pass')
            
    else:
        master_key_add_form = MasterKeyAddForm()
    context = {
        'master_key_add_form':master_key_add_form,
        'errors':errors
    }
    return render(request, 'server/pass_manager/add_master_key.html',context) 

@login_required
def my_master_pass(request):
    mp_ins = Secret.objects.filter(user_id=request.user)
    context={
        'mp_ins':mp_ins
    }
    return render(request, 'server/pass_manager/mp_list.html',context)

@login_required
def change_master_pass(request):
    errors=""
    if request.method == 'POST':
        master_key_change_form = MasterKeyChangeForm(request.POST, user=request.user)
        if master_key_change_form.is_valid():
            current_master_key = master_key_change_form.cleaned_data.get('current_master_key')
            new_master_key = master_key_change_form.cleaned_data.get('master_key')
            master_key_id = master_key_change_form.cleaned_data.get('master_key_name')

            current_master_key_hash =  hashlib.sha256(current_master_key.encode()).hexdigest()
            # saved_mp = Secret.objects.get(user_id=request.user, pk=pass_entry_ins.master_key.id)
            master_key_instances = Secret.objects.get(user_id=request.user, pk=master_key_id, masterkey_hash=current_master_key_hash)
            
            all_password_entries = Passwd.objects.filter(user_id=request.user, master_key=master_key_instances)
            device_secrete = master_key_instances.device_secret

            current_mk = computeMasterKey(current_master_key,device_secrete)



            new_mk = computeMasterKey(new_master_key,master_key_instances.device_secret)

            for password_entry in all_password_entries:
                decrypted_username = decrypt(key=current_mk,source=password_entry.username,keyType="bytes")
                decrypted_password = decrypt(key=current_mk,source=password_entry.password,keyType="bytes")
                decrypted_username = decrypted_username.decode()
                decrypted_password = decrypted_password.decode()

                
                encrypted_password = encrypt(key=new_mk, source=decrypted_password, keyType="bytes")
                encrypted_user = encrypt(key=new_mk, source=decrypted_username, keyType="bytes")
                
                password_entry.username = encrypted_user
                password_entry.password = encrypted_password
                password_entry.save() 

            new_hashed_mp = hashlib.sha256(new_master_key.encode()).hexdigest()
            master_key_instances.masterkey_hash = new_hashed_mp
            master_key_instances.save()         
            messages.success(request, f'Master Key and related Password has been changed Successfully!')
            return redirect('my_master_pass')

    else:
        master_key_change_form = MasterKeyChangeForm(user=request.user)
    context = {
        'master_key_change_form':master_key_change_form,
    }
    return render(request, 'server/pass_manager/change_master_key.html',context) 

@login_required
def add_entry(request):
    if request.method == 'POST':
        add_entry_form = AddEntryForm(request.POST,user=request.user)
        if add_entry_form.is_valid():
            master_key = add_entry_form.cleaned_data.get('master_key')
            master_key_id = add_entry_form.cleaned_data.get('master_key_name')
            site_server_name = add_entry_form.cleaned_data.get('site_server_name')
            ip_or_url = add_entry_form.cleaned_data.get('ip_or_url')
            username = add_entry_form.cleaned_data.get('username')
            password = add_entry_form.cleaned_data.get('password')
            remark = add_entry_form.cleaned_data.get('remark')

            hashed_mp = hashlib.sha256(master_key.encode()).hexdigest()
            mp_ins = Secret.objects.get(masterkey_hash=hashed_mp, pk=master_key_id,user_id=request.user)
            mk = computeMasterKey(master_key,mp_ins.device_secret)

            encrypted = encrypt(key=mk, source=password, keyType="bytes")
            encrypted_user = encrypt(key=mk, source=username, keyType="bytes")

            passwd = Passwd(user_id=request.user, master_key=mp_ins, site_server_name=site_server_name, ip_or_url=ip_or_url, username=encrypted_user, password=encrypted, remark=remark)
            passwd.save() 
            messages.success(request, f'Password of {site_server_name} has been Encripted and Stored Successfully!')

            return redirect('add_entry')
    else:
        add_entry_form = AddEntryForm(user=request.user)

    context = {
        'add_entry_form':add_entry_form,
    }
    return render(request, 'server/pass_manager/add_entry.html',context) 

@login_required
def pass_list(request):
    pass_ins = Passwd.objects.filter(user_id=request.user)

    context={
        'pass_ins':pass_ins
    }
    return render(request, 'server/pass_manager/pass_list.html',context)

@login_required
def view_pass(request):
    if request.method == 'POST':
        if request.POST["view-pass-name"] != "":
            master_key = request.POST["view-pass-name"]
            pass_entry = request.POST["entry-id"]
            pass_entry_ins = get_object_or_404(Passwd, pk=pass_entry)
            if pass_entry_ins:
                given_mp_hash =  hashlib.sha256(master_key.encode()).hexdigest()
                saved_mp = Secret.objects.get(user_id=request.user, pk=pass_entry_ins.master_key.id)

                device_secrete = saved_mp.device_secret

                if given_mp_hash == saved_mp.masterkey_hash:
                    mk = computeMasterKey(master_key,device_secrete)
                    decrypted_username = decrypt(key=mk,source=pass_entry_ins.username,keyType="bytes")
                    decrypted_password = decrypt(key=mk,source=pass_entry_ins.password,keyType="bytes")
                    decrypted_username = decrypted_username.decode()
                    decrypted_password = decrypted_password.decode()
                    return JsonResponse({"status":"success","message": f"Password Decrypted syccessfully!","username":f"{decrypted_username}","password":f"{decrypted_password}","password_id":f"{pass_entry}"})


                else:
                    return JsonResponse({"status":"error","message": f"Given Master Key didn't matched. Please Provide {saved_mp.master_key_name}"})  
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})  

@login_required
def edit_entry(request, pk):
    pass_ins = get_object_or_404(Passwd, pk=pk, user_id=request.user)
    if request.method == 'POST':
        pass_edit_form = EditEntryForm(request.POST, user=request.user, pass_inst=pass_ins)

        if pass_edit_form.is_valid():
            master_key = pass_edit_form.cleaned_data.get('new_master_key')
            master_key_id = pass_edit_form.cleaned_data.get('new_master_key_name')
            site_server_name = pass_edit_form.cleaned_data.get('site_server_name')
            ip_or_url = pass_edit_form.cleaned_data.get('ip_or_url')
            username = pass_edit_form.cleaned_data.get('username')
            password = pass_edit_form.cleaned_data.get('password')
            remark = pass_edit_form.cleaned_data.get('remark')

            if master_key == "":
                old_master_key = pass_edit_form.cleaned_data.get('old_master_key')
                old_master_key_name = pass_edit_form.cleaned_data.get('old_master_key_name')
                old_master_key_ins = Secret.objects.get(user_id=request.user, master_key_name=old_master_key_name)
                master_key_id = old_master_key_ins.id
                master_key = old_master_key

            hashed_mp = hashlib.sha256(master_key.encode()).hexdigest()
            print(hashed_mp)
            print(master_key_id)
            print(request.user)
            mp_ins = Secret.objects.get(masterkey_hash=hashed_mp, pk=master_key_id, user_id=request.user)
            
            # print(mp_ins.device_secret)
            mk = computeMasterKey(master_key,mp_ins.device_secret)
            # print(mk)
            encrypted_pass = encrypt(key=mk, source=password, keyType="bytes")
            encrypted_user = encrypt(key=mk, source=username, keyType="bytes")

            pass_ins.master_key = mp_ins
            pass_ins.site_server_name = site_server_name
            pass_ins.ip_or_url = ip_or_url
            pass_ins.username = encrypted_user
            pass_ins.password = encrypted_pass
            pass_ins.remark = remark

            pass_ins.save()
            messages.success(request, f'Entry of {site_server_name} has been Edited Successfully!')
            return redirect('pass_list')


    else:
        pass_edit_form = EditEntryForm(user=request.user,pass_inst=pass_ins,initial={'old_master_key_name':pass_ins.master_key.master_key_name , 'new_master_key_name':pass_ins.master_key.pk, 'site_server_name':pass_ins.site_server_name,'ip_or_url':pass_ins.ip_or_url,'remark':pass_ins.remark})

    context = {
        'pass_edit_form' : pass_edit_form,
        'pass_ins':pass_ins
    }

    return render(request, 'server/pass_manager/edit_entry.html',context) 

@login_required
def delete_entry(request):
    if request.method == 'POST':
        if request.POST["delete-pass-name"] != "":
            master_key = request.POST["delete-pass-name"]
            pass_entry = request.POST["delete-entry-id"]
            pass_entry_ins = get_object_or_404(Passwd, pk=pass_entry, user_id=request.user)
            if pass_entry_ins:
                given_mp_hash =  hashlib.sha256(master_key.encode()).hexdigest()
                saved_mp = Secret.objects.get(user_id=request.user, pk=pass_entry_ins.master_key.id)
                if given_mp_hash == saved_mp.masterkey_hash:
                    pass_entry_ins.delete()
                    return JsonResponse({"status":"success","message": f"Entry Deleted Successfully"})
                else:
                    return JsonResponse({"status":"error","message": f"Given Master Key didn't matched. Please Provide {saved_mp.master_key_name}"})  
        else:
            return JsonResponse({"status":"error","message": f"Please fill the required fields."})  
