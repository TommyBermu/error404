import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from courses.models import Material, Content


@receiver(post_delete, sender=Content)
def auto_delete_material_on_content_delete(sender, instance, **kwargs):
    if instance.material_id:
        try:
            material = Material.objects.get(pk=instance.material_id)
            # verificar si el material ha quedado huérfano
            if not material.contents.exists():  # pyright: ignore[reportAttributeAccessIssue]
                material.delete()
        except Material.DoesNotExist:
            # material ya fue eliminado
            pass


@receiver(post_delete, sender=Material)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(pre_save, sender=Material)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Material.objects.get(pk=instance.pk).file
    except Material.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)
