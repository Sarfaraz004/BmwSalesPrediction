from django.core.management.base import BaseCommand
from prediction.ML_models import train_model

class Command(BaseCommand):
    help = "Retrains the BMW Sales Prediction model with updated data.csv"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🚀 Starting model retraining..."))
        train_model.retrain_model()
        self.stdout.write(self.style.SUCCESS("✅ Model retrained and saved successfully!"))
