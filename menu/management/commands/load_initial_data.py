import json
import csv
from django.core.management.base import BaseCommand
from menu.models import Category, Dish
from django.db import transaction

class Command(BaseCommand):
    help = 'Load initial data from JSON or CSV files'

    def add_arguments(self, parser):
        parser.add_argument('file', help='Path to JSON or CSV file')

    def handle(self, *args, **options):
        file_path = options['file']
        if file_path.endswith('.json'):
            self.load_json(file_path)
        elif file_path.endswith('.csv'):
            self.load_csv(file_path)
        else:
            self.stderr.write('Unsupported file format. Use .json or .csv')

    def load_json(self, path):
        with open(path) as f:
            data = json.load(f)
        self._load_data(data)

    def load_csv(self, path):
        data = []
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        self._load_data(data)

    @transaction.atomic
    def _load_data(self, data):
        for item in data:
            category_name = item.get('category')
            category, _ = Category.objects.get_or_create(name=category_name)
            Dish.objects.update_or_create(
                name=item['name'],
                defaults={
                    'description': item.get('description', ''),
                    'price': item.get('price', 0),
                    'category': category,
                    'is_vegetarian': item.get('is_vegetarian', False),
                    'is_gluten_free': item.get('is_gluten_free', False),
                }
            )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
