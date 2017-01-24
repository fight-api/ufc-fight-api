from django.core.management import BaseCommand
from scraping.scraping_functions import SherdogEvents


class Command(BaseCommand):

    def handle(self, *args, **options):
        sh = SherdogEvents()
        sh.scrape_events()
