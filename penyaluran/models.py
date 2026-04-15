from django.db import models

class PenerimaBantuan(models.Model):
    masyarakat = models.ForeignKey('masyarakat.Masyarakat', on_delete=models.CASCADE)
    bantuan = models.ForeignKey('bantuan.Bantuan', on_delete=models.SET_NULL, null=True, blank=True)
    
    tanggal_terima = models.DateField(auto_now_add=True) # Waktu menerima bantuan
    catatan = models.TextField(null=True, blank=True) # catatan, misalnya kondisi penerima
    aktif = models.BooleanField(default=True)  # Status penerima aktif/tidak
    
    def __str__(self):
        return f"{self.masyarakat} - {self.bantuan}"
