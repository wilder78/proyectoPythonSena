from django.contrib import admin
from .models import MechanicalWatch, QuartzWatch, Customer, Employee, Supplier, Service

# Registrar los modelos en el panel de administración
@admin.register(MechanicalWatch)
class MechanicalWatchAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'type_of_machinery', 'winding_type')
    search_fields = ('brand', 'model')

@admin.register(QuartzWatch)
class QuartzWatchAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'type_of_machinery', 'battery_life')
    search_fields = ('brand', 'model')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'salary', 'phone')
    search_fields = ('name', 'post')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'phone')
    search_fields = ('name', 'company')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('watch', 'customer', 'service_type', 'status', 'received_date', 'delivery_date', 'cost')
    search_fields = ('service_type', 'status')
    list_filter = ('status', 'received_date')


