from masyarakat.models import Masyarakat
from bantuan.models import Bantuan
from penyaluran.models import PenerimaBantuan

class RangkumanData:
    
    @staticmethod    
    def total_masyarakat():
        return Masyarakat.objects.all().count()
    
    @staticmethod
    def total_bantuan():
        return Bantuan.objects.all().count()
    
    @staticmethod
    def total_penerima_bantuan():
        return PenerimaBantuan.objects.all().count()