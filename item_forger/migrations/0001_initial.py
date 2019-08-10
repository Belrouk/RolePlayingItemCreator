# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-03 06:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('note', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RPItem',
            fields=[
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('campaign', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('rarity', models.IntegerField(blank=True, choices=[(10, 'Mundane'), (20, 'Common'), (30, 'Uncommon'), (40, 'Rare'), (50, 'Very Rare'), (60, 'Legendary'), (70, 'Artifact')], default=10, null=True, verbose_name='Item Rarity')),
                ('attunement', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Special', 'Special')], default='Yes', max_length=10, null=True, verbose_name='Requires Attunemnet')),
                ('type', models.IntegerField(blank=True, choices=[(10, 'Armor'), (20, 'Potion'), (30, 'Ring'), (40, 'Amulet'), (50, 'Rod'), (60, 'Scroll'), (70, 'Staff'), (80, 'Wand'), (90, 'Weapon'), (100, 'Wonderous Item'), (110, 'Trinket')], default=None, null=True, verbose_name='Item type')),
                ('value', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('description', models.TextField()),
                ('benefits', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='notes',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='item_forger.RPItem'),
        ),
    ]
