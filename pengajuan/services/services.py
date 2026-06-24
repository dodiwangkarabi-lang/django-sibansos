from pengajuan.models import Pengajuan
from penyaluran.models import PenerimaBantuan

from core.services import EmailService

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
            
            # kirim notifikasi ke email
            EmailService.send_email(
                subject="Permohonan Bantuan",
                message=f"Permohonan bantuan ({pengajuan.bantuan.nama}) telah diterima",
                recipient_list=[pengajuan.masyarakat.user.email]
            )
            
        if pengajuan.status == "ditolak":
            PenerimaBantuan.objects.filter(
                masyarakat=pengajuan.masyarakat,
                bantuan=pengajuan.bantuan
            ).delete()
            
            # kirim notifikasi ke email
            EmailService.send_email(
                subject="Permohonan Bantuan",
                message=f"Permohonan bantuan ({pengajuan.bantuan.nama}) telah ditolak",
                recipient_list=[pengajuan.masyarakat.user.email]
            )
            