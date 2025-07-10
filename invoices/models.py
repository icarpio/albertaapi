from django.db import models
from django.utils import timezone

class Owner(models.Model):
    name = models.CharField(max_length=200, default="Accommodation Name")
    tax_id = models.CharField(max_length=50, default="TAXID12345678")
    address = models.CharField(max_length=200, default="Accommodation Address")
    phone = models.CharField(max_length=20, default="000-000-000")
    fist_name = models.CharField(max_length=200, default="Accommodation Name")
    vat_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=10.00)  # predefined VAT %

    def __str__(self):
        return self.name

class Guest(models.Model):
    full_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20)  
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.full_name

class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    #number_of_guests = models.IntegerField()
    unit = models.CharField(max_length=50)

    def stay_duration(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"Booking for {self.guest} from {self.check_in} to {self.check_out}"

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    receipt_date = models.DateField(default=timezone.now)
    invoice_number = models.IntegerField()
    # financial breakdown stored as JSON list of items
    breakdown = models.JSONField()

    @property
    def subtotal(self):
        # Aplica un 10% de descuento
        total_amount = sum(item['amount'] for item in self.breakdown)
        return round(total_amount / 1.10, 2)  # 90% del total

    @property
    def vat(self):
        owner = Owner.objects.first()
        if owner:
            return round(self.subtotal * 0.10, 2)
        return 0
    
    @property
    def total(self):
        return round(self.subtotal + self.vat, 2)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.booking.guest.full_name}"

