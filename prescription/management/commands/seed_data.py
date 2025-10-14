from django.core.management.base import BaseCommand
import pandas as pd
from prescription.models import Complaint, History, Examination, Diagnosis, Advice, FollowUp, Investigation
from medicine.models import Manufacturer, Generic, Drug, DosageForm

def add_prescription_data(model, path ):
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        if model.objects.filter(text=row['text']):
            continue
        model.objects.create(
            text=row['text'],
        )

def add_medicine():
    df = pd.read_csv('data/medicine.csv')
    # Insert Manufacturers
    manufacturers = {name: Manufacturer.objects.get_or_create(name=name)[0] for name in
                     df['Name of the Manufacturer'].unique()}

    # Insert Generics
    generics = {name: Generic.objects.get_or_create(name=name)[0] for name in df['Generic Name'].unique()}

    # Insert Dosage Forms
    dosage_forms = {desc: DosageForm.objects.get_or_create(description=desc)[0] for desc in
                    df['Dosages Description'].unique()}

    # Insert Drugs
    for _, row in df.iterrows():
        Drug.objects.get_or_create(
            brand_name=row['Brand Name'],
            generic=generics[row['Generic Name']],
            strength=row['Strength'],
            dosage_form=dosage_forms[row['Dosages Description']],
            manufacturer=manufacturers[row['Name of the Manufacturer']],
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
        add_medicine()

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
