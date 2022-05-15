from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from guardian.shortcuts import assign_perm

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return f'{self.get_full_name()}'

    def get_absolute_url(self):
        return reverse('profiles_detail', args=[self.id])
    #
    # def get_items(self):
    #     all_taxreturns = self.taxreturn_set.all()
    #     if all_taxreturns:
    #         output = all_taxreturns[0].get_items()
    #         for taxreturn in all_taxreturns[1:]:
    #             output = output.union(taxreturn.get_items())
    #     else:
    #         return all_taxreturns
    #     return output


@receiver(post_save, sender=Profile)
def profile_post_save(sender, **kwargs):
    profile, created = kwargs["instance"], kwargs["created"]
    if created and profile.user.username != settings.ANONYMOUS_USER_NAME:
        assign_perm("view_profile", profile.user, profile)
        assign_perm("change_profile", profile.user, profile)
        assign_perm("delete_profile", profile.user, profile)


@receiver(post_delete, sender=Profile)
def profile_post_delete(sender, **kwargs):
    profile = kwargs["instance"]
    profile.user.delete()
