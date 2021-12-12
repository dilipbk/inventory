from django.contrib import admin
from .models import Stock,Purchase,Purchase_items,Sales,Addbusiness,Usermanage,Return,Imagetry,Salesbill,Sales_items
# Register your models here.
admin.site.register(Stock)
admin.site.register(Purchase)
admin.site.register(Purchase_items)
admin.site.register(Sales)
admin.site.register(Addbusiness)
admin.site.register(Usermanage)
admin.site.register(Return)
admin.site.register(Imagetry)
admin.site.register(Sales_items)
admin.site.register(Salesbill)