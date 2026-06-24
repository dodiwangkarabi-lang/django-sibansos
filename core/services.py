from pengajuan.models import Pengajuan
from penyaluran.models import PenerimaBantuan
from masyarakat.models import Masyarakat
from django.contrib.auth.models import User, Group

from django.db import transaction

from django.conf import settings
from django.core.mail import send_mail


class EmailService:

    @staticmethod
    def send_email(
        subject: str,
        message: str,
        recipient_list: list[str]
    ):
        """
        kirim email

        Args:
            subject (str): subjek
            message (str): pesan yang dkirim
            recipient_list (list[str]): daftar penerima
        
        Example:
            EmailService.send_email(
                subject="Test Email",
                message="Halo dunia",
                recipient_list=["user@gmail.com"]
            )
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

class KelolaDataPenerimaBantuan:

    def proses_pengajuan(self, pengajuan_id):
        pengajuan = Pengajuan.objects.get(id=pengajuan_id)

        if not self.validasi_kelayakan(pengajuan):
            raise Exception("Tidak layak menerima bantuan")

        if self.sudah_menerima(pengajuan.masyarakat.id, pengajuan.bantuan.id):
            raise Exception("Sudah pernah menerima bantuan")

        penerima = PenerimaBantuan.objects.create(
            masyarakat=pengajuan.masyarakat,
            bantuan=pengajuan.bantuan
        )

        return penerima

    def validasi_kelayakan(self, pengajuan):
        return pengajuan.penghasilan < 2000000

    def sudah_menerima(self, masyarakat_id, bantuan_id):
        return PenerimaBantuan.objects.filter(
            masyarakat_id=masyarakat_id,
            bantuan_id=bantuan_id
        ).exists()
        
class VerifikasiPermohonanService:

    def verifikasi(self, pengajuan_id):
        pengajuan = Pengajuan.objects.get(id=pengajuan_id)

        if not self.validasi(pengajuan):
            pengajuan.status = "ditolak"
            pengajuan.save()
            return pengajuan

        pengajuan.status = "disetujui"
        pengajuan.save()

        # lanjut ke penerima bantuan
        KelolaDataPenerimaBantuan().proses_pengajuan(pengajuan.id)

        return pengajuan

    def validasi(self, pengajuan):
        return pengajuan.penghasilan < 2000000
    
class LaporanService:
    
    @staticmethod
    def daftar_penerima_bantuan():
        return PenerimaBantuan.objects.all()
    
def mengajukan_permohonan_bantuan(masyarakat_id, bantuan_id):
    pengajuan = Pengajuan.objects.create(masyarakat_id=masyarakat_id, bantuan_id=bantuan_id)
    return pengajuan

def revisi_pengajuan_permohonan_bantuan(pengajuan_id, catatan):
    pengajuan = Pengajuan.objects.get(id=pengajuan_id)
    pengajuan.status = "revisi"
    pengajuan.catatan = catatan
    pengajuan.save()
    return pengajuan

# 
    