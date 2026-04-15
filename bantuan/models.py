from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(null=True, blank=True)
    aktif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nama

class Bantuan(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(null=True, blank=True)
    
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    
    tanggal_dibuat = models.DateField(auto_now_add=True)
    tanggal_diperbarui = models.DateField(auto_now=True)
    aktif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nama
    

