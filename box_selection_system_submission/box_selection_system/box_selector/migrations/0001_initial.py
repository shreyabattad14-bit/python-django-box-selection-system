from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('length_cm', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('width_cm', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('height_cm', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('weight_kg', models.DecimalField(decimal_places=3, max_digits=8, validators=[django.core.validators.MinValueValidator(0.001)])),
            ],
        ),
        migrations.CreateModel(
            name='ShippingBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('inner_length_cm', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('inner_width_cm', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('inner_height_cm', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('max_weight_kg', models.DecimalField(decimal_places=3, max_digits=8, validators=[django.core.validators.MinValueValidator(0.001)])),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(name='Order', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name='OrderItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('quantity', models.PositiveIntegerField(default=1)),
            ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='box_selector.order')),
            ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='box_selector.product')),
        ]),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(condition=models.Q(('quantity__gte', 1)), name='positive_order_quantity'),
        ),
    ]
