from django.contrib import admin

# Register your models here.
#!/usr/bin/env python3
# encoding: utf-8


# Register your models here.

from .models import FiatCurrency, M_o_d_e_l_C_o_m_p_o_n_e_n_t

@admin.register(FiatCurrency)
class FiatCurrencyAdmin(admin.ModelAdmin):
    # order-view the 100 > 98 so decreasing
    # need to see active before
    ordering = ["-active", "-order_view", "-update"]

@admin.register(M_o_d_e_l_C_o_m_p_o_n_e_n_t)
class M_o_d_e_l_C_o_m_p_o_n_e_n_tAdmin(admin.ModelAdmin):
    ordering = ["-active", "-order_view", "-update"]

