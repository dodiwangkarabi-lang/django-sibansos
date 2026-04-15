from .models import Pengajuan
from django import forms

class PengajuanForm(forms.ModelForm):
    class Meta:
        model = Pengajuan
        fields = ["bantuan", "file_pengajuan", "catatan"]
        
class VerifikasiPermohonanForm(forms.ModelForm):
    class Meta:
        model = Pengajuan
        fields = ["status", "catatan"]