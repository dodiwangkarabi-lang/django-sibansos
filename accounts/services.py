from django.contrib.auth.models import User, Group
from django.db import transaction
from masyarakat.models import Masyarakat


def registrasi_service(data: dict):
    with transaction.atomic():
        # buat user
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
        )
        
        # buat group
        group = Group.objects.get(name="masyarakat")
        group.user_set.add(user)
        
        # buat profil (masyarakat)
        obj_masyarakat = Masyarakat(user=user)
        obj_masyarakat.nik = data["nik"]
        obj_masyarakat.nama = data["nama"]
        obj_masyarakat.save()
        
        # Masyarakat.objects.create(
        #     user = user
        # )
        
    return user