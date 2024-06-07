# Generated by Django 5.0.2 on 2024-06-07 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(help_text='IP address of host`s network interface', protocol='IPv4')),
                ('hostname', models.CharField(help_text='Hostname', max_length=20)),
                ('status', models.BooleanField(default=False, help_text='Active / Inactive')),
                ('system', models.CharField(help_text='Name & version of host`s OS', max_length=50)),
                ('measures', models.TextField(help_text='Collect measures of host`s params')),
            ],
        ),
    ]
