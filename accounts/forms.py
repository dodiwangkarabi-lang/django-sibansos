from django import forms
from django.contrib.auth.models import User
from masyarakat.models import Masyarakat

class MasyarakatForm(forms.ModelForm):
    class Meta:
        model = Masyarakat
        fields = ["nik", "nama"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # aturan form
        self.fields["nik"].required = True
        self.fields["nama"].required = True
        
    def clean(self):
        cleaned_data = super().clean()

        nik = cleaned_data.get("nik")
        nama = cleaned_data.get("nama")

        if nik and len(nik) != 16:
            self.add_error("nik", "NIK harus 16 digit")

        if nama and nama.lower() == "admin":
            self.add_error("nama", "Nama tidak boleh admin")

        return cleaned_data

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        self.password_confirm = cleaned_data.get("password_confirm")
        
        if password != self.password_confirm:
            raise forms.ValidationError("Password tidak sama")
        
        return cleaned_data