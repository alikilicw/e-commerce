document.getElementById("navbar-small1").style.display='none';

var x = document.getElementById("company-signup-form")
// x.style.display = "none";

var y = document.getElementById("personal-signup-form")
y.style.display = "none";

var z = document.getElementById("customer-signup-form")
z.style.display = "none";

document.getElementById("company-signup").onclick = function () {
    x.style.display = "block";
    y.style.display = "none";
    z.style.display = "none";
}

document.getElementById("personal-signup").onclick = function () {
    y.style.display = "block";
    x.style.display = "none";
    z.style.display = "none";
}

document.getElementById("customer-signup").onclick = function () {
    z.style.display = "block";
    y.style.display = "none";
    x.style.display = "none";
}

$('input[name="username"]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    $(this).attr('pattern', "^(?=.{5,20}$)(?![])(?!.*[_.]{2})[a-z0-9._]+(?<![])$")

    if ($(this).val().length < 5){
        textfield.setCustomValidity('Kullanıcı adı mininum 5 karakter olmalı.'); 
    }
    else if($(this).val().length > 20){
        textfield.setCustomValidity('Kullanıcı adı maximum 20 karakter olmalı.'); 
    }
    else if (!textfield.validity.valid) {
        console.log("fwawf")
        textfield.setCustomValidity('Kullanıcı adı küçük harf, rakam ve ( _ . ) sembollerinden oluşabilir. Semboller art arda kullanılamaz.');  
    }
});

$('input[type=number]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    $(this).attr('pattern', '^(?=.{}$)(?![])(?!.*[]{}[0-9]+(?<![])$')
    if (!textfield.validity.valid) {
        textfield.setCustomValidity('Bu alan yalnızca rakamları içerebilir.');
    }
});

$('input[type=email]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    if (!textfield.validity.valid) {
      textfield.setCustomValidity('Lütfen geçerli bir email adresi giriniz.');  
    }
});

$('input[type=password]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    $(this).attr('pattern', "^(?=.{5,20}$)(?![])(?!.*[_.]{2})[a-z0-9._]+(?<![])$")

    if ($(this).val().length < 5){
        textfield.setCustomValidity('Şifre mininum 5 karakter olmalı.'); 
    }
    else if($(this).val().length > 20){
        textfield.setCustomValidity('Şifre maximum 20 karakter olmalı.'); 
    }
    else if (!textfield.validity.valid) {
        textfield.setCustomValidity('Şifre küçük harf, rakam ve ( _ . ) sembollerinden oluşabilir. Semboller art arda kullanılamaz.');  
    }
});

$('#company-register-form input[type=text]').not('input[name="username"], input[type=number], input[type=email]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    
    if (!textfield.validity.valid) {
      textfield.setCustomValidity('Lütfen bu alanı doldurun.');  
    }
});
$('#personal-manu-register-form input[type=text]').not('input[name="username"], input[type=number], input[type=email]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    
    if (!textfield.validity.valid) {
      textfield.setCustomValidity('Lütfen bu alanı doldurun.');  
    }
});
$('#customer-register-form input[type=text]').not('input[name="username"], input[type=number], input[type=email]').on('change invalid', function() {
    var textfield = $(this).get(0);
    textfield.setCustomValidity('');
    
    if (!textfield.validity.valid) {
      textfield.setCustomValidity('Lütfen bu alanı doldurun.');  
    }
});

$("#customer-register-form").submit(function(event) {
    event.preventDefault();

    $.ajax({
        type: "POST",
        url: $("#customer-register-form").attr('action'),
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            first_name: $('#customer-first-name').val(),
            last_name: $('#customer-last-name').val(),
            username: $('#customer-username').val(),
            email: $('#customer-email').val(),
            password: $('#customer-password').val(),
            re_password: $('#customer-repassword').val(),
            agree_term: $('#customer-agree-term').prop('checked'),
            register_submit: 'customer'
        },
        success: function(response) {    
            if (response.success){          
                setTimeout(() => {
                    location.replace('login')
                  }, 2500);   
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: response.success,
                    showConfirmButton: false,
                    timer: 2500
                })
            }else if (response.error){
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: response.error,
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        },
    });
});
$("#personal-manu-register-form").submit(function(event) {
    event.preventDefault();

    $.ajax({    
        type: "POST",
        url: $("#personal-manu-register-form").attr('action'),
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            first_name: $('#personal-manu-first-name').val(),
            last_name: $('#personal-manu-last-name').val(),
            username: $('#personal-manu-username').val(),
            email: $('#personal-manu-email').val(),
            password: $('#personal-manu-password').val(),
            re_password: $('#personal-manu-repassword').val(),
            tc: $('#personal-manu-tc').val(),
            name: $('#personal-manu-name').val(),
            agree_term: $('#personal-manu-agree-term').prop('checked'),
            register_submit: 'personal-manu'
        },
        success: function(response) {    
            if (response.success){    
                setTimeout(() => {
                    location.replace('login')
                  }, 2500);      
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: response.success,
                    showConfirmButton: false,
                    timer: 2500
                })
            }else if (response.error){
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: response.error,
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        },
    });
});
$("#company-register-form").submit(function(event) {
    event.preventDefault();

    $.ajax({
        type: "POST",
        url: $("#company-register-form").attr('action'),
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            company_name: $('#company-name').val(),
            tax_num: $('#company-tax-no').val(),
            username: $('#company-username').val(),
            email: $('#company-email').val(),
            password: $('#company-password').val(),
            re_password: $('#company-repassword').val(),
            agree_term: $('#company-agree-term').prop('checked'),
            register_submit: 'company'
        },
        success: function(response) {    
            if (response.success){          
                setTimeout(() => {
                    location.replace('login')
                  }, 2500); 
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: response.success,
                    showConfirmButton: false,
                    timer: 2500
                })
            }else if (response.error){
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: response.error,
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        },
    });
});





