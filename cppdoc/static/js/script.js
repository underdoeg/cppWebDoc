$(document).ready(function(){
    $('div.edit').editable('/users/dashboard/edit/{{ user.username }}/', {
     	style: 'display: inline;height: 400px',
        type: 'textarea'
    });
    $('span.edit').editable('/users/dashboard/edit/{{ user.username }}/', {
     	style: 'display: inline'
    });
    $('.col').tinyscrollbar();
})