import itertools
import uuid
from datetime import datetime,date
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.mail import EmailMessage

from djangoldp.models import Model
from djangoldp_conversation.models import Conversation



User = get_user_model()


# appending custom behaviour to User model
def active_actions(self):
    return self.actiongroups.filter(actiondate__gte=date.today())

User.active_actions=active_actions
User.name=User.get_full_name

def convergent_actions(self):
    start_date = datetime(2019, 11, 28)
    end_date = datetime(2019, 12, 9)
    return self.actiongroups.filter(actiondate__gt=start_date,actiondate__lt=end_date)

User.convergent_actions=convergent_actions


class Representative(Model):
    """Displaying contact and functions of elected officials"""
    civility = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Civilité")
    firstname = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Prénom")
    lastname = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Nom")
    function = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Fonction")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Titre")
    protocol_role = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Rôle protocolaire")
    protocol_person = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Personne protocolaire")
    political_party = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Parti politique")
    election_department = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Département d'élection")
    election_region = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"Région d'élection")
    phone_organization = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"Tél. organisation")
    email_direct = models.EmailField(max_length=100, blank=True, null=True, verbose_name=u"Email direct")
    email_organization = models.EmailField(max_length=100, blank=True, null=True, verbose_name=u"Email Organisation")
    address1 = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Adresse 1")
    address2 = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Adresse 2")
    postal_code = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Code postal")
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"Ville")
    country = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"Pays")
    website = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"Site web")
    organization_type = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"Type d'organisation")
    organization_subtype = models.CharField(max_length=150, blank=True, null=True, verbose_name=u"Sous-type d'organisation")
    photo = models.URLField(verbose_name=u"Photo")
    slug = models.SlugField(blank=True, null=True, unique=True)
    permanent_commission = models.CharField(max_length=255, blank=True, verbose_name=u"Commission permanente")
    parliamentary_missions = models.TextField(blank=True, verbose_name=u"Missions parlementaires")
    additional_functions = models.TextField(blank=True, verbose_name=u"Fonctions supplémentaires")
    study_groups = models.TextField(blank=True, verbose_name=u"Groupes d'étude")
    assistants = models.ManyToManyField('Representative', blank=True)
    position_campagne = models.CharField(max_length=255, blank=True, verbose_name=u"Position de l'élue sur la campange")
    commune = models.TextField(blank=True, verbose_name=u"Commune et Code postal")
    twitter = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Compte twitter de l'élu")


    def get_full_name(self):
        return "{} {}".format(self.firstname, self.lastname)

    class Meta:
        serializer_fields = ['@id', 'civility', 'firstname', 'lastname', 'get_full_name', 'function', 'title', 'protocol_role', 'protocol_person', 'political_party', 'election_department', 'election_region', 'direct_phones', 'phone_organization', 'email_direct', 'email_organization', 'address1', 'address2', 'postal_code', 'city', 'country', 'website', 'organization_type', 'organization_subtype', 'photo', 'slug', 'permanent_commission', 'additional_functions', 'parliamentary_missions', 'study_groups', 'assistants', 'actiongroups','commune','twitter','position_campagne']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change']
        ordering = ['lastname']

    def __str__(self):
        if self.firstname and self.lastname:
            return self.firstname + " " + self.lastname
        else:
            return "no name"


class Phone(Model):
    """Phone numbers of elected officials"""
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"Numéro de téléphone")
    representative = models.ForeignKey(Representative, related_name="direct_phones", verbose_name=u"Élu",
                                       on_delete=models.CASCADE)

    def __str__(self):
        return self.number


# TODO: leverage Loomio API to add loomio topics within an action group
class LoomioTopic(Model):
    title = models.CharField(max_length=255, verbose_name=u"Titre du sujet")
    url = models.URLField(verbose_name=u"Loomio", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        serializer_fields = ['@id','title', 'url']


class Theme(Model):
    """Type of ActionGroup"""
    name = models.CharField(max_length=255, verbose_name=u"Nom")
    photo = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Photo")

    def __str__(self):
        return self.name


class OrgType(Model):
    """Type of organisation. E.g. NGO, Citizen Movement.."""
    name = models.CharField(max_length=255, verbose_name=u"Type d'organisation")

    def __str__(self):
        return self.name

class TwitterMessage(Model):
  tweet = models.TextField(max_length=255, verbose_name=u"Tweet")
  
  class Meta:
    serializer_fields = ['@id','tweet']
    nested_fields = ['twitterMessage']
    anonymous_perms = ['view']
    authenticated_perms = ['inherit', 'add']
    owner_perms = ['inherit', 'change', 'control', 'delete']
    ordering = ['tweet']

  def __str__(self):
    return self.tweet
  

class ActionGroup(Model):
    """Connected users can create actions that are visible to all users in the group"""
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name=u"Nom de l'action")
    objective = models.TextField(verbose_name=u"Objectif")
    actiondate = models.DateField(blank=True, null=True, verbose_name=u"Date de l'action")
    endactiondate = models.DateField(blank=True, null=True, verbose_name=u"Date de fin de l'action")
    image = models.URLField(default="/static/img/action_group_blank.png",verbose_name=u"Image", null=True, blank=True)
    theme = models.ForeignKey(Theme, null=True, verbose_name=u"Type d'action", default="Lobbying Citoyen" ,on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True, verbose_name=u"Description")
    members = models.ManyToManyField(User, related_name='actiongroups', blank=True)
    actiongroups = models.ManyToManyField("self", blank=True)
    author = models.ForeignKey(User, related_name='created_groups', blank=True, null=True, on_delete=models.SET_NULL)
    conversation = models.ManyToManyField(Conversation, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Adresse")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Ville")
    postcode = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Code postal")
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name=u"Latitude")
    lng = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name=u"Longitude")

    # Modules
    loomios = models.ManyToManyField(LoomioTopic, blank=True)
    jugementmaj = models.URLField(max_length=9999999, blank=True, null=True,
                                  verbose_name=u"Module jugement majoritaire")
    linkcollabtext = models.URLField(max_length=9999999, blank=True, null=True,
                                     verbose_name=u"Liens vers un texte collaboratif")
    pressreleasetitle = models.CharField(max_length=255,blank=True, null=True, verbose_name=u"Titre du Communiqué de Presse")
    pressreleasecontent = models.TextField(blank=True, null=True, verbose_name=u"Contenu du Communiqué de Presse")

    # elected officials
    electedofficialemailsubject = models.CharField(max_length=255,blank=True, null=True,
                                                   verbose_name=u"Sujet de l'email à  envoyer aux élu.e.s")
    electedofficialemailtext = models.TextField(blank=True, null=True,
                                                verbose_name=u"Texte de l'email à envoyer aux élu.e.s")
    representatives = models.ManyToManyField(Representative, blank=True, related_name='actiongroups')
    #Contact EO on twitt 
    twitterContent = models.CharField(blank=True, null=True,max_length=280, verbose_name=u"Contenu du tweet")
    
    #unhide when issue #393 is solved https://git.happy-dev.fr/startinblox/applications/risefor-lobbying/issues/393
    #twitter_prioEo = models.ManyToManyField(Representative,blank=True, related_name='twitter_prioEo') 
    #prioEo_reason = models.TextField(blank=True, null=True,verbose_name=u"Pourquoi contacter ces élues prioritairement")
    
    #figure out how to show content of this model && of nested field in same sib-display

    # more info on action
    actioninfolink = models.URLField(max_length=9999999, blank=True, null=True,
                                     verbose_name=u"Plus d'informations sur l'action")
    signuplink = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"S'inscrire à l'action")
    # social Media accounts to follow for the action
    facebook = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Compte facebook à suivre")
    instagram = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Compte instagram à suivre")
    twitter = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Compte twitter à suivre")
    #sign call
    calltitle = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Titre du texte à signer")
    callcontent = models.TextField( blank=True, null=True, verbose_name=u"Contenu du texte à signer")
    callmoreinfo = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Lien pour plus d'information")

    #call video
    videotitle = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Titre de la vidéo")
    videourl = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Vidéo associé à l'action")

    #interpellation anyone on twitter
    anytwittContent =  models.CharField(blank=True, null=True,max_length=280, verbose_name=u"Tweet Global - Content")
    anytwittTargets =  models.TextField(blank=True, null=True, verbose_name=u"Tweet Global - Targets")
    anytwittExplination = models.TextField(blank=True, null=True, verbose_name=u"Tweet Global - Explination")

    #Revamp twitter -> Multiple tweets offered
    twitterMessage = models.ManyToManyField(TwitterMessage,related_name="twitterMessage",blank=True)


    class Meta:
        auto_author = 'author'
        serializer_fields = ['@id', 'name', 'author', 'pressreleasetitle', 'pressreleasecontent', 'jugementmaj',
                             'signuplink', 'instagram', 'twitter', 'facebook', 'objective', 'actiondate',
                             'endactiondate', 'image','actioninfolink', 'description', 'theme', 'linkcollabtext',
                             'electedofficialemailsubject', 'electedofficialemailtext', 'representatives', 'members',
                             'actiongroups', 'loomios', 'conversation', 'address', 'city', 'postcode', 'lat', 'lng',
                             'events', 'org_actions','twitterContent','calltitle','callcontent','callmoreinfo','videotitle','videourl','anytwittContent','anytwittTargets','anytwittExplination',
                             'related_text','twitterMessage']
        nested_fields = ["author", "representatives", "loomios", "actiongroups", "conversation", "members", "events",
                         'org_actions','related_text','twitterMessage']
        anonymous_perms = ['view','add']
        authenticated_perms = ['inherit', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']
        owner_field = 'author'
        ordering = ['actiondate']

    def __str__(self):
        return self.name


class Organisation(Model):
    """Organisations can add a page describing their organisation and actions"""
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name=u"Nom de l'association")
    tagline = models.CharField(blank=True, null=True, max_length=600, verbose_name=u"Tagline")
    author = models.ForeignKey(User, related_name='created_ngo', blank=True, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name='ngomembers', blank=True)
    description = models.TextField(blank=True, null=True, verbose_name=u"Description")
    site = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Site du collectif")
    telephone = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"Numéro de téléphone")
    contact_address = models.EmailField(max_length=100, blank=True, null=True, verbose_name=u"NGO Contact email")
    org_actions = models.ManyToManyField(ActionGroup, blank=True, related_name='org_actions')
    logo = models.CharField(default="/static/img/action_group_blank.png", blank=True, null=True,
                            verbose_name="Logo du collectif", max_length=1000)
    slug = models.SlugField(blank=True, null=True, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Adresse")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Ville")
    postcode = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Code postal")
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name=u"Latitude")
    lng = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name=u"Longitude")
    organisation_type = models.ForeignKey(OrgType, verbose_name=u"Type d'organisation", null=True,
                                          on_delete=models.SET_NULL)
    facebook = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Facebook Account")
    twitter = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Twitter Account")
    instagram = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"Instagram Account")
    linkedin = models.URLField(max_length=9999999, blank=True, null=True, verbose_name=u"LinkedIn Account")

    class Meta:
        auto_author = 'author'
        serializer_fields = ['@id', 'name', 'facebook', 'twitter', 'instagram', 'linkedin', 'organisation_type',
                             'tagline', 'members', 'contact_address', 'telephone', 'org_actions', 'logo', 'author',
                             'site', 'description', 'address', 'city', 'postcode', 'lat', 'lng']
        nested_fields = ["author", 'members', 'org_actions']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']
        owner_field = 'author'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Event(Model):
    """An event, as associated with an Action"""
    name = models.CharField(max_length=255, verbose_name=u"Nom de l'évenement")
    image = models.URLField(verbose_name=u"Image", null=True, blank=True)
    date = models.DateField(blank=True, null=True, verbose_name=u"Date de l'évenement")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Lieu")
    theme = models.ForeignKey(Theme, verbose_name=u"Type d'événement", null=True, on_delete=models.SET_NULL)
    organization = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Organisation")
    actiongroup = models.ForeignKey(ActionGroup, related_name="events", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True, verbose_name=u"Description")

    class Meta:
        serializer_fields = ['@id','image', 'name', 'description', 'date', 'location', 'theme', 'actiongroup', 'organization']
        ordering=['-date']

    def __str__(self):
        return self.name

# HelpInstall - one kind of contact form (submitting a request for help installing the tool)


class HelpOrgType(Model):
    """Type of organisation wanting to install the tool"""
    name = models.CharField(max_length=255, verbose_name=u"Type de collectif")

    def __str__(self):
        return self.name


class HelpLevel(Model):
    """A category representing the amount of help needed"""
    name = models.CharField(max_length=255, verbose_name=u"Niveau d'aide nécessaire")

    def __str__(self):
        return self.name


class HelpInstall(Model):
    """Contact form to ask for help in order to deploy Risefor"""
    TRUE_FALSE_CHOICES = (
        (True, 'Oui'),
        (False, 'Non')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    orgname = models.CharField(max_length=255, verbose_name=u"Nom de l'organisation")
    orgType = models.ForeignKey(HelpOrgType, verbose_name=u"Type de collectif", null=True, on_delete=models.SET_NULL)
    helpLevel = models.ForeignKey(HelpLevel, verbose_name=u"Level of technical help needed", null=True, on_delete=models.SET_NULL)
    usage_tool = models.TextField(verbose_name=u"Cadre d'utilisation")
    extra_msg = models.TextField(verbose_name=u"Message supplémentaire")
    contact_email = models.EmailField(max_length=100, verbose_name=u"Adresse email du contact")

    class Meta:
        auto_author = 'contact_email'
        serializer_fields = ['@id', 'created_at', 'extra_msg', 'usage_tool', 'orgname', 'orgType', 'helpLevel',
                             'contact_email']
        anonymous_perms = ['view', 'add']
        authenticated_perms = ['inherit', 'add']

    def __str__(self):
        return self.orgname


# ContactTeam is used for other kinds of contact


class ContactReason(Model):
    """Reasons for making contact with the team"""
    name = models.CharField(max_length=255, verbose_name=u"Raison du contact")

    def __str__(self):
        return self.name


class ContactTeam(Model):
    """A submitted contact form"""
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255, verbose_name=u"Sujet de l'email")
    contact_reason = models.ForeignKey(ContactReason, verbose_name=u"Raison du contact", null=True,
                                       on_delete=models.SET_NULL)
    content = models.TextField(verbose_name=u"Contenu de l'email")
    contact_email = models.EmailField(max_length=100, verbose_name=u"Adresse email du contact")

    class Meta:
        serializer_fields = ['@id', 'created_at','subject','contact_reason', 'content', 'contact_email']
        # nested_fields=['contact_reason']
        anonymous_perms = ['view', 'add']
        authenticated_perms = ['inherit', 'add']

    def __str__(self):
        return self.subject


# TODO: this model is a workaround to https://git.happy-dev.fr/startinblox/solid-spec/issues/14
# it allows us to have permissions specifically for the email field
class TextSupporters_Email(Model):
    """Email of supports that signed the txt in an action group"""
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=u"Supporter email")

    class Meta:
        serializer_fields = ['email']
        anonymous_perms = ['add', 'view']

    def __str__(self):
        return self.email


class TextSupporters(Model):
    """Allow citizens to sign a text that is in an action group"""
    created_at = models.DateTimeField(auto_now_add=True)
    supporterFirstname = models.CharField(max_length=100, verbose_name=u"Prénom")
    supporterLastname = models.CharField(max_length=100, verbose_name=u"Nom")
    supporterCollectif = models.CharField(max_length=100,blank=True,null=True, verbose_name=u"Organisation")
    supportedGroup = models.ForeignKey(ActionGroup, related_name="supportedGroup", on_delete=models.CASCADE)
    #supported_email = models.ForeignKey(TextSupporters_Email, related_name="supported_email", blank=True, null=True)
    class Meta:
        serializer_fields = ['@id','supportedGroup','supporterFirstname','supporterLastname','supporterCollectif']
        nested_fields=['supportedGroup',]
        anonymous_perms = ['add','view']
        authenticated_perms = ['inherit', 'add']
        ordering=['-created_at']

    def __str__(self):
        return self.supporterFirstname + " " + self.supporterLastname



class Newsletter(Model):
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, verbose_name=u"First name")
    lastname = models.CharField(max_length=100, verbose_name=u"Last name")
    userEmail = models.EmailField(max_length=200, verbose_name=u"Email du citoyen.ne")
    subscriptionType = models.TextField(verbose_name=u"Type de souscription",blank=True,null=True)

    class Meta:
        serializer_fields = ['@id','subscriptionType','firstname','userEmail','lastname']
        anonymous_perms = ['add']
        authenticated_perms = ['inherit','add']
        ordering = ['-created_at']

    def __str__(self):
        return self.firstname + " " + self.lastname


class InformNewsletterOption(Model):
    name = models.CharField(max_length=255, verbose_name=u"Subscription to the newsletter")

    def __str__(self):
        return self.name
                                                                                                       



class HomePageElectedOfficals(Model):
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, verbose_name=u"First name")
    lastname = models.CharField(max_length=100, verbose_name=u"Last name")
    userEmail = models.EmailField(max_length=200, verbose_name=u"Email du citoyen.ne")
    emailSubject = models.CharField(max_length=255, verbose_name=u"Sujet")
    emailContent =   models.TextField(verbose_name=u"Contenu de l'email")
    electedEmails = models.TextField(verbose_name=u"Emails des élues")
    newsLetterSignUp = models.ForeignKey(InformNewsletterOption, null=True, on_delete=models.SET_NULL)

    class Meta:
        serializer_fields = ['@id','newsLetterSignUp','firstname','electedEmails','emailContent','emailSubject','userEmail','lastname']
        anonymous_perms = ['add','view']
        authenticated_perms = ['inherit','add']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class ContactEO(Model):
    """Enable citizens to send a personalized email on the base of an offered text within an action group"""
    created_at = models.DateTimeField(auto_now_add=True)
    # user info
    citizen_firstname = models.CharField(max_length=255, verbose_name=u"Prénom")
    citizen_lastname = models.CharField(max_length=255, verbose_name=u"Nom")
    # linked data
    related_action = models.ForeignKey(ActionGroup, related_name='related_text', blank=True, null=True, on_delete=models.SET_NULL)
    targeted_official = models.ManyToManyField(Representative, related_name='linked_official')
    # email content
    email_subject = models.CharField(max_length=255, verbose_name=u"Sujet")
    email_content = models.TextField(verbose_name=u"Contenu de l'email")
    email_citizen = models.EmailField(max_length=200, verbose_name=u"Email du citoyen.ne")
    # for security email is it's own model with own permissions
    # citizen_email = models.ManyToManyField(ContactEO_Email, related_name='citizen_email')
    # Can't fetch Citizens manytomany on email send// https://git.happy-dev.fr/startinblox/applications/risefor-lobbying/issues/389
    elected_email = models.TextField(max_length=400, verbose_name=u"Contacted elected official ")

    class Meta:
        serializer_fields = ['@id', 'email_subject', 'email_content', 'targeted_official', 'related_action',
                             'citizen_lastname', 'email_citizen', 'elected_email', 'citizen_firstname']
        nested_fields = []
        anonymous_perms = ['view', 'add']
        authenticated_perms = ['inherit', 'add', 'view']
        owner_perms = ['inherit', 'change', 'control']

    def __str__(self):
        return self.citizen_firstname + " " + self.citizen_lastname


#Email des Signataire de l'appel en Home Page <-- Modèle dédié pour p    rotéger les données
class CitizenSupportEmail(Model):
  email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=u"Supporter email")
  class Meta:
    serializer_fields = ['email']
    nested_fields = ['signataireEmail']
    authenticated_perms = ['inherit', 'add']
    anonymous_perms = ['add']

    """Anoted below because creates error when trying to access  
    citizensupport model in admin
    
    def __str__(self):
    return self.email
      """


"""Citizens available to come help the inhabitants when needed"""
class CitizenSupport(Model):
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=255, verbose_name=u"Prénom") 
    lastname = models.CharField(max_length=255, verbose_name=u"Nom")     
    #slug = models.SlugField(blank=True, null=True, unique=True)
    signataireEmail = models.ForeignKey(CitizenSupportEmail, related_name="signataireEmail", blank=True, null=True,
                                        on_delete=models.SET_NULL)
    #contact info taken via profile or allow anyone to signup?

    class Meta:
        serializer_fields = ['@id','signataireEmail','firstname','lastname']
        anonymous_perms = ['view',"add"]
        authenticated_perms = ['inherit', 'add']
        ordering=['-created_at']

        def __str__(self):
            return self.name

@receiver(post_save, sender=ActionGroup)
def save_autojoin_actiongroup(sender, instance, created, **kwargs):
    if created and instance.author is not None:
        instance.members.add(instance.author)


@receiver(post_save, sender=Organisation)
def save_autojoin_organisation(sender, instance, created, **kwargs):
    if created and instance.author is not None:
        instance.members.add(instance.author)


@receiver(pre_save, sender=ActionGroup)
def actiongroup_generate_slug(sender, instance, **kwargs):
    instance.slug = default_slug = slugify(instance.name)[:40]
    for index in itertools.count(1):
        if not ActionGroup.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = "{}-{}".format(default_slug, index)


@receiver(pre_save, sender=Organisation)
def organisation_generate_slug(sender, instance, **kwargs):
    instance.slug = default_slug = slugify(instance.name)[:40]
    for index in itertools.count(1):
        if not Organisation.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = "{}-{}".format(default_slug, index)


@receiver(pre_save, sender=Representative)
def representative_generate_slug(sender, instance, **kwargs):
    instance.slug = default_slug = slugify("{} {}".format(instance.firstname, instance.lastname))[:40]
    for index in itertools.count(1):
        if not Representative.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = "{}-{}".format(default_slug, index)


@receiver(post_save, sender=ContactEO)
def send_email_on_contacteo(sender, instance, created, **kwargs):
    if created:
        teamEmail = "community@risefor.org"
        body = {
        'Sujet ': instance.email_subject, 
        'Message  ': instance.email_content,
        'De la part de ': instance.citizen_firstname + " " + instance.citizen_lastname,
        
         }
        content = {"%s: %s" % (key, value) for (key, value) in body.items()}
        # turn those strings into 1 block of text separated by newlines
        content = "\n".join(content)
        email = EmailMessage(
        instance.email_subject,
        content, 
        from_email=[instance.email_citizen],
        to=[instance.elected_email],
        cc=[instance.email_citizen,teamEmail],
        reply_to=[instance.email_citizen,teamEmail],
        )
        email.send()


@receiver(post_save, sender=HomePageElectedOfficals)
def send_email_on_HomePageElectedOfficals(sender, instance, created, **kwargs):
    if created:
        #teamEmail = "test@test.com"
        key = [' ','De la part ']
        body = {
            key[0] : instance.emailContent,
            key[1] : instance.firstname + " " + instance.lastname,
        }
        content = {"%s : %s" % (key, value) for (key, value) in body.items()}
        # turn those strings into 1 block of text separated by newlines
        content = "\n".join(content)
        content =content.strip(key[0] + " :")
        email = EmailMessage(
            instance.emailSubject + " " + instance.firstname + " "+ instance.lastname,
            content,
            instance.userEmail,#here is from value
            to=[instance.electedEmails],
            cc=[instance.userEmail],
            reply_to=[instance.userEmail],
            #from=[instance.userEmail],
        )
        #email.attach_file('./static/img/ATTESTATION-DE-SORTIE-DE-CRISE-DÉROGATOIRE.pdf')
        email.send()



@receiver(post_save, sender=ContactTeam)
def send_email_on_contactteam(sender, instance, created, **kwargs):
    if created:
        body = {
            'subject': instance.subject,
            'contact_reason': instance.contact_reason,
            'content': instance.content,
            'contact_email': instance.contact_email,
        }
        content = {"%s: %s" % (key, value) for (key, value) in body.items()}
        # turn those strings into 1 block of text separated by newlines
        content = "\n".join(content)
        email = EmailMessage(
            "Nouveau Contact " + instance.subject,
            content,
            to=['community@united4earth.org']
        )
        email.send()


@receiver(post_save, sender=HelpInstall)
def send_email_on_contact(sender, instance, created, **kwargs):
    if created:
        body = {
            'Nom de organisation': instance.orgname,
            'Type organisation': instance.orgType,
            'Niveau aide nécessaire': instance.helpLevel,
            'Utilisation de outil': instance.usage_tool,
            'Commentaire': instance.extra_msg,
            'Email de contact': instance.contact_email,

        }
        content = {"%s: %s" % (key, value) for (key, value) in body.items()}
        # turn those strings into 1 block of text separated by newlines
        content = "\n".join(content)
        email = EmailMessage(
            "Demande d'aide par " + instance.orgname,
            content,
            to=['community@united4earth.org']
        )
        email.send()

