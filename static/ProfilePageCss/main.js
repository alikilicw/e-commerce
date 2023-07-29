var x = document.getElementById("edit-profile-stage");
x.style.display = "none";
var y = document.getElementById("products-stage")

var z = document.getElementById("edit-profile-button")
var t = document.getElementById("see-products")
t.style.display = "none";
z.onclick = function() {
    x.style.display = "block";
    y.style.display = "none";
    z.style.display = "none";
    t.style.display = "inline";
}

t.onclick = function() {
    x.style.display = "none";
    y.style.display = "block";
    z.style.display = "inline";
    t.style.display = "none";
}

function passShowFunc() {
    var x = document.getElementById("input-active-pass");
    var y = document.getElementById("input-new-pass");
    var z = document.getElementById("input-new-pass-again");

    if (x.type === "password") {
      x.type = "text";
      y.type = "text";
      z.type = "text";
    } else {
      x.type = "password";
      y.type = "password";
      z.type = "password";
    }
  }


$("#images-change-form").submit(function() {
  $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
  return true;
});

$('#open-add-product-form').click(function(){
  $('#popup').css('display', 'flex')
})

$('#close-add-product-form').on('click', function(e){
    $('.popup').css('display', 'none')
})


$('#input-cover-image').change(function(){
  const file = this.files[0]

  if(file){
    const reader = new FileReader()
    reader.onload = function(){
      const result = reader.result
      $('#img-cover-image').attr('src', result)
    }
    reader.readAsDataURL(file)
  }
  $('#img-cover-image-label').text('Yeni Arkaplan')
})

$('#input-profile-image').change(function(){
  const file = this.files[0]

  if(file){
    const reader = new FileReader()
    reader.onload = function(){
      const result = reader.result
      $('#img-profile-image').attr('src', result)
    }
    reader.readAsDataURL(file)
  }
  $('#img-profile-image-label').text('Yeni Profil')
})

$('#input-product-photo-one').change(function(){
  const file = this.files[0]

  if(file){
    const reader = new FileReader()
    reader.onload = function(){
      const result = reader.result
      $('#img-product-image-1').attr('src', result)
    }
    reader.readAsDataURL(file)
  }
})

$('#input-product-photo-two').change(function(){
  const file = this.files[0]

  if(file){
    const reader = new FileReader()
    reader.onload = function(){
      const result = reader.result
      $('#img-product-image-2').attr('src', result)
    }
    reader.readAsDataURL(file)
  }
})

$('#input-product-photo-three').change(function(){
  const file = this.files[0]

  if(file){
    const reader = new FileReader()
    reader.onload = function(){
      const result = reader.result
      $('#img-product-image-3').attr('src', result)
    }
    reader.readAsDataURL(file)
  }
})


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


$('#changeInfos input[type=text]').not('input[name="username"], input[type=number], input[type=email]').on('change invalid', function() {
  var textfield = $(this).get(0);
  textfield.setCustomValidity('');
  
  if (!textfield.validity.valid) {
    textfield.setCustomValidity('Lütfen bu alanı doldurun.');  
  }
});


$(document).ready(function(){
  if ($('#input-country').val() == ''){
    $('#input-city').attr('disabled', true)
    $('#input-district').attr('disabled', true)
    $('#input-neighbourhood').attr('disabled', true)
    $('#input-full-address').attr('disabled', true)
  }
  else if ($('#input-city').val() == ''){
    $('#input-district').attr('disabled', true)
    $('#input-neighbourhood').attr('disabled', true)
    $('#input-full-address').attr('disabled', true)
  }
  else if ($('#input-district').val() == ''){
    $('#input-neighbourhood').attr('disabled', true)
    $('#input-full-address').attr('disabled', true)
  }
  else if ($('#input-neighbourhood').val() == ''){
    $('#input-full-address').attr('disabled', true)
  }
})

$('#input-country').on('keyup', function(){
  if($(this).val() != ''){
    $('#input-city').attr('disabled', false)
  }
  else{
    $('#input-city').attr('disabled', true)
  }
})
$('#input-city').on('keyup', function(){
  if($(this).val() != ''){
    $('#input-district').attr('disabled', false)
  }
  else{
    $('#input-district').attr('disabled', true)
  }
})
$('#input-district').on('keyup', function(){
  if($(this).val() != ''){
    $('#input-neighbourhood').attr('disabled', false)
  }
  else{
    $('#input-neighbourhood').attr('disabled', true)
  }
})
$('#input-neighbourhood').on('keyup', function(){
  if($(this).val() != ''){
    $('#input-full-address').attr('disabled', false)
  }
  else{
    $('#input-full-address').attr('disabled', true)
  }
})

