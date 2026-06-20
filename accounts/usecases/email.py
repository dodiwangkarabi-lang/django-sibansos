from django.conf import settings
from django.core.mail import send_mail


class EmailService:

    @staticmethod
    def send_email(
        subject: str,
        message: str,
        recipient_list: list[str]
    ):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
    # @staticmethod
    # def send_reset_password_email(user):
    #     uid = urlsafe_base64_encode(
    #         force_bytes(user.pk)
    #     )

    #     token = PasswordResetTokenGenerator().make_token(
    #         user
    #     )

    #     reset_url = (
    #         f"{settings.FRONTEND_URL}"
    #         f"/reset-password/{uid}/{token}/"
    #     )

    #     send_mail(
    #         subject="Reset Password",
    #         message=(
    #             "Klik link berikut untuk mereset password:\n\n"
    #             f"{reset_url}"
    #         ),
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[user.email],
    #         fail_silently=False,
    #     )
    
# EmailService.send_email(
#     subject="Test Email",
#     message="Halo dunia",
#     recipient_list=["user@gmail.com"]
# )
        
        