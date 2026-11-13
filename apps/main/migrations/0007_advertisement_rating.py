from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='rating',
            field=models.FloatField(default=5.0, verbose_name='Рейтинг'),
        ),
    ]
