from django.core.management.base import BaseCommand, CommandError

from popolo.models import Person

class Command(BaseCommand):
    args = "<PERSON-ID> <SCHEME> <IDENTIFIER>"
    help = "Add an identifier to a particular person"

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        if len(args) != 3:
            raise CommandError("You must provide all three arguments")

        person_id, scheme, identifier = args

        person = Person.objects.get(id=person_id)

        person.identifiers.append(
            {
                'scheme': scheme,
                'identifier': identifier,
            }
        )

        person.save()

        # FIXME: this should create a new version in the versions
        # array too, otherwise you manually have to edit on the
        # YourNextRepresentative site too to create a new version with
        # a change message.

        self.stdout.write("Successfully updated {0}\n".format(person_id))
