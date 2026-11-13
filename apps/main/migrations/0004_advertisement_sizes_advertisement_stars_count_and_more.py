import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_remove_advertisementcharacteristic_brend_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='sizes',
            field=models.CharField(default='M/L/X/XL', max_length=100, verbose_name='Размеры'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='stars_count',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1),
                                                             django.core.validators.MaxValueValidator(5)],
                                      verbose_name='Количество звезд (от 1 до 5)'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, max_length=10),
        ),
    ]
