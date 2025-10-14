from django.core.management.base import BaseCommand
import pandas as pd
from prescription.models import Complaint, History, Examination, Diagnosis, Advice, FollowUp, Investigation


def add_prescription_data(model, path ):
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        if model.objects.filter(text=row['text']):
            continue
        model.objects.create(
            text=row['text'],
        )


class Command(BaseCommand):
    help = 'Seed database from CSV file'

    def handle(self, *args, **kwargs):
        add_prescription_data(Complaint, 'data/complaints.csv')
        add_prescription_data(History, 'data/history.csv')
        add_prescription_data(Examination, 'data/examination.csv')
        add_prescription_data(Diagnosis, 'data/diagnosis.csv')
        add_prescription_data(Advice, 'data/advice.csv')
        add_prescription_data(FollowUp, 'data/followup.csv')
        add_prescription_data(Investigation, 'data/investigation.csv')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
