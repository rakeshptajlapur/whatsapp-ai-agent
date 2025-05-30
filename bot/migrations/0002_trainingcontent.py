# Generated by Django 5.0.1 on 2025-04-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content_type', models.CharField(choices=[('rules', 'Business Rules'), ('faq', 'FAQ'), ('policy', 'Policies'), ('pricing', 'Pricing'), ('service', 'Services')], max_length=20)),
                ('content', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('priority', models.IntegerField(default=0)),
                ('source_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-priority', '-updated_at'],
            },
        ),
    ]
