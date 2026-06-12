from pengajuan.models import Pengajuan
from penyaluran.models import PenerimaBantuan

class PengajuanService:
    def __init__(self):
        pass
    
    
    def verifikasi_pengajuan(self, pengajuan: Pengajuan):
        
        if pengajuan.status == "diterima":
            penerima_bantuan, crated = PenerimaBantuan.objects.update_or_create(
                masyarakat=pengajuan.masyarakat,
                bantuan=pengajuan.bantuan,
                defaults={
                    "catatan": ""
                }
            )
            
        if pengajuan.status == "ditolak":
            PenerimaBantuan.objects.filter(
                masyarakat=pengajuan.masyarakat,
                bantuan=pengajuan.bantuan
            ).delete()
            