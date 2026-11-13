from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0007_advertisement_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
    ]
