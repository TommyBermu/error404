import os

from django.core.management.base import BaseCommand

from accounts.models import AppUser


class Command(BaseCommand):
    help = "Create or update a default admin user for demos and manual testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default=os.getenv("DEFAULT_ADMIN_USERNAME", "admin"),
            help="Username for the admin account (default: admin or DEFAULT_ADMIN_USERNAME)",
        )
        parser.add_argument(
            "--email",
            default=os.getenv("DEFAULT_ADMIN_EMAIL", "admin@safe.com"),
            help="Email for the admin account (default: admin@safe.com or DEFAULT_ADMIN_EMAIL)",
        )
        parser.add_argument(
            "--password",
            default=os.getenv("DEFAULT_ADMIN_PASSWORD", "Admin123!"),
            help=(
                "Password for the admin account (default: Admin123! or DEFAULT_ADMIN_PASSWORD). "
                "Use --reset-password to force applying it if the user already exists."
            ),
        )
        parser.add_argument(
            "--role",
            default=os.getenv("DEFAULT_ADMIN_ROLE", AppUser.UserRole.ANALISTA_TH),
            choices=[choice[0] for choice in AppUser.UserRole.choices],
            help="Business role assigned to the admin account (default: analistaTH).",
        )
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="Reset the password even if the account already exists.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]
        role = options["role"]
        reset_password = options["reset_password"]

        defaults = {
            "email": email,
            "first_name": "Admin",
            "last_name": "User",
            "role": role,
            "status": AppUser.UserStatus.ACTIVE,
        }
        user, created = AppUser.objects.get_or_create(username=username, defaults=defaults)

        if not created:
            if user.email != email:
                user.email = email
            if user.role != role:
                user.role = role
            if user.status != AppUser.UserStatus.ACTIVE:
                user.status = AppUser.UserStatus.ACTIVE
            if user.first_name != "Admin":
                user.first_name = "Admin"
            if user.last_name != "User":
                user.last_name = "User"

        if created or reset_password:
            user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            message = f"Admin user created: username='{username}', email='{email}'."
        elif reset_password:
            message = (
                f"Admin user updated and password reset: username='{username}', "
                f"email='{email}'."
            )
        else:
            message = (
                f"Admin user updated: username='{username}', email='{email}'. "
                "Password left unchanged; use --reset-password to force a new one."
            )

        self.stdout.write(self.style.SUCCESS(message))
