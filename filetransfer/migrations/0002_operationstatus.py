# Generated by Django 3.0.7 on 2020-06-28 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filetransfer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('operation', models.CharField(max_length=10)),
                ('objectName', models.CharField(max_length=50)),
                ('status', models.IntegerField(choices=[(1, 'progress'), (2, 'stop'), (3, 'resume'), (4, 'terminate')], default=1)),
            ],
        ),
    ]
