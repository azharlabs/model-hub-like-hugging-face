
$('#basicinfo-btn').click(function(){
    console.log("basic info called");
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
        url: "/accounts/save_basicinfo/",
        type: "POST",
        data:{ 
          'firstname': $('#firstname').val(), 
          'lastname': $('#lastname').val(), 
          'phone': $('#phone').val(), 
          'company': $('#company').val(), 
          'account_type1': $('#account_type1:checked').val(), 
          'account_type2': $('#account_type2:checked').val(),
          'address1': $('#address1').val(), 
          'address2': $('#address2').val(), 
          'zipcode': $('#zipcode').val(),
          csrfmiddlewaretoken: csrftoken },
            dataType : "html",
        success: function (data) {
          console.log(data);
          if (data=='Success') {
            const settingToast = new bootstrap.Toast(document.querySelector('#notificationsettingToast'))
            $('#notificationsettingToast-body').html('Basic information chages saved')
            settingToast.show();
          
          };
          
        }
    });
});


$('#changepassword-btn').click(function(){
  console.log("change password called");
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
$.ajax({
      url: "/accounts/change_password/",
      type: "POST",
      data:{ 
        'old_password': $('#id_old_password').val(), 
        'new_password1': $('#id_new_password1').val(), 
        'new_password2': $('#id_new_password2').val(),
        csrfmiddlewaretoken: csrftoken },
          dataType : "html",
      success: function (data) {
        console.log(data);
        
          const settingToast = new bootstrap.Toast(document.querySelector('#notificationsettingToast'))
          $('#notificationsettingToast-body').html(data)
          settingToast.show();
          $('#id_old_password').val('');
          $('#id_new_password1').val('');
          $('#id_new_password2').val('');
          if (data=="Password changes Successfully"){
            location.reload(true);
          }
          

      }
  });
});

$('#email-btn').click(function(){
  console.log("email changes function called");
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
$.ajax({
      url: "/accounts/save_email/",
      type: "POST",
      data:{ 
        'email': $('#email').val(), 
        csrfmiddlewaretoken: csrftoken },
          dataType : "html",
      success: function (data) {
        console.log(data);
        
          const settingToast = new bootstrap.Toast(document.querySelector('#notificationsettingToast'))
          $('#notificationsettingToast-body').html(data)
          settingToast.show();
          $('#email').val('');
          if (data=="Email is changed"){
            location.reload(true);
          }
      }
  });
});


$('#notification-permission-btn').click(function(){
  console.log("basic info called");
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
$.ajax({
      url: "/notification/save_permission/",
      type: "POST",
      data:{ 
        'feature_update': $('#feature_update:checked').val(),
        'interested_blog_update': $('#interested_blog_update:checked').val(), 
        'new_device_signin': $('#new_device_signin:checked').val(),
        csrfmiddlewaretoken: csrftoken },
          dataType : "html",
      success: function (data) {
        console.log(data);
        
          const settingToast = new bootstrap.Toast(document.querySelector('#notificationsettingToast'))
          $('#notificationsettingToast-body').html(data)
          settingToast.show();
        
     
        
      }
  });
});


$('#account-preferences-btn').click(function(){
  console.log("account preference function called");
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
$.ajax({
      url: "/accounts/save_preferences/",
      type: "POST",
      data:{ 
        'early_release': $('#early_release:checked').val(),
        'profile_viewed': $('#profile_viewed:checked').val(), 
        csrfmiddlewaretoken: csrftoken },
          dataType : "html",
      success: function (data) {
        console.log(data);
        
          const settingToast = new bootstrap.Toast(document.querySelector('#notificationsettingToast'))
          $('#notificationsettingToast-body').html(data)
          settingToast.show();

          
        
     
        
      }
  });
});





$('#team-add-btn').click(function(){
  console.log("team add function called");
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
$.ajax({
      url: "/dashboard/teams/add/",
      type: "POST",
      data:{ 
        'title': $('#team_title').val(),
        'description': $('#team_description').val(), 
        csrfmiddlewaretoken: csrftoken },
          dataType : "html",
      success: function (data) {
        console.log(data);
        
          const settingToast = new bootstrap.Toast(document.querySelector('#notificationsettingToast'))
          $('#notificationsettingToast-body').html(data)
          
        
          if (data=="Team added"){
            location.reload(true);
          }else{
        
            $('#team_title').val('');
            $('#team_description').val('');
            $('#shareWithPeopleModal').click();
            
            settingToast.show();
           
          }
        
      }
  });
});
