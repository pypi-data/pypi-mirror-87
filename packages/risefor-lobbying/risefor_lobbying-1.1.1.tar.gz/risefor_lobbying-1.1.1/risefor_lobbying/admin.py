from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Representative, Phone


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class RepresentativeAdmin(GuardedModelAdmin):
    inlines = [ PhoneInline, ]


admin.site.register(Representative, RepresentativeAdmin)
