from django.core.management.base import BaseCommand, CommandError
from bot.handlers import init_bot

class Command(BaseCommand):

    def handle(self, *args, **options):
        init_bot(self)
