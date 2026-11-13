import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя автора')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.PositiveIntegerField(default=5, verbose_name='Оценка (1-5)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('advertisement',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                   to='main.advertisement', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Отзыв покупателя',
                'verbose_name_plural': 'Отзывы покупателей',
            },
        ),
    ]
