from appGastos.models import Usuarios


class CustomAuthUser:
    def authenticate(self, email=None, senha=None):
        try:
            user = Usuarios.objects.get(email=email)
            if user.check_password(senha):
                return user
        except Exception:
            pass
        return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Exception:
            return None
