$(document).ready(function(){
   
  
    
    

    function username_validation(){
        // var contact = $(this).val();
        $('#valid').remove()
        var username=$('#id_username').val()
        $('#phone').remove()
        $.ajax({
        url: '/ajax/validate_username/',
        data: {
        'username': username
        },
        dataType: 'json',
        success: function (data) {
        if (data.is_taken) {
            
        $('#id_username').after("<span id='phone' class='text-danger'><img class='img-thumbnail' style='width: 40px' src='../static/error.png'/>User With This Username Already Exists.</span></p> ")
        return false
        }else if(username.length <= 0){
            $('#id_username').after("<span style='color:red' id='phone'><img class='img-thumbnail' style='width: 40px' src='../static/error.png'/>* Username can not be blank !</span>")
            return false
        }
    else {
            $('#id_username').after("<span id='phone' class='text-primary'><img class='img-thumbnail' style='width: 40px' src='../static/success.png'/>&nbsp;Availabel.</span></p> ")
            return true
            
        }
        }
      
        });
        
        }

    function contact_validation(){
         len=$('#id_contact').val()
         var con= /^[0-9]*$/
         $('#error_contact').remove()
         if(len.length>10 || len.length<10 ){
             $("#id_contact").after("<span style='color:red' id='error_contact'>* Contact Number Must Contains 10 digits NUmber !</span>")
             return false
         }else if(!con.test(len)){
            $("#id_contact").after("<span style='color:red' id='error_contact'>* Contact Number Must be digit not a character !</span>")
             return false
         }else{
             return true
         }
    }
    function email_validation()
    {
         len=$('#id_email').val()
         var con= /^[a-zA-Z_.0-9]+@[a-zA-Z]+[.]{1}[a-zA-Z]+$/
         $('#error_email').remove()
         if(!con.test(len)){
            $("#id_email").after("<span style='color:red' id='error_email'>* Please Enter Valid Email Address!</spna>")
             return false
         }else{
             return true
         }
    }
    function password_validation1()
    {
        pass1 = $('#id_password1').val()
        $('#error_password1').remove()
        
        if(pass1.length<=0){
            $('#id_password1').after("<span style='color:red' id='error_password1'>* Password should not be blank !</span>") 
            return false
        }
        else{
            return true
        }
    }

    function password_validation()
    {
        pass1=$('#id_password1').val()
        pass2=$('#id_password2').val()
        $('#error_password2').remove()
        
        if(pass2.length<=0){
            $('#id_password2').after("<span style='color:red' id='error_password2'>* Confirm Password should not be blank !</span>") 
            return false
        }
        
        if(pass1!=pass2){
            $('#id_password2').after("<span style='color:red' id='error_last_name'>* Password not match with Confirm Password !</span>") 
            return false
        }else{
            return true
        }

    }
   
    //registration form validation
   

    // $('#id_phone').blur(function(){
        
    // });

    $('#id_username').blur(function(){
        username_validation()
        
    }); 

    $('#id_contact').blur(function(){
        contact_validation()
        
    }); 

    $('#id_email').blur(function(){
        email_validation()
    });

    $('#id_password1').blur(function(){
        password_validation1()
     });
 
    
    $('#id_password2').blur(function(){
       password_validation()
    });

    $('#singup').submit(function(e) {
        
        if(!(contact_validation() && !(username_validation()) &&  email_validation() && password_validation1() && password_validation())) 
        {
            e.preventDefault()
        } 
    });

$("#id_username").change(function () {
    console.log( $(this).val() );
  });

function pass_validation(){
    len=$('id_password').val()
    $('#error_password').remove()
    if(len.length<=5){
        $('id_password').after("<span style='color:red' id='error_contact'>*Password not less then 5 Digits!</span>")
        return false
    }
    else{
    return true
    }
}

$('#id_password').blur(function(){
    pass_validation()
    });
    
$('#login').submit(function(e) {
    
if(!(Login_contact_validation() && pass_validation())) 
{
    e.preventDefault()
} 
});

})
