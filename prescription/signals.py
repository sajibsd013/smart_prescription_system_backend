from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from .models import PrescriptionVersionHistory

User = get_user_model()

INCLUDE_MODELS = [
    "Prescription",  # your history table
]
from django.forms.models import model_to_dict
from django.db.models import ForeignKey, ManyToManyField


def serialize_instance(instance):
    """
    Convert a model instance into a JSON-serializable dictionary.
    ForeignKeys are replaced with their primary key.
    ManyToMany fields are replaced with list of PKs.
    """
    data = model_to_dict(instance, fields=[f.name for f in instance._meta.fields])

    # Convert ForeignKey objects to their primary keys
    for field in instance._meta.fields:
        if isinstance(field, ForeignKey):
            value = getattr(instance, field.name)
            data[field.name] = value.pk if value else None

    # Optional: handle ManyToMany fields
    for field in instance._meta.many_to_many:
        data[field.name] = list(getattr(instance, field.name).values_list('pk', flat=True))

    return data


@receiver(post_save)
def save_version(sender, instance, created, **kwargs):
    print(sender.__name__)
    if sender.__name__ not in INCLUDE_MODELS:
        return

    data = serialize_instance(instance)

    last_version = PrescriptionVersionHistory.objects.filter(
        object_id=instance.pk
    ).order_by('-version_number').first()

    new_version_number = (last_version.version_number + 1) if last_version else 1

    PrescriptionVersionHistory.objects.create(
        object_id=instance.pk,
        version_number=new_version_number,
        change_type='create' if created else 'update',
        data=data
    )


@receiver(post_delete)
def delete_version(sender, instance, **kwargs):
    if sender.__name__ not in INCLUDE_MODELS:
        return

    data = serialize_instance(instance)

    last_version = PrescriptionVersionHistory.objects.filter(
        object_id=instance.pk
    ).order_by('-version_number').first()

    new_version_number = (last_version.version_number + 1) if last_version else 1

    PrescriptionVersionHistory.objects.create(
        object_id=instance.pk,
        version_number=new_version_number,
        change_type='delete',
        data=data
    )
