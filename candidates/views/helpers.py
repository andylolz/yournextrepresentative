from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect

from slugify import slugify

from ..election_specific import AREA_POST_DATA
from ..models import (
    PopItPerson, membership_covers_date
)

def get_redirect_to_post(election, post_data):
    short_post_label = AREA_POST_DATA.shorten_post_label(
        election, post_data['label']
    )
    return HttpResponseRedirect(
        reverse(
            'constituency',
            kwargs={
                'election': election,
                'post_id': post_data['id'],
                'ignored_slug': slugify(short_post_label),
            }
        )
    )

def get_party_people_for_election_from_memberships(
        election,
        party_id,
        memberships
):
    people = []
    election_data = settings.ELECTIONS[election]
    for membership in memberships:
        if not membership.get('role') == election_data['candidate_membership_role']:
            continue
        person = PopItPerson.create_from_dict(membership['person_id'])
        if person.party_memberships[election]['id'] != party_id:
            continue
        position_in_list = membership.get('party_list_position')
        if position_in_list:
            position_in_list = int(position_in_list)
        else:
            position_in_list = None
        people.append((position_in_list, person))
    people.sort(key=lambda t: (t[0] is None, t[0]))
    return people

def get_people_from_memberships(election_data, memberships):
    current_candidates = set()
    past_candidates = set()
    for membership in memberships:
        if not membership.get('role') == election_data['candidate_membership_role']:
            continue
        person = PopItPerson.create_from_dict(membership['person_id'])
        if membership_covers_date(
                membership,
                election_data['election_date']
        ):
            current_candidates.add(person)
        else:
            for other_election, other_election_data in settings.ELECTIONS_BY_DATE:
                if not other_election_data.get('use_for_candidate_suggestions'):
                    continue
                if membership_covers_date(
                        membership,
                        other_election_data['election_date'],
                ):
                    past_candidates.add(person)

    return current_candidates, past_candidates
