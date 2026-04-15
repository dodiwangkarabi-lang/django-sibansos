# kelola data masyarakat (crud)

from masyarakat.models import Masyarakat

class KelolaDataMasyarakat:
    def __init__(self):
        pass
    
    @staticmethod
    def get_all_masyarakat():
        return Masyarakat.objects.all()
    
    @staticmethod
    def create_masyarakat(data):
        masyarakat = Masyarakat()
        masyarakat.nik = data['nik']
        masyarakat.no_kk = data['no_kk']
        masyarakat.nama = data['nama']
        masyarakat.jenis_kelamin = data['jenis_kelamin']
        masyarakat.tempat_lahir = data['tempat_lahir']
        masyarakat.tanggal_lahir = data['tanggal_lahir']
        masyarakat.alamat = data['alamat']
        masyarakat.rt = data['rt']
        masyarakat.rw = data['rw']
        masyarakat.desa = data['desa']
        masyarakat.kecamatan = data['kecamatan']
        masyarakat.kabupaten = data['kabupaten']
        masyarakat.provinsi = data['provinsi']
        masyarakat.no_hp = data['no_hp']
        masyarakat.wilayah = data['wilayah']
        masyarakat.save()
        return masyarakat
    
    @staticmethod
    def update_masyarakat(id, data):
        masyarakat = Masyarakat.objects.get(id=id)
        masyarakat.nik = data['nik']
        masyarakat.no_kk = data['no_kk']
        masyarakat.nama = data['nama']
        masyarakat.jenis_kelamin = data['jenis_kelamin']
        masyarakat.tempat_lahir = data['tempat_lahir']
        masyarakat.tanggal_lahir = data['tanggal_lahir']
        masyarakat.alamat = data['alamat']
        masyarakat.rt = data['rt']
        masyarakat.rw = data['rw']
        masyarakat.desa = data['desa']
        masyarakat.kecamatan = data['kecamatan']
        masyarakat.kabupaten = data['kabupaten']
        masyarakat.provinsi = data['provinsi']
        masyarakat.no_hp = data['no_hp']
        masyarakat.wilayah = data['wilayah']
        masyarakat.save()
        return masyarakat
    
    @staticmethod
    def delete_masyarakat(id):
        Masyarakat.objects.get(id=id).delete()