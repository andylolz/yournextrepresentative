# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import models, migrations

from popolo.importers.popit import PopItImporter

class YNRPopItImporter(PopItImporter):

    person_id_to_json_data = {}

    def __init__(self, apps, schema_editor):
        self.apps = apps
        self.schema_editor = schema_editor

    def update_person(self, person_data):
        new_person_data = person_data.copy()
        # There are quite a lot of summary fields in PopIt that are
        # way longer than 1024 characters.
        new_person_data['summary'] = (person_data.get('summary') or '')[:1024]
        # Surprisingly, quite a lot of PopIt email addresses have
        # extraneous whitespace in them, so strip any out to avoid
        # the 'Enter a valid email address' ValidationError on saving:
        email = person_data.get('email') or None
        if email:
            email = re.sub(r'\s*', '', email)
        new_person_data['email'] = email
        person_id, person = super(YNRPopItImporter, self).update_person(new_person_data)

        self.person_id_to_json_data[person_id] = new_person_data
        return person_id, person

    def update_post(self, post_data, area, org_id_to_django_object):
        post_id, post = super(YNRPopItImporter, self).update_post(post_data, area, org_id_to_django_object)

        PostExtra = self.get_model_class('candidates', 'PostExtra')
        post_extra, created = PostExtra.objects.get_or_create(base=post)
        post_extra.candidates_locked = post_data.get('candidates_locked', False)
        post_extra.save()

        return post_id, post

    def update_membership(
        self,
        membership_data,
        area,
        org_id_to_django_object,
        post_id_to_django_object,
        person_id_to_django_object,
    ):
        membership_id, membership = super(YNRPopItImporter, self).update_membership(
            membership_data,
            area,
            org_id_to_django_object,
            post_id_to_django_object,
            person_id_to_django_object,
        )

        election_slug = membership_data.get('election', None)
        if election_slug is not None:
            Election = self.get_model_class('elections', 'Election')
            election = Election.objects.get(slug=election_slug)

            if membership.role == election.candidate_membership_role:
                MembershipExtra = self.get_model_class('candidates', 'MembershipExtra')
                me, created = MembershipExtra.objects.get_or_create(
                    base=membership,
                    election=election
                )

                person_data = self.person_id_to_json_data[membership.person_id]
                party = person_data['party_memberships'].get(election.slug)
                if party is not None:
                    membership.on_behalf_of = org_id_to_django_object[party['id']]
                    membership.save()

        return membership_id, membership

    def make_contact_detail_dict(self, contact_detail_data):
        new_contact_detail_data = contact_detail_data.copy()
        # There are some contact types that are used in PopIt that are
        # longer than 12 characters...
        new_contact_detail_data['type'] = contact_detail_data['type'][:12]
        return super(YNRPopItImporter, self).make_contact_detail_dict(new_contact_detail_data)

    def make_link_dict(self, link_data):
        new_link_data = link_data.copy()
        # There are some really long URLs in PopIt, which exceed the
        # 200 character limit in django-popolo.
        new_link_data['url'] = new_link_data['url'][:200]
        return super(YNRPopItImporter, self).make_link_dict(new_link_data)


def import_from_popit(apps, schema_editor):
    importer = YNRPopItImporter(apps, schema_editor)
    filename = '/home/mark/yournextrepresentative/export.json'
    importer.import_from_export_json(filename)


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_membershipextra_organizationextra_personextra_postextra'),
        ('popolo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_from_popit),
    ]
