import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug (URL)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('description', models.TextField(verbose_name='Description')),
                ('color', models.CharField(blank=True, max_length=100, null=True, verbose_name='Available Colors')),
                ('brend', models.CharField(blank=True, max_length=100, null=True, verbose_name='Brand')),
                ('preview', models.ImageField(upload_to='advertisements/previews/', verbose_name='Preview Image')),
                ('subcategory',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements',
                                   to='main.subcategory', verbose_name='Sub Category')),
            ],
            options={
                'verbose_name': 'Advertisement',
                'verbose_name_plural': 'Advertisements',
            },
        ),
        migrations.CreateModel(
            name='AdvertisementCharacteristic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, verbose_name='Specification Title / Key')),
                ('color',
                 models.CharField(blank=True, max_length=100, null=True, verbose_name='Color for Specification')),
                ('brend',
                 models.CharField(blank=True, max_length=100, null=True, verbose_name='Brand for Specification')),
                ('advertisement',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics',
                                   to='main.advertisement', verbose_name='Advertisement')),
            ],
            options={
                'verbose_name': 'Advertisement Characteristic',
                'verbose_name_plural': 'Advertisement Characteristics',
            },
        ),
        migrations.CreateModel(
            name='AdvertisementImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='advertisements/gallery/', verbose_name='Gallery Image')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images',
                                                    to='main.advertisement', verbose_name='Advertisement')),
            ],
            options={
                'verbose_name': 'Advertisement Image',
                'verbose_name_plural': 'Advertisement Images',
            },
        ),
    ]
