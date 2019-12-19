from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def add_new_user(self, email, password, **extrafields):
        if not email:
            raise ValueError('Must be Email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extrafields):
        extrafields.setdefault('is_superuser', False)
        extrafields.setdefault('is_staff', False)
        return self.add_new_user(email, password, **extrafields)

    def create_superuser(self, email, password, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)
        if not extrafields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')
        return self.add_new_user(email, password, **extrafields)
