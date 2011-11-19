$(document).ready(function(){
    $('.edit').editable('/users/dashboard/edit/{{ user.username }}/', {
     	style: 'display: inline',
        type: 'textarea',
     });
    $('.col').tinyscrollbar();
})