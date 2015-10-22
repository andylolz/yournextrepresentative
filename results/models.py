from django.contrib.auth.models import User
from django.db import models

class ResultEvent(models.Model):

    class Meta:
        ordering = ['created']

    created = models.DateTimeField(auto_now_add=True)
    election = models.CharField(blank=True, null=True, max_length=512)
    winner_popit_person_id = models.CharField(blank=False, max_length=256)
    winner_person_name = models.CharField(blank=False, max_length=1024)
    post_id = models.CharField(blank=False, max_length=256)
    post_name = models.CharField(blank=True, null=True, max_length=1024)
    winner_party_id = models.CharField(blank=True, null=True, max_length=256)
    source = models.CharField(max_length=512)
    user = models.ForeignKey(User, blank=True, null=True)
    proxy_image_url_template = \
        models.CharField(blank=True, null=True, max_length=1024)
    parlparse_id = models.CharField(blank=True, null=True, max_length=256)

    @property
    def winner_party_name(self):
        from candidates.election_specific import PARTY_DATA
        return PARTY_DATA.party_id_to_name.get(self.winner_party_id)

    @classmethod
    def create_from_popit_person(cls, popit_person, election, source, user):
        kwargs = {
            'election': election,
            'winner_popit_person_id': popit_person.id,
            'winner_person_name': popit_person.name,
            'post_id': popit_person.standing_in[election]['post_id'],
            'post_name': popit_person.standing_in[election]['name'],
            'winner_party_id': popit_person.party_memberships[election]['id'],
            'source': source,
            'user': user,
            'parlparse_id': popit_person.get_identifier('uk.org.publicwhip')
        }
        if popit_person.proxy_image:
            kwargs['proxy_image_url_template'] = \
                '{base}/{{width}}/{{height}}.{{extension}}'.format(
                    base=popit_person.proxy_image
                )
        return ResultEvent.objects.create(**kwargs)
