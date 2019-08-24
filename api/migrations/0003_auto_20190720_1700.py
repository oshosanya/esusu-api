# Generated by Django 2.2.3 on 2019-07-20 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20190718_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingsgroup',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='savingsgroupmember',
            name='amount_saved',
            field=models.FloatField(null=True),
        ),
        migrations.CreateModel(
            name='SavingsGroupInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('savings_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SavingsGroup')),
            ],
        ),
    ]
