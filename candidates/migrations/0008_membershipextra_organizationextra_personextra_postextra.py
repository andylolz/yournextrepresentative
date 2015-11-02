# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0004_auto_20151014_1648'),
        ('popolo', '0001_initial'),
        ('candidates', '0008_migrate_to_django_popolo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.OneToOneField(related_name='extra', to='popolo.Membership')),
                ('election', models.ForeignKey(related_name='candidacies', blank=True, to='elections.Election', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('register', models.CharField(max_length=512, blank=True)),
                ('base', models.OneToOneField(related_name='extra', to='popolo.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='PersonExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.OneToOneField(related_name='extra', to='popolo.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PostExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.OneToOneField(related_name='extra', to='popolo.Post')),
            ],
        ),
    ]
