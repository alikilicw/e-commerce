from asyncio.windows_events import NULL
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from .models import CustomUser, Address
from django.utils.text import slugify
from ProductApp.models import Category, Currency, Product
from django.contrib.auth.hashers import check_password, make_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.utils.encoding import force_bytes, force_str  
from django.contrib.sites.shortcuts import get_current_site 
from .tokens import account_activation_token 
from django.utils.html import strip_tags
from django.core import mail  
import os
from .validators import reg_validator, user_change_infos_validator

def login_req(request):
    if request.method == "POST":
        _username_or_email = request.POST.get("username_or_email")
        _password = request.POST.get("password")

        if _username_or_email.find('@') == -1:
            user = authenticate(request, username=_username_or_email, password=_password)
            if user is not None: 
                login(request, user)
                return redirect("homePage")
            else: 
                return render(request, "Account/login.html",{
                    "error" : "Girdiğiniz bilgiler hatalıdır.",
                    "username_or_email" : _username_or_email
                })
        else:
            try:
                _username = CustomUser.objects.get(email=_username_or_email).username
            except CustomUser.DoesNotExist:
                 return render(request, "Account/login.html",{
                    "error" : "Girdiğiniz email adresini kontrol ediniz.",
                    "username_or_email" : _username_or_email
                })

            user = authenticate(request, username=_username, password = _password)
            if user is not None:
                login(request, user)
                return redirect("homePage")
            else: 
                return render(request, "Account/login.html",{
                    "error" : "Girdiğiniz bilgiler hatalıdır.",
                    "username_or_email" : _username_or_email
                })
        
    return render(request, "Account/login.html")

def register_req(request):
    if request.method == "POST":
        _username = request.POST.get("username") if request.POST.get("username") else None
        _email = request.POST.get("email") if request.POST.get("email") else None
        _password = request.POST.get("password") if request.POST.get("password") else None
        _re_password = request.POST.get("re_password") if request.POST.get("re_password") else None
        _tax_no = request.POST.get("tax_num") if request.POST.get("tax_num") else None
        _company_name = request.POST.get("company_name") if request.POST.get("company_name") else None
        _name = request.POST.get("name") if request.POST.get("name") else None
        _first_name = request.POST.get("first_name") if request.POST.get("first_name") else None
        _last_name = request.POST.get("last_name") if request.POST.get("last_name") else None
        _tc = request.POST.get("tc") if request.POST.get("tc") else None
        _agree_term = request.POST.get('agree_term')
        _submit_button = request.POST.get('register_submit')

        if _agree_term != 'true':
            return JsonResponse({'error' : 'Kayıt olabilmek için kullanıcı sözleşmesini kabul etmelisiniz.'})

        m_group = "company" if _submit_button == 'company' else "personal_manu" if _submit_button == 'personal-manu' else 'customer'

        message = reg_validator(m_group, _username, _email, _password, _tax_no, _company_name, _name, _first_name, _last_name, _tc)
        if message is not None:
            return JsonResponse({'error' : message})


        if _company_name is not None:
            slug_string = slugify(_company_name)

            if _password == _re_password:
                if CustomUser.objects.filter(username = _username).exists() and CustomUser.objects.filter(email = _email).exists():
                    return JsonResponse({'error' : 'Girdiğiniz kullanıcı adı ve email değerleri daha önce alınmış.'}) 
                elif CustomUser.objects.filter(email = _email).exists():
                    return JsonResponse({'error' : 'Girdiğiniz email adresi daha önce alınmış.'})
                elif CustomUser.objects.filter(username = _username).exists():
                    return JsonResponse({'error' : 'Girdiğiniz kullanıcı adı daha önce alınmış.'})
                else:
                    user = CustomUser.objects.create_user(
                    username = _username,
                    email = _email,
                    password = _password,
                    name = _company_name,
                    tax_num = _tax_no,
                    slug = slug_string,
                    groups = Group.objects.get(name = "Company")
                    )
                    user.is_active = False
                    user.save()
                    try:
                        email_sender(request, user)
                    except:
                        user.delete()
                        return JsonResponse({'error' : 'Girdiğiniz email adresine mail gönderemiyoruz.'})
                    return JsonResponse({'success' : 'Hesabınızı aktive etmek için mail adresinize gönderdiğimiz aktivasyon linkine tıklayınız.'})
            else: 
                return JsonResponse({"error" : "Girdiğiniz parolalar birbiriyle uyuşmuyor."})

        elif _tc:       
            counter = CustomUser.objects.filter(first_name = _first_name, last_name = _last_name).count()

            if counter == 0:
                slug_string = _first_name + " " + _last_name 
            else:
                slug_string = _first_name + " " + _last_name + str(counter)
            
            slug_string = slugify(slug_string)

            if _password == _re_password:
                if CustomUser.objects.filter(username = _username).exists() and CustomUser.objects.filter(email = _email).exists():
                    return JsonResponse({'error' : 'Girdiğiniz kullanıcı adı ve email değerleri daha önce alınmış.'}) 
                elif CustomUser.objects.filter(email = _email).exists():
                    return JsonResponse({'error' : 'Girdiğiniz email adresi daha önce alınmış.'})
                elif CustomUser.objects.filter(username = _username).exists():
                    return JsonResponse({'error' : 'Girdiğiniz kullanıcı adı daha önce alınmış.'})
                else:
                    user = CustomUser.objects.create_user(
                    username = _username,
                    email = _email,
                    password = _password,
                    tc = _tc,
                    first_name = _first_name,
                    last_name = _last_name,
                    slug = slug_string,
                    name = _name,
                    groups = Group.objects.get(name = "Personal")
                    )
                    user.is_active = False
                    user.save()
                    try:
                        email_sender(request, user)
                    except:
                        user.delete()
                        return JsonResponse({'error' : 'Girdiğiniz email adresine mail gönderemiyoruz.'})
                    return JsonResponse({'success' : 'Hesabınızı aktive etmek için mail adresinize gönderdiğimiz aktivasyon linkine tıklayınız.'})
            else: 
                return JsonResponse({"error" : "Girdiğiniz parolalar birbiriyle uyuşmuyor."})

        else:
            if _password == _re_password:
                if CustomUser.objects.filter(username = _username).exists() and CustomUser.objects.filter(email = _email).exists():
                    return JsonResponse({'error' : 'Girdiğiniz kullanıcı adı ve email değerleri daha önce alınmış.'}) 
                elif CustomUser.objects.filter(email = _email).exists():
                    return JsonResponse({'error' : 'Girdiğiniz email adresi daha önce alınmış.'})
                elif CustomUser.objects.filter(username = _username).exists():
                    return JsonResponse({'error' : 'Girdiğiniz kullanıcı adı daha önce alınmış.'})
                else:
                    user = CustomUser.objects.create_user(
                        username = _username,
                        email = _email,
                        password = _password,
                        first_name = _first_name,
                        last_name = _last_name,
                        groups = Group.objects.get(name = "Normal User")
                    )
                    user.is_active = False
                    user.save()
                    try:
                        email_sender(request, user)
                    except:
                        user.delete()
                        return JsonResponse({'error' : 'Girdiğiniz email adresine mail gönderemiyoruz.'})
                    return JsonResponse({'success' : 'Hesabınızı aktive etmek için mail adresinize gönderdiğimiz aktivasyon linkine tıklayınız.'})
            else:
                return JsonResponse({'error' : 'Girdiğiniz parolalar birbiriyle uyuşmuyor.'})
                
    return render(request, "Account/register.html")

def logout_req(request):
    logout(request)
    return redirect("homePage")

def profilePage(request, slug):
    current_profile = CustomUser.objects.get(slug=slug)
    context = {
        "current_profile" : current_profile,
        "products" : Product.objects.filter(user__slug = slug),
        "categories" : Category.objects.all(),
        "currencies" : Currency.objects.all()
    }

    return render(request, "Account/ProfilePage.html", context)

def userChangeInfos(request, slug): 
    if request.method == 'POST':
        _username = request.POST.get('username') if request.POST.get('username') else None
        _email = request.POST.get('email') if request.POST.get('email') else None
        _name = request.POST.get('name') if request.POST.get('name') else None
        _full_address = request.POST.get('full_address') if request.POST.get('full_address') else None
        _country = request.POST.get('country') if request.POST.get('country') else None
        _city = request.POST.get('city') if request.POST.get('city') else None
        _district = request.POST.get('district') if request.POST.get('district') else None
        _neighbourhood = request.POST.get('neighbourhood') if request.POST.get('neighbourhood') else None
        _phone_num = request.POST.get('phone_num') if request.POST.get('phone_num') else None
        _description = request.POST.get('description') if request.POST.get('description') else None

        if request.POST.get('tc'):
            _first_name = request.POST.get('first_name')
            _last_name = request.POST.get('last_name')
            _tc = request.POST.get('tc')

            message = user_change_infos_validator('personal_manu', _username, _email, None, None, _name, _first_name, _last_name, _tc, _country, _city, _district, _neighbourhood, _full_address)
            if message is not None:
                return JsonResponse({'error' : message})
            

            if CustomUser.objects.filter(username = _username).exists() and CustomUser.objects.filter(email = _email).exists() and _username != CustomUser.objects.get(slug=slug).username and _email != CustomUser.objects.get(slug=slug).email:
                error = "Değiştirmek istediğiniz kullanıcı adı ve email değerleri daha önce alınmış.."
                return JsonResponse({'error' : error})
            elif CustomUser.objects.filter(email = _email).exists() and _email != CustomUser.objects.get(slug=slug).email:
                error = "Değiştirmek istediğiniz kullanıcı adı daha önce alınmış.."
                return JsonResponse({'error' : error})
            elif CustomUser.objects.filter(username = _username).exists() and _username != CustomUser.objects.get(slug=slug).username:
                error = "Değiştirmek istediğiniz email daha önce alınmış.."
                return JsonResponse({'error' : error})
            else: 

                if request.user.address is not None:
                    Address.objects.filter(customuser__username = request.user.username).update(
                        full_address = _full_address,
                        country = _country,
                        district = _district,
                        city = _city,
                        neighbourhood = _neighbourhood
                    )
                elif  _country is not None: 
                    _address = Address.objects.create(
                        full_address = _full_address,
                        country = _country,
                        district = _district,
                        city = _city,
                        neighbourhood = _neighbourhood
                    )
                    CustomUser.objects.filter(slug=slug).update(
                    address = _address,
                    )

                CustomUser.objects.filter(slug=slug).update(
                    username = _username,
                    email = _email, 
                    name = _name, 
                    phone_num = _phone_num,
                    description = _description,
                    first_name = _first_name,
                    last_name = _last_name,
                    tc = _tc
                )
                user = CustomUser.objects.get(slug=slug)

                user.save()
                
                success = "Bilgiler başarıyla kaydedildi.."
                if slug == user.slug:
                    return JsonResponse({'success' : success})

                return JsonResponse({'success' : success, 'slug' : user.slug})
        else: 
            _tax_num = request.POST['tax_num']

            message = user_change_infos_validator('company', _username, _email, _tax_num, _name, None, None, None, None, _country, _city, _district, _neighbourhood, _full_address)
            if message is not None:
                return JsonResponse({'error' : message})

            if CustomUser.objects.filter(username = _username).exists() and CustomUser.objects.filter(email = _email).exists() and _username != CustomUser.objects.get(slug=slug).username and _email != CustomUser.objects.get(slug=slug).email:
                error = "Değiştirmek istediğiniz kullanıcı adı ve email değerleri daha önce alınmış.."
                return JsonResponse({'error' : error})
            elif CustomUser.objects.filter(email = _email).exists() and _email != CustomUser.objects.get(slug=slug).email:
                error = "Değiştirmek istediğiniz kullanıcı adı daha önce alınmış.."
                return JsonResponse({'error' : error})
            elif CustomUser.objects.filter(username = _username).exists() and _username != CustomUser.objects.get(slug=slug).username:
                error = "Değiştirmek istediğiniz email daha önce alınmış.."
                return JsonResponse({'error' : error})
            else: 
                
                if request.user.address is not None:
                    if  _country is None:
                        Address.objects.filter(customuser__username = request.user.username).delete()
                    else:
                        Address.objects.filter(customuser__username = request.user.username).update(
                            full_address = _full_address,
                            country = _country,
                            district = _district,
                            city = _city,
                            neighbourhood = _neighbourhood
                        )
                elif _country is not None: 
                    _address = Address.objects.create(
                        full_address = _full_address,
                        country = _country,
                        district = _district,
                        city = _city,
                        neighbourhood = _neighbourhood
                    )
                    CustomUser.objects.filter(slug=slug).update(
                    address = _address,
                    )

                CustomUser.objects.filter(slug=slug).update(
                    name = _name,
                    username = _username,
                    email = _email, 
                    phone_num = _phone_num,
                    description = _description,
                    tax_num = _tax_num
                )

                user = CustomUser.objects.get(slug=slug)

                user.save()

                success = "Bilgiler başarıyla kaydedildi.."
                if slug == user.slug:
                    return JsonResponse({'success' : success})

                return JsonResponse({'success' : success, 'slug' : user.slug})


def userChangePassword(request, slug):
    _active_password = request.POST['active_password']
    _new_password = request.POST['new_password']
    _new_re_password = request.POST['new_password_again']
    if check_password(_active_password, request.user.password): 
        if _new_password == _new_re_password:
            _new_password = make_password(_new_password)
            CustomUser.objects.filter(slug=slug).update(
                password = _new_password
            )
            # user = authenticate(password = _new_password)
            # login(request, user)
            success = "Şifre başarılı bir şekilde güncellendi."
            return JsonResponse({'success' : success})
        else: 
            error = "Girilen şifreler eşleşmiyor.."
            return JsonResponse({'error' : error})
    else:
        error = "Aktif şifrenizi yanlış girdiniz.."
        return JsonResponse({'error' : error})

from .forms import CustomUserChangeImages

def userChangeImages(request, slug):
    user = CustomUser.objects.get(slug=slug)
    cover_image_path = None
    profile_image_path = None
    if user.cover_image:
        cover_image_path = user.cover_image.path
    if user.profile_image:
        profile_image_path = user.profile_image.path

    form = CustomUserChangeImages(request.POST, request.FILES, instance=user)

    if form.is_valid():
        
        if request.FILES.get('profile_image'):
            if profile_image_path:
                try: 
                    os.remove(profile_image_path)
                except:
                    pass
        if request.FILES.get('cover_image'):
            if cover_image_path:
                try:
                    os.remove(cover_image_path)
                except:
                    pass
    
        form.save()
    
    return redirect('profilePage', slug)

def email_sender(request, user):
    current_site = get_current_site(request)  
    mail_subject = 'Activation link has been sent to your email id'
    message = render_to_string('Account/mail.html', {  
        'user': user,  
        'domain': current_site.domain,  
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
        'token':account_activation_token.make_token(user),  
    })  
    plain_message = strip_tags(message)
    to_email = user.email
    print(to_email)

    mail.send_mail(mail_subject, plain_message, from_email=None, recipient_list=[to_email], html_message=message)
    


def activate(request, uidb64, token):
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True
        user.save()  
        return render(request,'Account/success_verify.html',{'success':'Doğrulama işlemi başarılı! Artık giriş yapabilirsiniz. '})  
    else:  
        return render(request, 'Account/success_verify.html',{'error':'Doğrulama işlemi tamamlanamadı.'})