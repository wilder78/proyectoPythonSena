from django.db import models
from django.utils import timezone


# ========================/ Base models for watches. /========================= #
class Watch(models.Model):
    brand = models.CharField(max_length=100)
    type_of_machinery = models.CharField(max_length=50)
    model = models.CharField(max_length=100)

    class Meta:
        abstract = True  # Modelo abstracto para evitar crear tabla en la BD

    def general_maintenance(self):
        return f"Mantenimiento general realizado en el reloj {self.brand} {self.model} ({self.type_of_machinery})."

    def get_information(self):
        return f"{self.brand} {self.model} - Tipo: {self.type_of_machinery}"

    def __str__(self):
        return self.get_information()


# ===========================/ Clases hijas de Watch /=========================== #
class MechanicalWatch(Watch):
    WINDING_CHOICES = [("manual", "Manual"), ("automatic", "Automático")]
    winding_type = models.CharField(max_length=10, choices=WINDING_CHOICES, default="manual")

    def general_maintenance(self):
        return f"Se ha realizado calibración ({self.winding_type}), limpieza y lubricación en el reloj {self.brand} {self.model} ({self.type_of_machinery})."


class QuartzWatch(Watch):
    battery_life = models.IntegerField(default=2)  # Vida útil de la batería en años.

    def general_maintenance(self):
        return f"Se ha realizado limpieza y cambio de batería en el reloj {self.brand} {self.model} ({self.type_of_machinery})."


class SmartWatch(Watch):
    os = models.CharField(max_length=50, default="Desconocido")  # Sistema operativo
    connectivity = models.CharField(max_length=100, default="No especificado")  # Tipos de conectividad

    def general_maintenance(self):
        return f"Se ha realizado actualización de software y revisión de sensores en el reloj {self.brand} {self.model} ({self.type_of_machinery})."

    class Meta:
        verbose_name = "Reloj Inteligente"
        verbose_name_plural = "Relojes Inteligentes"


# ========================/ Base models for person. /========================= #
class Person(models.Model):
    name = models.CharField(max_length=100)
    identification = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - ID: {self.identification} - Tel: {self.phone}"


# ===========================/ Clases hijas de Person /=========================== #
class Customer(Person):
    email = models.EmailField(unique=True)


class Employee(Person):
    post = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)


class Supplier(Person):
    company = models.CharField(max_length=100)
    products = models.TextField()


# ========================/ Modelo de Servicios corregido /========================= #
class Service(models.Model):
    WATCH_CHOICES = [
        ("MechanicalWatch", "Reloj Mecánico"),
        ("QuartzWatch", "Reloj de Cuarzo"),
        ("SmartWatch", "Reloj Inteligente"),
    ]
    
    watch_type = models.CharField(max_length=20, choices=WATCH_CHOICES)
    mechanical_watch = models.ForeignKey(MechanicalWatch, on_delete=models.SET_NULL, null=True, blank=True)
    quartz_watch = models.ForeignKey(QuartzWatch, on_delete=models.SET_NULL, null=True, blank=True)
    smart_watch = models.ForeignKey(SmartWatch, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Pendiente")
    observations = models.TextField(blank=True, null=True)
    parts_used = models.TextField(blank=True, null=True)
    received_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def complete_service(self):
        self.status = "Terminado"
        self.delivery_date = timezone.localdate()
        self.save()

    def __str__(self):
        return f"Servicio: {self.service_type} - Estado: {self.status} - Cliente: {self.customer.name}"




# class Watch(models.Model):
#     _Brand = models.CharField(max_length=100)
#     _Type_of_machinary = models.CharField(max_length=50)
#     _Model = models.CharField(max_length=100)

#     class Meta:
#         abstract = True

#     @property
#     def brand(self):
#         return self._Brand
    
#     @property
#     def type_of_machinary(self):
#         return self._Type_of_machinary
    
#     @property
#     def model(self):
#         return self._Model
    
#     def generalMaintenance(self):
#         """ Método pilimórfico para realizar mantenimiento en los relojes."""
#         return "Mantenimiento general realizado."
    
#     def getInformation(self):
#         """ Metodo para obtener informacion basica del reloj. """
#         return f"{self.brand} {self.model} {self.type_of_machinary}"
    
#     def __str__(self):
#         return self.getInformation()

# class QuartzWatch(Watch):
#     battery_life = models.IntegerField(default=2)  # Vida útil de la batería en años.

#     def battery_verification(self):
#         """ Método específico para verificar el estado de la batería. """
#         return f"La batería del reloj {self.brand} {self.model} tiene una duración estimada de {self.battery_life} años."

#     def general_maintenance(self):
#         """ Mantenimiento específico para relojes de cuarzo. """
#         return f"Se ha realizado limpieza y cambio de batería en el reloj {self.brand} {self.model} ({self.type_of_machinery})."
