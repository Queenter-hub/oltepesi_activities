from django.http import HttpResponse
import csv
from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup
from django.utils.timezone import localtime
from .models import Group, TeamLeader, HarvesterActivity
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

class DateRangeFilter(SimpleListFilter):
    title = _("Date Range")
    parameter_name = "start_time__range"
    template = "admin/date_range_filter.html"

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_time__date__lte=end_date)

        return queryset

admin.site.site_header = "Oltepesi Admin"

admin.site.unregister(AuthGroup)

admin.site.register(Group)
admin.site.register(TeamLeader)

def download_selected_activities(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="harvester_activities.csv"'

    writer = csv.writer(response)

    # Header row
    writer.writerow([
        'Date',
        'Group',
        'Team Leader',
        'Activity',
        'Start Time',
        'End Time',
        'Duration',
    ])

    # Data rows
    for obj in queryset:
        start = localtime(obj.start_time)
        end = localtime(obj.end_time)
        created_date = start.date()

        writer.writerow([
            created_date,
            obj.group.name,
            obj.team_leader.name,
            obj.get_activity_display(),
            start.strftime('%H:%M'),
            end.strftime('%H:%M'),
            str(obj.duration),
        ])

    return response


download_selected_activities.short_description = "Download selected activities"


@admin.register(HarvesterActivity)
class HarvesterActivityAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'team_leader',
        'activity',
        'start_time',
        'end_time',
        'created_at',
    )

    list_filter = (
        DateRangeFilter,
        'activity',
        'group',
    )

    ordering = ('-start_time',)

    actions = [download_selected_activities]