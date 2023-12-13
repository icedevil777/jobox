from django import forms


class SignUpForm(forms.Form):
    inn = forms.CharField(label="ИНН", max_length=12, min_length=8)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", min_length=8, max_length=32)
    password_repeat = forms.CharField(label="Пароль повторно", min_length=8, max_length=32)


class SignUpappForm(forms.Form):
    tel = forms.CharField(label="Телефон", max_length=20, min_length=11)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", min_length=8, max_length=32)
    password_repeat = forms.CharField(label="Пароль повторно", min_length=8, max_length=32)


class SignInForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", min_length=8, max_length=32)


class ForgotPasswordFormKey(forms.Form):
    key = forms.CharField(max_length=12)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")


class SignReForm(forms.Form):
    password1 = forms.CharField(label="Пароль1", min_length=6, max_length=32)
    password2 = forms.CharField(label="Пароль2", min_length=6, max_length=32)
    # password2 = forms.PasswordInput()


class EditAdministratorInfo(forms.Form):
    name = forms.CharField(max_length=250)
    position = forms.CharField(max_length=250)
    phone = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=250)


class EditCompanyDescription(forms.Form):
    description = forms.CharField(max_length=4096)


class EditUserPasswordForm(forms.Form):
    password = forms.CharField(label="Пароль", min_length=8, max_length=32)
    new_password = forms.CharField(label="Пароль", min_length=8, max_length=32)
    new_password_repeat = forms.CharField(label="Пароль повторно", min_length=8, max_length=32)

