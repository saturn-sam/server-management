$('.add-vm-location').click(function (event) {
    event.preventDefault()
    // var postId = $(this).data("catid")
    var vm_loc = $('.vm-location').val()

    $.ajax({
    type: "POST",
    url: `/server/add_vm_loc`,

    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        vm_loc: vm_loc
    },
    success: function(data1) {
        
        if (data1.status == "error"){
            toastr.error(data1.message);
        }
        else if (data1.status == "success"){
            $('.modal-add-vm-location').modal('hide')
            $('.vm-location').val('')
            var appendData1 = "<option value=''>---------</option>";
            for (var i = 0; i < data1.all_vm_loc.length; i++) {
                if (i==data1.all_vm_loc.length-1){
                    appendData1 += "<option value ='" + data1.all_vm_loc[i].id + "' selected>" + data1.all_vm_loc[i].container + "</option>";
                }
                else{
                    appendData1 += "<option value ='" + data1.all_vm_loc[i].id + "'>" + data1.all_vm_loc[i].container + "</option>";
                }
                
            }
            $('#id_vm_location_type').html(appendData1)
            toastr.success(data1.message);
        }
    }
    })
})


$('.add-service-type').click(function (event) {
    event.preventDefault()
    var service_type = $('.service-type').val()
    $.ajax({
    type: "POST",
    url: `/server/add_service_type`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        service_type: service_type
    },
    success: function(data1) {
        
        if (data1.status == "error"){
            toastr.error(data1.message);
        }
        else if (data1.status == "success"){
            $('.modal-add-service-type').modal('hide')
            $('.service-type').val('')
            var appendData1 = "<option value=''>---------</option>";
            for (var i = 0; i < data1.all_service_type.length; i++) {
                if (i==data1.all_service_type.length-1){
                    appendData1 += "<option value ='" + data1.all_service_type[i].id + "' selected>" + data1.all_service_type[i].service_type_name + "</option>";
                }
                else{
                    appendData1 += "<option value ='" + data1.all_service_type[i].id + "'>" + data1.all_service_type[i].service_type_name + "</option>";
                }
                
            }
            $('#id_service_type').html(appendData1)
            toastr.success(data1.message);
        }
    }
    })
})

$('.add-os').click(function (event) {
    event.preventDefault()
    // var postId = $(this).data("catid")
    var os_name = $('.os-name').val()

    $.ajax({
    type: "POST",
    url: `/server/add_os`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        os_name: os_name
    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('.modal-add-os').modal('hide')
            $('.os-name').val('')
            // select = document.getElementById('#os_type_dd');
            var appendData = "<option value=''>---------</option>";
            for (var i = 0; i < data.all_os.length; i++) {
                if (i==data.all_os.length-1){
                    appendData += "<option value ='" + data.all_os[i].id + "' selected>" + data.all_os[i].os_type + "</option>";
                }
                else{
                    appendData += "<option value ='" + data.all_os[i].id + "'>" + data.all_os[i].os_type + "</option>";
                }
                
            }
            $('#id_os_type').html(appendData)
            toastr.success(data.message);
        }
    }
    })
})

$('.add-os-version').click(function (event) {
    event.preventDefault()
    // var postId = $(this).data("catid")
    var os_version = $('.os-version-name').val()
    // alert(os_version)
    $.ajax({
    type: "POST",
    url: `/server/add_os_version`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        os_version: os_version
    },
    success: function(data1) {
        
        if (data1.status == "error"){
            toastr.error(data1.message);
        }
        else if (data1.status == "success"){
            $('.modal-add-os-version').modal('hide')
            $('.os-version-name').val('')
            // select = document.getElementById('#os_type_dd');
            var appendData1 = "<option value=''>---------</option>";
            for (var i = 0; i < data1.all_os_version.length; i++) {
                if (i==data1.all_os_version.length-1){
                    appendData1 += "<option value ='" + data1.all_os_version[i].id + "' selected>" + data1.all_os_version[i].os_version + "</option>";
                }
                else{
                    appendData1 += "<option value ='" + data1.all_os_version[i].id + "'>" + data1.all_os_version[i].os_version + "</option>";
                }
                
            }
            $('#id_os_version').html(appendData1)
            toastr.success(data1.message);
        }
    }
    })
})

$('.add-zone').click(function (event) {
    event.preventDefault()
    // var postId = $(this).data("catid")
    var zone = $('.zone').val()
    // alert(os_version)
    $.ajax({
    type: "POST",
    url: `/server/add_zone`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        zone: zone
    },
    success: function(data1) {
        
        if (data1.status == "error"){
            toastr.error(data1.message);
        }
        else if (data1.status == "success"){
            $('.modal-add-zone').modal('hide')
            $('.zone').val('')
            // select = document.getElementById('#os_type_dd');
            var appendData1 = "<option value=''>---------</option>";
            for (var i = 0; i < data1.all_zone.length; i++) {
                if (i==data1.all_zone.length-1){
                    appendData1 += "<option value ='" + data1.all_zone[i].id + "' selected>" + data1.all_zone[i].zone + "</option>";
                }
                else{
                    appendData1 += "<option value ='" + data1.all_zone[i].id + "'>" + data1.all_zone[i].zone + "</option>";
                }
                
            }
            $('#id_zone').html(appendData1)
            toastr.success(data1.message);
        }
    }
    })
})

$('.add-project').click(function (event) {
    event.preventDefault()
    // var postId = $(this).data("catid")
    var project = $('.project').val()
    // alert(os_version)
    $.ajax({
    type: "POST",
    url: `/server/add_project`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        project: project
    },
    success: function(data1) {
        
        if (data1.status == "error"){
            toastr.error(data1.message);
        }
        else if (data1.status == "success"){
            $('.modal-add-project').modal('hide')
            $('.project').val('')
            // select = document.getElementById('#os_type_dd');
            var appendData1 = "<option value=''>---------</option>";
            for (var i = 0; i < data1.all_project.length; i++) {
                if (i==data1.all_project.length-1){
                    appendData1 += "<option value ='" + data1.all_project[i].id + "' selected>" + data1.all_project[i].project + "</option>";
                }
                else{
                    appendData1 += "<option value ='" + data1.all_project[i].id + "'>" + data1.all_project[i].project + "</option>";
                }
                
            }
            $('#id_project').html(appendData1)
            toastr.success(data1.message);
        }
    }
    })
})

$('.add-service').click(function (event) {
    event.preventDefault()


    var service_name = $('#service-modal').serialize()

    $.ajax({
    type: "POST",
    url: `/server/add_service2`,
    data: service_name

    ,
    success: function(data1) {
        
        if (data1.status == "error"){
            toastr.error(data1.message);
        }
        else if (data1.status == "success"){
            $('.modal-add-service').modal('hide')
            $('#id_service_type').val('')
            $('#id_service_ip').val('')
            $('#id_service_file_loc').val('')
            $('#id_service_owner').val('')
            $('#id_comment').val('')
            for (var i = 0; i < data1.all_service_list.length; i++) {
                $('#id_service_name').append($('<option>', {value:data1.all_service_list[i].id, text:data1.all_service_list[i].service_name}));
            }

            toastr.success(data1.message);
        }
    }
    })
})

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-share-user').forEach(function(button) {
        button.onclick = function(e) {
            e.preventDefault()
            var kb_id = button.dataset.kbid;
            form_id = "#share-user-form-"+kb_id
            var user_name = $(form_id).serialize()
            $.ajax({
                type: "POST",
                url: `/kb/share-kb`,
                data: user_name,
                success: function(data1) {
                    
                    if (data1.status == "error"){
                        toastr.error(data1.message);
                    }
                    else if (data1.status == "success"){
                        $('.modal-share-with').modal('hide')
                        $('#select_share_user').val('')
                        toastr.success(data1.message);
                    }
                }
                })
        }
    });
 });

 document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.unshare-user').forEach(function(button) {
        button.onclick = function(e) {
            e.preventDefault()
            var kb_id = button.dataset.kbid;
            // var form_id = "#unshare-user-form-"+kb_id
            // var form = $(form_id).serialize()
            // var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
            var checkbox_class = "checkbox-"+kb_id
            var checkboxes = $('.'+checkbox_class+':checked')
            var unshare_user = new Array();
            var len = checkboxes.length;
            for (var i=0; i<len; i++) {
                unshare_user.push(checkboxes[i].value)
                // console.log(checkboxes[i].value)
            }
            console.log(unshare_user)
            $.ajax({
                type: "POST",
                url: `/kb/unshare-kb`,
                data: {
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    'unshare_user[]': unshare_user,
                    kb_id:kb_id
                },
                success: function(data1) {
                    
                    if (data1.status == "error"){
                        toastr.error(data1.message);
                    }
                    else if (data1.status == "success"){
                        $('.modal-share-with').modal('hide')
                        $('#select_share_user').val('')
                        toastr.success(data1.message);
                    }
                }
                })
        }
    });
 });


//Comment add in single task view
$('.add-comment').click(function (event) {
    event.preventDefault()
    var comment = $('#comment').val()
    var task_id = $('#task_id').val()

    $.ajax({
    type: "POST",
    url: `/taskmanager/add-comment`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        comment: comment,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#add-comment').modal('hide')
            $('.comment').val('')
            toastr.success(data.message);
        }
    }
    })
})

//Change status in single task view
$('.status-change-btn').click(function (event) {
    event.preventDefault()
    var status_id = $('#status_id').val()
    var task_id = $('#task_id').val()


    $.ajax({
    type: "POST",
    url: `/taskmanager/change-status`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        status_id: status_id,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#status-change').modal('hide')
            $('.status_id').val('')
            toastr.success(data.message);
        }
    }
    })
})


//Change visibility in single task view
$('.visibility-change-btn').click(function (event) {
    event.preventDefault()
    var task_id = $('#task_id').val()


    $.ajax({
    type: "POST",
    url: `/taskmanager/change-visibility`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#visibility-change').modal('hide')
            toastr.success(data.message);
        }
    }
    })
})

//Change assignment in single task view
$('.assignment-change-btn').click(function (event) {
    event.preventDefault()
    var user = $('#assigned_to').val()
    var task_id = $('#task_id').val()
    console.log(user)
    $.ajax({
    type: "POST",
    url: `/taskmanager/change-assign-to`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        user: user,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#assignment-change').modal('hide')
            $('.assigned_to').val('')
            toastr.success(data.message);
        }
    }
    })
})

//Change reference task in single task view
$('.add-ref-task-btn').click(function (event) {
    event.preventDefault()
    var ref_task = $('#ref_task').val()
    var task_id = $('#task_id').val()

    $.ajax({
    type: "POST",
    url: `/taskmanager/change-ref-task`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        ref_task: ref_task,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#add-ref-task').modal('hide')
            $('.ref_task').val('')
            toastr.success(data.message);
        }
    }
    })
})

//change due date in single task view
$('.change-due-date-btn').click(function (event) {
    event.preventDefault()
    var due_date = $('#due_date').val()
    var task_id = $('#task_id').val()

    $.ajax({
    type: "POST",
    url: `/taskmanager/change-due-date`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        due_date: due_date,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#change-due-date').modal('hide')
            $('#due_date').val('')
            toastr.success(data.message);
        }
    }
    })
})

//Change kb in single task view
$('.change-kb-btn').click(function (event) {
    event.preventDefault()
    var kb = $('#kb').val()
    var task_id = $('#task_id').val()
    console.log(kb)
    $.ajax({
    type: "POST",
    url: `/taskmanager/change-kb`,
    data: {
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        kb: kb,
        task_id: task_id

    },
    success: function(data) {
        
        if (data.status == "error"){
            toastr.error(data.message);
        }
        else if (data.status == "success"){
            $('#change-kb').modal('hide')
            $('.kb').val('')
            toastr.success(data.message);
        }
    }
    })
})


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.view-pass-btn').forEach(function(button) {
        button.onclick = function(e) {
            e.preventDefault()
            var entry_id = button.dataset.passid;
            form_id = "#view-pass-form-"+entry_id
            var master_pass = $(form_id).serialize()
            $.ajax({
                type: "POST",
                url: `/pass_manager/view_pass`,
                data: master_pass,
                success: function(data1) {
                    
                    if (data1.status == "error"){
                        toastr.error(data1.message);
                    }
                    else if (data1.status == "success"){
                        $('.view-pass').modal('hide')
                        $('.view-pass-name').val('')
                        $('#username-'+data1.password_id).html(data1.username);
                        $('#password-'+data1.password_id).html(data1.password);
                        // $('#show-btn-'+data1.password_id).css({display:'none'});
                        // $('#unshow-btn-'+data1.password_id).css({display:'block'});
                        setTimeout(function() {
                            $('#username-'+data1.password_id).html('*****');
                            $('#password-'+data1.password_id).html('*****');
                          }, 10000);

                        toastr.success(data1.message);
                    }
                }
                })
        }
    });
 });

 document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-pass-btn').forEach(function(button) {
        button.onclick = function(e) {
            e.preventDefault()
            var entry_id = button.dataset.passid;
            form_id = "#delete-pass-form-"+entry_id
            var master_pass = $(form_id).serialize()
            $.ajax({
                type: "POST",
                url: `/pass_manager/delete_entry`,
                data: master_pass,
                success: function(data1) {
                    
                    if (data1.status == "error"){
                        toastr.error(data1.message);
                    }
                    else if (data1.status == "success"){
                        $('.delete-pass').modal('hide')
                        $('.delete-pass-name').val('')
                        

                        toastr.success(data1.message);
                    }
                }
                })
        }
    });
 });