# Generated by Django 5.0.6 on 2024-07-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobtracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('Applied', 'Applied'), ('Unsuccessful', 'Unsuccessful'), ('Interview', 'Interview'), ('Under Consideration', 'Under Consideration'), ('Offered', 'Offered'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Withdrawn', 'Withdrawn'), ('Awaiting Response', 'Awaiting Response'), ('Follow-up Required', 'Follow-up Required'), ('Hired', 'Hired'), ('Closed', 'Closed')], default='Applied', max_length=20),
        ),
    ]
