from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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

    def winding_verification(self):
        return f"El reloj {self.brand} {self.model} tiene un mecanismo de cuerda {self.winding_type}."

    def general_maintenance(self):
        return f"Se ha realizado calibración ({self.winding_type}), limpieza y lubricación en el reloj {self.brand} {self.model} ({self.type_of_machinery})."


class QuartzWatch(Watch):
    battery_life = models.IntegerField(default=2)  # Vida útil de la batería en años.

    def general_maintenance(self):
        return f"Se ha realizado limpieza y cambio de batería en el reloj {self.brand} {self.model} ({self.type_of_machinery})."


# ========================/ Base models for person. /========================= #
class Person(models.Model):
    name = models.CharField(max_length=100)
    identification = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def get_role_info(self):
        return f"Identidad: {self.name} - ID: {self.identification} - Teléfono: {self.phone}"

    def __str__(self):
        return self.get_role_info()


# ===========================/ Clases hijas de Person /=========================== #
class Customer(Person):
    email = models.EmailField(unique=True)

    def get_role_info(self):
        return f"Cliente: {self.name} - Email: {self.email} - Tel: {self.phone}"


class Employee(Person):
    post = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def get_role_info(self):
        return f"Empleado: {self.name} - Cargo: {self.post} - Salario: ${self.salary}"


class Supplier(Person):
    company = models.CharField(max_length=100)
    products = models.TextField()

    def get_role_info(self):
        return f"Proveedor: {self.name} - Empresa: {self.company} - Productos: {self.products}"


# ========================/ Base models for person. /========================= #
class Service(models.Model):
    watch_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    watch_id = models.PositiveBigIntegerField()
    watch = GenericForeignKey('watch_type', 'watch_id')
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

    @classmethod
    def create_pending_service(cls, watch, customer, service_type, cost=0, observations=""):
        """
        Crea un nuevo servicio con estado "Pendiente".
        """
        return cls.objects.create(
            watch_type=ContentType.objects.get_for_model(watch),
            watch_id=watch.id,
            customer=customer,
            service_type=service_type,
            cost=cost,
            observations=observations
        )




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
