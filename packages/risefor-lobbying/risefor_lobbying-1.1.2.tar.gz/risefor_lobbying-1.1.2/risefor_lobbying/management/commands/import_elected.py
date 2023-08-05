import os
from csv import DictReader
from risefor_lobbying.models import Representative, Phone
from django.core.management.base import BaseCommand
from django.db.models import Value
from django.db.models.functions import Concat
from django.conf import settings
import risefor_lobbying


class Command(BaseCommand):
    help = 'Imports representatives'

    def import_csv(self, options, file_name):
        with open(file_name) as csvFile:
            csvReader = DictReader(csvFile)
            i = 0

            # Importing elected from file
            for row in csvReader:
                already_created = Representative.objects.filter(firstname__iexact=row["PRENOM"],
                                                                lastname__iexact=row["NOM"]).exists()

                if not already_created:
                    representative = Representative()
                    representative.civility = row["CIVILITE"].capitalize()
                    representative.firstname = row["PRENOM"].capitalize()
                    representative.lastname = row["NOM"].capitalize()
                    representative.function = row["FONCTION"].capitalize()
                    representative.title = row["TITRE"].capitalize()
                    representative.protocol_role = row["PROTOCOLE ROLE"].capitalize()
                    representative.protocol_person = row["PROTOCOLE PERSONNE"].capitalize()
                    representative.political_party = row["PARTI"].capitalize()
                    representative.election_department = row["DEPARTEMENT ELECTION"].capitalize()
                    representative.election_region = row["REGION ELECTION"].capitalize()
                    representative.phone_organization = row["TEL ORGANISME"]
                    representative.email_direct = row["EMAIL DIRECT"]
                    #representative.email_organization = row["EMAIL ORGANISME"]
                    #representative.address1 = row["ADRESSE 1"]
                    representative.address2 = row["ADRESSE 2"]
                    representative.postal_code = row["CP"]
                    representative.city = row["VILLE"].capitalize()
                    representative.country = row["PAYS"].capitalize()
                    representative.website = row["WEB"]
                    representative.organization_type = row["TYPE"].capitalize()
                    representative.organization_subtype = row["SOUS TYPE"].capitalize()
                    representative.commune = row["COMMUNES"].capitalize()
                    representative.twitter = row["TWETTER"].capitalize()
                    representative.position_campagne = row["Soutien_RIP"].capitalize()

                    if "MME" in row["CIVILITE"]:
                        representative.photo = settings.SITE_URL + "static/img/avatar_f.png"
                    else:
                        representative.photo = settings.SITE_URL + "static/img/avatar_h.png"

                    representative.photo = row["photo"]
                    representative.save()

                    if row["TEL DIRECT"]:
                        phone = Phone()
                        phone.number = row["TEL DIRECT"]
                        phone.representative = representative
                        phone.save()

                    i = i + 1
                    if options['dev'] and i > 10:
                        break

            # Associating assistants with elected
            for representative in Representative.objects.all():
                if (representative.function == 'Attache parlementaire'):
                    title_array = representative.title.split(' madame ')
                    title_array = title_array[len(title_array) - 1].split(' monsieur ')
                    assistant_name = title_array[len(title_array) - 1]

                    elected_officials = Representative.objects.annotate(
                        search_name=Concat('firstname', Value(' '), 'lastname'))
                    try:
                        elected_official = elected_officials.get(search_name__iexact=assistant_name)
                        elected_official.assistants.add(representative)
                        elected_official.save()
                    except Representative.DoesNotExist:
                        print(assistant_name + ' not found in database')

    def add_arguments(self, parser):
        parser.add_argument(
            '--dev',
            action='store_true',
            help='Dummy data for development',
        )

    def handle(self, *args, **options):
        rise_for_lobbying_path = os.path.abspath(os.path.dirname(risefor_lobbying.__file__))
        file_name = os.path.join(rise_for_lobbying_path,
                                 'elected-officials/fichier_deputes_commissions_rip-animaux.csv')
        self.import_csv(options=options, file_name=file_name)
