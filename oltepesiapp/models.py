from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class TeamLeader(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Team Leader"
        verbose_name_plural = "Team Leaders"

    def __str__(self):
        return f"{self.name}"

class HarvesterActivity(models.Model):
    ACTIVITY_CHOICES = [
        ("HARVESTING", "Harvesting"),
        ("PINCHING", "Pinching"),
        ("PLANTING", "Planting"),
        ("GREENHOUSE_PREP", "Greenhouse Preparations"),
        ("STAPLING_BOXES", "Stapling Boxes"),
        ("COLDSTORE", "Coldstore"),
        ("WASTE_COLLECTION", "Waste Collection"),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group} - {self.get_activity_display()}"

    @property
    def duration(self):
        return self.end_time - self.start_time
    class Meta:
        verbose_name_plural = "Harvester Activities" 