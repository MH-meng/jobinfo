# Generated by Django 2.1.5 on 2019-04-15 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('remake', models.CharField(blank=True, max_length=244, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='info.Conpanys')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='info.StudentInfo')),
            ],
        ),
    ]
