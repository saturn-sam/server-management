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


    console.log(service_name)
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
            $('#id_service_name').val('')
            // select = document.getElementById('#os_type_dd');
            var appendData1 = "<select name='service_name' class='form-control form-control-sm' id='id_service_name' multiple>" 
            for (var i = 0; i < data1.all_service_list.length; i++) {
                appendData1 += "<option value ='" + data1.all_service_list[i].id + "'>" + data1.all_service_list[i].service_name + "</option>"
            }
            appendData1 += "</select>"
            $('.service-class').html(appendData1)
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




// $('.unshare-user').click(function (event) {
//     event.preventDefault()
//     var kb_id = $('.unshare-kb-id').val()
//     var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
//     var len = checkboxes.length;
//     var unshare_user = new Array();
//     for (var i=0; i<len; i++) {
//         unshare_user.push(checkboxes[i].value)
//         // console.log(checkboxes[i].value)
//     }
//     console.log(unshare_user)
//     $.ajax({
//     type: "POST",
//     url: `/kb/unshare-kb`,
//     data: {
//         csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
//         'unshare_user[]': unshare_user,
//         kb_id:kb_id
//     },
//     success: function(data1) {
        
//         if (data1.status == "error"){
//             toastr.error(data1.message);
//         }
//         else if (data1.status == "success"){
//             $('.modal-share-with').modal('hide')
//             $('#select_share_user').val('')
//             toastr.success(data1.message);
//         }
//     }
//     })
// })