from django.db import models
from django.contrib.auth.models import User


class Wilayah(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    kode = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # class Meta:
    #     abstract = True # untuk membuat model abstrak
    
    def __str__(self):
        return self.nama

JENIS_KELAMIN = [
    ('Laki-laki', 'Laki-laki'),
    ('Perempuan', 'Perempuan'),
]

class Masyarakat(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    nik = models.CharField(max_length=16, unique=True, null=True, blank=True)
    no_kk = models.CharField(max_length=16, unique=False, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    
    jenis_kelamin = models.CharField(max_length=100, choices=JENIS_KELAMIN, null=True, blank=True)
    tempat_lahir = models.CharField(max_length=100, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    
    alamat = models.TextField(null=True, blank=True)
    rt = models.CharField(max_length=5, null=True, blank=True)
    rw = models.CharField(max_length=5, null=True, blank=True)
    desa = models.CharField(max_length=100, null=True, blank=True)
    kecamatan = models.CharField(max_length=100, null=True, blank=True)
    kabupaten = models.CharField(max_length=100, null=True, blank=True)
    provinsi = models.CharField(max_length=100, null=True, blank=True)
    
    no_hp = models.CharField(max_length=13, null=True, blank=True)
    
    wilayah = models.ForeignKey(Wilayah, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.nama}"
    



