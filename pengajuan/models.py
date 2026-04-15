from django.db import models
from django.contrib.auth.models import User
from masyarakat.models import Masyarakat
from bantuan.models import Bantuan

STATUS = [
    ("diproses", "Diproses"),
    ("ditolak", "Ditolak"),
    ("diterima", "Diterima"),
    ("revisi", "Perlu Revisi"),
]

class Pengajuan(models.Model):
    masyarakat = models.ForeignKey(Masyarakat, on_delete=models.CASCADE, null=True, blank=True)
    bantuan = models.ForeignKey(Bantuan, on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=100, choices=STATUS, default="Diproses")

    file_pengajuan = models.FileField(upload_to="pengajuan/", null=True, blank=True)

    diverifikasi_oleh = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    tanggal_verifikasi = models.DateField(null=True, blank=True)

    catatan = models.TextField(null=True, blank=True)
    
    tanggal_pengajuan = models.DateField(auto_now_add=True)
    tanggal_diperbarui = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"id: {self.id} {self.masyarakat} - {self.bantuan}"
    
# class Verifikasi(models.Model):
#     pengajuan = models.ForeignKey(Pengajuan, on_delete=models.CASCADE)
#     verifier = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     status = models.CharField(max_length=50)
#     catatan = models.TextField(null=True, blank=True)
    
#     tanggal = models.DateTimeField(auto_now_add=True) # tanggal verifikasi
#     tanggal_diperbarui = models.DateTimeField(auto_now=True)
