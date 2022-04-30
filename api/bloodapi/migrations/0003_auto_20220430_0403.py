# Generated by Django 3.2.13 on 2022-04-29 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bloodapi', '0002_alter_profile_last_blood_donated'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='reward_point',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='BloodRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodapi.profile')),
            ],
        ),
    ]
