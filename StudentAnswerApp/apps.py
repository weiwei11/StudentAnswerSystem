from django.apps import AppConfig


class StudentanswerappConfig(AppConfig):
    name = 'StudentAnswerApp'

    def ready(self):
        from StudentAnswerApp.signals import *
        pass
