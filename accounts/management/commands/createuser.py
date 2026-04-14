# accounts/management/commands/createuser.py

from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Create a user with role and branch"

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("email")
        parser.add_argument("role")
        parser.add_argument("password")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        role = options["role"].lower()
        password = options["password"]

        allowed_roles = [r[0] for r in CustomUser.ROLE_CHOICES]

        if role not in allowed_roles:
            self.stdout.write(self.style.ERROR(
                f"Invalid role. Allowed roles: {allowed_roles}"
            ))
            return


        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_role=role,
        )

        if role == "guide":
            user.is_staff = True
            user.is_superuser = False

        elif role == "coordinator":
            user.is_staff = True
            user.is_superuser = True

        user.save()


        self.stdout.write(
            self.style.SUCCESS(
                f"User Created → {user.username} ({user.user_role})"
            )
        )
