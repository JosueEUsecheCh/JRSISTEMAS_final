from django import forms
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from .models import User_register

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User_register
        fields = ['name', 'last_name', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': RegionalPhoneNumberWidget(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User_register.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado")
        return email

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        password = self.cleaned_data["password1"]
        if password:
            user.set_password(password)  # Cifra la contraseña
        if commit:
            user.save()
        return user


class CodigoVerificacionForm(forms.Form):
    email = forms.EmailField()
    verification_code = forms.CharField(max_length=6)



class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))