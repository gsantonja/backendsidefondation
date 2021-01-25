# Generated by Django 3.1.2 on 2021-01-20 10:19

import a_p_p_l_i_c_a_t_i_o_n_N_a_m_e.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FiatCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(default='€', max_length=5, unique=True)),
                ('nameShort', models.CharField(default='EUR', max_length=5, unique=True)),
                ('nameLong', models.CharField(blank=True, default='Euro', max_length=20, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('default', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('update', models.DateTimeField(default=django.utils.timezone.now)),
                ('create', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_view', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='M_o_d_e_l_C_o_m_p_o_n_e_n_t',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('value', models.FloatField(default=0.0)),
                ('active', models.BooleanField(default=True)),
                ('order_view', models.IntegerField(default=0)),
                ('update', models.DateTimeField(default=django.utils.timezone.now)),
                ('create', models.DateTimeField(default=django.utils.timezone.now)),
                ('currentCurrency', models.ForeignKey(blank=True, default=a_p_p_l_i_c_a_t_i_o_n_N_a_m_e.models.getDefaultCurrency, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='M_o_d_e_l_s_k_e_l_e_t_o_n_fiatcurrency', to='a_p_p_l_i_c_a_t_i_o_n_N_a_m_e.fiatcurrency')),
            ],
        ),
    ]