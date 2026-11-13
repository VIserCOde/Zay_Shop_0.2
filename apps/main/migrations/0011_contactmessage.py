from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0010_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема обращения')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
            ],
            options={
                'verbose_name': 'Сообщение из контактов',
                'verbose_name_plural': 'Сообщения из контактов',
                'ordering': ['-created_at'],
            },
        ),
    ]
