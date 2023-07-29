import re

def reg_validator(m_group, username = None, email = None, password = None, tax_num = None, company_name = None, name = None, first_name = None, last_name = None, tc = None):

    message = None

    if username is None:
        message = "Kullanıcı adı boş bırakılamaz."
    else :
        message = username_validator(message, username)  

    if message is None:
        if email is None:
            message = "Email alanı boş bırakılamaz."
        else:
            message = email_validator(message, email)

    if message is None:
        if password is None:
            message = "Şifre alanı boş bırakılamaz."
        else:
            message = password_validator(message, password)

    if m_group == 'company':
        if message is None:
            if company_name is not None:
                message = company_name_validator(message, company_name)
            else:
                message = "Şirketd adı boş bırakılamaz."

        if message is None:
            if tax_num is None:
                message = "Vergi no alanı boş bırakılamaz."
            else:
                message = tax_num_validator(message, tax_num)

    if m_group == 'personal_manu':
        if message is None:
            if name is not None:
                message = name_validator(message, name)

        if message is None:
            if tc is None:
                message = "Tc alanı boş bırakılamaz."
            else:
                message = tc_validator(message, tc)

    if m_group == 'personal_manu' or m_group == 'customer':
        if message is None:
            if first_name is None:
                message = "İsim alanı boş bırakılamaz." 
            else:
                message = first_name_validator(message, first_name)

        if message is None:
            if last_name is None:
                message = "Soyisim alanı boş bırakılamaz."   
            else:
                message = last_name_validator(message, last_name)


    return message


def user_change_infos_validator(m_group, username = None, email = None, tax_num = None, company_name = None, name = None, first_name = None, last_name = None, tc = None, country = None, city = None, district = None, neighbourhood = None, full_address = None):
    
    message = None

    if username is None:
        message = "Kullanıcı adı boş bırakılamaz."
    else:
        message = username_validator(message, username)  

    if message is None:
        if email is None:
            message = "Email alanı boş bırakılamaz."
        else:
            message = email_validator(message, email)

    if m_group == 'company':
        if message is None:
            if company_name is not None:
                message = company_name_validator(message, company_name)
            else:
                message = "Şirketd adı boş bırakılamaz."

        if message is None:
            if tax_num is None:
                message = "Vergi no alanı boş bırakılamaz."
            else:
                message = tax_num_validator(message, tax_num)

    if m_group == 'personal_manu':
        if message is None:
            if name is not None:
                message = name_validator(message, name)

        if message is None:
            if tc is None:
                message = "Tc alanı boş bırakılamaz."
            else:
                message = tc_validator(message, tc)

        if message is None:
            if first_name is None:
                message = "İsim alanı boş bırakılamaz." 
            else:
                message = first_name_validator(message, first_name)

        if message is None:
            if last_name is None:
                message = "Soyisim alanı boş bırakılamaz."   
            else:
                message = last_name_validator(message, last_name)
                
    if message is None:
        address_validator(message, country, city, district, neighbourhood, full_address)


    return message
        

def username_validator(message = None, username = None):
    if len(username) < 5:
        message = "Kullanıcı adı uzunluğu 5 karakterden kısa olamaz!"
    elif len(username) > 20:
        message = "Kullanıcı adı uzunluğu 20 karakterden uzun olamaz!"
    elif re.search(r"^(?!.*[_.]{2})[\w.]+\Z", username) == None:
        message = "Kullanıcı adı küçük harf, rakam ve ( _ . ) sembollerinden oluşabilir. Semboller art arda kullanılamaz."

    return message

def email_validator(message = None, email = None):
    if len(email) < 13:
        message = "Email uzunluğu 13 karakterden kısa olamaz!"
    elif len(email) > 254:
        message = "Email uzunluğu 254 karakterden uzun olamaz!"
    elif re.search(r"^[\w.]+@[a-z]+\.[a-z]{3}\Z", email) == None:
        message = "Lütfen geçerli email adresi giriniz."

    return message
    
def password_validator(message = None, password = None):
    if len(password) < 5:
        message = "Şifrenin uzunluğu 5 karakterden kısa olamaz!"
    elif len(password) > 20:
        message = "Şifrenin uzunluğu 20 karakterden uzun olamaz!"
    elif re.search(r"^(?!.*[_.]{2})[\w.]+\Z", password) == None:
        message = "Şifre küçük harf, rakam ve ( _ . ) sembollerinden oluşabilir. Semboller art arda kullanılamaz."

    return message

def tax_num_validator(message = None, tax_num = None):
    if len(tax_num) != 10:
        message = "Vergi no uzunluğu 10 karakter olmalıdır!"
    elif re.search(r"^[0-9]+\Z", tax_num) == None:
        message = "Vergi no yalnızca rakamlardan oluşabilir."

    return message

def company_name_validator(message = None, company_name = None):
    if len(company_name) > 100:
        message = "Şirket adı uzunluğu 100 karakterden uzun olamaz!"

    return message

def name_validator(message = None, name = None):
    if len(name) > 100:
        message = "Şirket adı uzunluğu 100 karakterden uzun olamaz!"

    return message

def first_name_validator(message = None, first_name = None):
    if len(first_name) > 100:
        message = "İsim uzunluğu 100 karakterden uzun olamaz!"

    return message

def last_name_validator(message = None, last_name = None):
    if len(last_name) > 100:
        message = "Soyisim uzunluğu 100 karakterden uzun olamaz!"

    return message
    
def tc_validator(message = None, tc = None):
    if len(tc) != 11:
        message = "Tc no uzunluğu 11 karakter olmalıdır!"
    elif re.search(r"^[0-9]+\Z", tc) == None:
        message = "Tc no yalnızca rakamlardan oluşabilir."

    return message

def address_validator(message = None, _country = None, _city = None, _district = None, _neighbourhood = None, _full_address = None):
    if len(_country) > 30:
        message = "Ülke alanına max 30 karakter girilebilir!"
    if len(_city) > 50:
        message = "Ülke alanına max 30 karakter girilebilir!"
    if len(_district) > 50:
        message = "Ülke alanına max 30 karakter girilebilir!"
    if len(_neighbourhood) > 70:
        message = "Ülke alanına max 30 karakter girilebilir!"
    if len(_full_address) > 250:
        message = "Ülke alanına max 30 karakter girilebilir!"

    return message