from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'GymBuddyApp.users'
    def ready(self):
        import GymBuddyApp.users.signals