from django.db import models

from elections.models import Election
from popolo.models import Person, Organization, Post, Membership

"""Extensions to the base django-popolo classes for YourNextRepresentative

These are done via explicit one-to-one fields to avoid the performance
problems with multi-table inheritance; it's preferable to state when you
want a join or not.

  http://stackoverflow.com/q/23466577/223092

"""


class PersonExtra(models.Model):
    base = models.OneToOneField(Person, related_name='extra')
    # FIXME: have to add multiple images

    def last_party(self):
        party = self.base.memberships.filter(
            organization__classification='Party'
        ).order_by('start_date').last()

        return party.organization

    def get_elected(self, election):
        e = Election.objects.get_by_slug(election)
        # FIXME: need to set post here as well I think
        count = self.base.memberships.filter(
            role=e.winner_membership_role,
            extra__election__slug=election
            ).count()

        if count == 1:
            return True
        return False


class OrganizationExtra(models.Model):
    base = models.OneToOneField(Organization, related_name='extra')

    # For parties, which party register is it on:
    register = models.CharField(blank=True, max_length=512)
    # FIXME: have to add multiple images (e.g. for party logos)


class PostExtra(models.Model):
    base = models.OneToOneField(Post, related_name='extra')

    candidates_locked = models.BooleanField(default=False)
    models.ManyToManyField(Election, related_name='posts')


class MembershipExtra(models.Model):
    base = models.OneToOneField(Membership, related_name='extra')

    party_list_position = models.IntegerField(null=True)
    election = models.ForeignKey(
        Election, blank=True, null=True, related_name='candidacies'
    )
