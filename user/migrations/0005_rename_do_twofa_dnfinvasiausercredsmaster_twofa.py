# Generated by Django 3.2.12 on 2023-10-04 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20231004_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dnfinvasiausercredsmaster',
            old_name='do_twofa',
            new_name='twoFA',
        ),
    ]
