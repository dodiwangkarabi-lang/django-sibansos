from core.utils.utils import _simpan, _filter_model_data

# models
from masyarakat.models import Masyarakat
from django.contrib.auth.models import User, Group

from django.contrib.auth.hashers import make_password

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from accounts.usecases.email import EmailService

import string
import secrets

class Auth:
    def __init__(self):
        pass
    
    def lupa_password(self, user):
        email = user.email
        password_baru = self.buat_password_random()
        
        user.set_password(password_baru)
        user.is_active = True
        user.save()
        
        data = {
            "subject": "Reset Password",
            "message": f"Pasword Baru Anda: {password_baru}",
            "recipient_list": [email]
        }
        
        res = EmailService.send_email(**data) # return 0 or 1
        if res:
            return True
        else:
            return False
    
    def hapus_akun(self, user):
        user.delete()
        return True
    
    def buat_password_random(self, length=12):
        chars = (
            string.ascii_letters +
            string.digits +
            "!@#$%^&*"
        )

        return ''.join(
            secrets.choice(chars)
            for _ in range(length)
        )
        
    
    def get_user_from_reset_link(self, uid, token):
        """
        Decode uid dan validasi token.

        Returns:
            User | None
        """
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return None

            return user

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):
            return None
    
    def get_user_from_uid(self, uid):
        """
        Decode uid dan mengembalikan user.
        
        Returns:
            User | None
        """
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            return User.objects.get(pk=user_id)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):
            return None
    
    def buka_link(self, uid, token):
        

        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)

        if PasswordResetTokenGenerator().check_token(user, token):
            # tampilkan form password baru
            pass
    
    def reset_password(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        url = f"/reset-password/{uid}/{token}/"
        return url
    
    def buat_token(self, user):
        # user = User.objects.get(id=1)
        generator = PasswordResetTokenGenerator()

        token = generator.make_token(user)
        # print(token)
        return token
        
    def validasi_token(self, user, token):
        generator = PasswordResetTokenGenerator()
        is_valid = generator.check_token(user, token)

        if is_valid:
            print("Token valid")
        else:
            print("Token tidak valid")
    
    def login(self):
        pass
    
    def ganti_password(self, user: User, password: str):
        user.set_password(password)
        user.save()
        return
    
    def aktifkan_akun(self, user: User):
        if user.is_active:
            return False
        
        user.is_active = True
        user.save()
        return user
    
    def nonaktifkan_akun(self, user: UserWarning, is_active: bool):
        if not is_active:
            user.is_active = is_active
            user.save()
            return user
        return
    
    def registrasi_akun(self, data: dict) -> tuple:
        """
        

        Args:
            data (dict): _description_

        Returns:
            tuple: user, masyarakat
        """
        data_masyarakat = _filter_model_data(Masyarakat, data)
        data_user = _filter_model_data(User, data)
        
        data_user["password"] = make_password(data_user["password"]) # hash password
        data_user["is_active"] = False
        
        masyarakat = _simpan(Masyarakat(**data_masyarakat), data_masyarakat)
        user = _simpan(User(**data_user), data_user)
        
        # masukkan user ke grup masyarakat
        group = Group.objects.get(name="masyarakat")
        group.user_set.add(user)
        
        # relasi user dan masyarakat
        masyarakat.user = user
        masyarakat.save()
        
        return user, masyarakat