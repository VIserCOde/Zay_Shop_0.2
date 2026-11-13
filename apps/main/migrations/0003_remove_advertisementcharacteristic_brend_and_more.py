from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_advertisement_advertisementcharacteristic_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisementcharacteristic',
            name='brend',
        ),
        migrations.RemoveField(
            model_name='advertisementcharacteristic',
            name='color',
        ),
        migrations.AddField(
            model_name='advertisementcharacteristic',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True,
                                   verbose_name='Value (e.g., 100% Cotton, 250g)'),
        ),
        migrations.AlterField(
            model_name='advertisementcharacteristic',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Property Name (e.g., Material, Weight)'),
        ),
    ]
