# oltepesiapp/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse  
from .forms import HarvesterActivityForm
from .models import HarvesterActivity
from django.utils.timezone import localtime
import csv

# View to add a harvester activity via form
def add_harvester_activity(request):
    if request.method == 'POST':
        form = HarvesterActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activity_success')
    else:
        form = HarvesterActivityForm()
    
    return render(request, 'oltepesiapp/add_activity.html', {'form': form})

# Simple success page after adding activity
def activity_success(request):
    return HttpResponse("Activity added successfully!")

# View to download all activities as CSV
def download_activities_csv(request):
    # Create the HttpResponse object with CSV headers
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="activities.csv"'},
    )

    writer = csv.writer(response)
    # Write header row
    writer.writerow(['Date', 'Group', 'Team Leader', 'Activity', 'Start Time', 'End Time', 'Duration'])

    # Get all activities ordered by start_time
    activities = HarvesterActivity.objects.all().order_by('start_time')

    for act in activities:
        start = localtime(act.start_time)
        end = localtime(act.end_time)
        duration = act.duration

        writer.writerow([
            start.date(),
            act.group.name,
            act.team_leader.name,
            act.get_activity_display(),
            start.strftime('%H:%M'),
            end.strftime('%H:%M'),
            str(duration)
        ])

    return response