from django.db import models
from django.db.models.expressions import OrderBy
from django.db.models.fields import CharField
from django.contrib.auth.models import User
# Create your models here.
class Stock(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    Product_name=models.CharField(max_length=255)
    Cost_Price=models.DecimalField(max_digits=100,decimal_places=2)
    Selling_Price=models.DecimalField(max_digits=100,decimal_places=2)
    Suppliers=models.CharField(max_length=300)
    Tax_method=models.CharField(max_length=255)
    Quantity=models.DecimalField(max_digits=100,decimal_places=2)
    Quantity_left=models.DecimalField(max_digits=100,decimal_places=2)
    Quantity_sold=models.DecimalField(max_digits=100,decimal_places=2)
    Summary=models.TextField()

    def __str__(self):
        return f"{self.Product_name}           User ={self.user}"
    class Meta:
        ordering=('Product_name',)

class Addbusiness(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Business_name=models.CharField(max_length=1000)
    Business_email=models.EmailField()
    Business_Address=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.Business_name}           User ={self.user}"
    class Meta:
        ordering=('Business_name',)

class Usermanage(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    Firstname=models.CharField(max_length=255)
    Lastname=models.CharField(max_length=255)
    Username=models.CharField(max_length=255)
    City=models.CharField(max_length=255)
    Gender=models.CharField(max_length=255)
    DOB=models.CharField(max_length=255)
    Marital_status=models.CharField(max_length=255)
    Age=models.CharField(max_length=255)
    Country=models.CharField(max_length=255)
    State=models.CharField(max_length=255)
    Address=models.TextField(max_length=255)

    def __str__(self):
        return f"{self.Username}           User ={self.user}"
    class Meta:
        ordering=("Username",)





class Purchase(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Date=models.CharField(max_length=255)
    Purchase_number=models.CharField(max_length=255)
    Supplier=models.CharField(max_length=255)
    Vat=models.IntegerField()
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Shipping=models.CharField(max_length=255)
    Payment=models.DecimalField(max_digits=100,decimal_places=2)
    Purchase_note=models.TextField()
    def __str__(self):
        return f"{self.Supplier}           User ={self.user}"
    class Meta:
        ordering=('-Date',)

class Purchase_items(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Date=models.CharField(max_length=255)
    Purchase_number=models.CharField(max_length=255)
    Supplier=models.CharField(max_length=255)
    Product_name=models.CharField(max_length=255)
    Quantity=models.DecimalField(max_digits=100,decimal_places=2)
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)

    def __str__(self):
        return f"{self.Supplier}           User ={self.user}"
    class Meta:
        ordering=('-Date',)

class Sales(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Date=models.CharField(max_length=255)
    Product=models.CharField(max_length=255)
    Customer=models.CharField(max_length=255)
    Quantity=models.DecimalField(max_digits=100,decimal_places=2)
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Vat=models.DecimalField(max_digits=100,decimal_places=2)
    Paid=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    Payment_status=models.CharField(max_length=255)
    Sales_note=models.TextField()

    def __str__(self):
        return f"{self.Customer}           User ={self.user}"
    class Meta:
        ordering=('-Date',)


class Return(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Date=models.CharField(max_length=255)
    Product=models.CharField(max_length=255)
    Customer=models.CharField(max_length=255)
    Quantity=models.DecimalField(max_digits=100,decimal_places=2)
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Vat=models.DecimalField(max_digits=100,decimal_places=2)
    Paid=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    Payment_status=models.CharField(max_length=255)
    Return_note=models.TextField()

    def __str__(self):
        return f"{self.Customer}           User ={self.user}"
    class Meta:
        ordering=('-Date',)


class Imagetry(models.Model):
    img=models.ImageField(upload_to="uploads/")

class Sales_items(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Date=models.CharField(max_length=255)
    Purchase_number=models.CharField(max_length=255)
    Supplier=models.CharField(max_length=255)
    Product_name=models.CharField(max_length=255)
    Quantity=models.DecimalField(max_digits=100,decimal_places=2)
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    net_total=models.DecimalField(max_digits=100,decimal_places=2)
    def __str__(self):
        return f"{self.Supplier}           User ={self.user}"
    class Meta:
        ordering=('-Date',)


class Salesbill(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)

    Date=models.CharField(max_length=255)
    Purchase_number=models.CharField(max_length=255)
    Supplier=models.CharField(max_length=255)
    Vat=models.IntegerField()
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Shipping=models.CharField(max_length=255)
    Payment=models.DecimalField(max_digits=100,decimal_places=2)
    Purchase_note=models.TextField()
    def __str__(self):
        return f"{self.Supplier}           User ={self.user}"
    class Meta:
        ordering=('-Date',)