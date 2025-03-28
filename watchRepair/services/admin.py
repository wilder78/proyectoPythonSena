from django.contrib import admin
from .models import MechanicalWatch, QuartzWatch, SmartWatch, Customer, Employee, Supplier, Service


@admin.register(MechanicalWatch)
class MechanicalWatchAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "type_of_machinery", "winding_type")
    search_fields = ("brand", "model")

@admin.register(QuartzWatch)
class QuartzWatchAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "type_of_machinery", "battery_life")
    search_fields = ("brand", "model")

@admin.register(SmartWatch)
class SmartWatchAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "type_of_machinery", "os", "connectivity")
    search_fields = ("brand", "model")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service_type", "status", "customer", "received_date", "cost")
    search_fields = ("service_type", "customer__name")
    list_filter = ("status", "received_date")
