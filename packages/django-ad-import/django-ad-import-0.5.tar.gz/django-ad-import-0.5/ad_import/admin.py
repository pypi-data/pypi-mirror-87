from django.contrib import admin

# Register your models here.
from ad_import.models import User, Directory, Query, Server, Workstation


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ['dc', 'dn']


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'directory', 'query', 'base_dn', 'type', 'target']
    list_filter = ['directory', 'type', 'target']
    save_as = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['directory', 'displayName', 'givenName', 'sn', 'sAMAccountName', 'lastLogon', 'last_update']
    list_filter = ['directory']
    readonly_fields = ['last_update']


class ComputerAdmin(admin.ModelAdmin):
    list_display = ['directory', 'cn', 'operatingSystem']
    list_filter = ['directory', 'operatingSystem', 'operatingSystemVersion']


@admin.register(Server)
class ServerAdmin(ComputerAdmin):
    pass


@admin.register(Workstation)
class WorkstationAdmin(ComputerAdmin):
    pass
