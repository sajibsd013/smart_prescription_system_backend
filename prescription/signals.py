from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from .models import PrescriptionVersionHistory
from django.db.models import ForeignKey
from prescription.middleware.current_request import get_current_request
User = get_user_model()

INCLUDE_MODELS = [
    "Prescription",  # your history table
]

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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_and_ip():
    request = get_current_request()
    user = getattr(request, 'user', None) if request else None
    ip_address = get_client_ip(request) if request else None
    return user, ip_address

@receiver(post_save)
def save_version(sender, instance, created, **kwargs):

    print(instance.id)

    if sender.__name__ not in INCLUDE_MODELS:
        return

    user, ip_address = get_user_and_ip()

    data = serialize_instance(instance)

    last_version = PrescriptionVersionHistory.objects.filter(
        prescription=instance
    ).order_by('-version_number').first()

    new_version_number = (last_version.version_number + 1) if last_version else 1

    PrescriptionVersionHistory.objects.create(
        prescription=instance,
        version_number=new_version_number,
        action_type='create' if created else 'update',
        changes=data,
        changed_by = user,
        ip_address = ip_address
    )


@receiver(post_delete)
def delete_version(sender, instance, **kwargs):
    if sender.__name__ not in INCLUDE_MODELS:
        return

    user, ip_address = get_user_and_ip()
    data = serialize_instance(instance)

    last_version = PrescriptionVersionHistory.objects.filter(
        prescription=instance.pk
    ).order_by('-version_number').first()

    new_version_number = (last_version.version_number + 1) if last_version else 1

    PrescriptionVersionHistory.objects.create(
        prescription=instance.pk,
        version_number=new_version_number,
        action_type='delete',
        changes=data,
        changed_by=user,
        ip_address=ip_address
    )
