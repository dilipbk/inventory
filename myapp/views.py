from django.contrib.auth import authenticate
from django.core.checks import messages
from django.db.models.fields import TextField
from django.db.models.query_utils import Q
from django.http import request
from django.shortcuts import redirect, render
from .models import Imagetry, Purchase_items,Sales,Salesbill,Usermanage,Sales_items,Return, Stock,Purchase,Purchase_items,Addbusiness

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
# datetime object containing current date and time

# Create your views here.
def nav(request):
    obj=Addbusiness.objects.filter(user=request.user,)
    for data in obj:
        business=data.Business_name
    return render('navigation-bar.html',{'business':business})
def logins(request):
    message1=""
    if request.method=='POST':
        username=request.POST['username']
        pw=request.POST['pw']
        user=authenticate(request,username=username,password=pw)
        if user is None:
            message1="Invalid Credentials"
        else:
            login(request,user)
            return redirect('index')
    return render(request,'login.html',{"message":message1})
@login_required
def index(request):
    #for total sale
    total_salee=0.0
    total_saleee=0.0
    try:
        obj_sales=Sales.objects.filter(user=request.user)
        for data in obj_sales:
            total_salee=round(total_salee+float(data.Total),2)
    except:
        total_salee=0.0
    try:
        obj_tot_sales=Sales_items.objects.filter(user=request.user)
        for data in obj_tot_sales:
            total_saleee=round(total_saleee+float(data.net_total),2)
    except:
        total_saleee=0.0
    finally:
        total_sale=total_salee+total_saleee
    
    #for total-purchase:
    total_purchase=0.0
    obj_purchase=Purchase_items.objects.filter(user=request.user)
    for data in obj_purchase:
        total_purchase=round(total_purchase+float(data.Total))
    #sales percent
    try:
        sales_percent=float((total_sale/total_purchase))*100
    except ZeroDivisionError:
        sales_percent=0
    #purchase-percent:
    purchase_percant=100-sales_percent

    #for sold ittems:
    obj_stock=Stock.objects.filter(user=request.user)
    Quantity=0.0
    Quantity_left=0.0
    stock=0.0
    for data in obj_stock:
        stock=round(stock+float(data.Quantity),2)
        Quantity_left=round(Quantity_left+float(data.Quantity_left),2)
        Quantity=round(Quantity+float(data.Quantity),2)
    sold_products=Quantity-Quantity_left
    rem_items=Quantity-sold_products
    #percantage calculation:
    try:
        sold_percent=round(float(sold_products/Quantity)*100,2)
    except ZeroDivisionError:
        sold_percent=0

    #for credit 
    obj_credit=Sales.objects.filter(Payment_status="Due",user=request.user)
    total_credit=0.0
    for data in obj_credit:
        total_credit=round(total_credit+float(data.Total)-float(data.Paid),2)

    #for credit percentage:
    try:
        credit_percent=float(total_credit/total_sale)*100
    except ZeroDivisionError:
        credit_percent=0

    #for items return
    obj_return=Return.objects.filter(user=request.user)
    return_item=0
    for data in obj_return:
        return_item=round(return_item+float(data.Quantity),2)
    #percentage for return items:
    try:
        return_percent=round(float(return_item/sold_products)*100,2)
    except ZeroDivisionError:
        return_percent=0
    #for profit calcuation....
    profit=stock
    #for sending object
    object_stock=Sales.objects.filter(user=request.user).order_by('-Date')
    #for best time all product
    obj_stock=Stock.objects.filter(user=request.user).order_by('-Quantity_sold')[:2]
    
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name

    object=Usermanage.objects.filter(user=request.user)
    for data in object:
        username=data.Username
    #for images

    context={'total':total_sale,
    'purchase':total_purchase,'username':username,'spercent':sales_percent,'ppercent':purchase_percant,'soldproduct':sold_products
    ,'sold_percent':sold_percent,'return_percent':return_percent,
    'total_credit':total_credit,
    'credit_percent':credit_percent,'rem_items':rem_items,'business':business,'return_item':return_item,'profit':profit,'object':object_stock,'objects':obj_stock}


    return render(request,'index2.html',context)
@login_required
def addproduct(request):
    if request.method=="POST":
        product=request.POST['product']
        cp=request.POST['cp']
        sp=request.POST['cp']
        tax=request.POST['type']
        suppliers=request.POST['suppliers']
        quantity=request.POST['quantity']
        summary=request.POST['des']
        obj=Stock.objects.filter(Product_name=product)
        if len(obj)==0:
            sold=int(quantity)
            objec=Stock.objects.create(user=request.user,Quantity_sold=0.0,Product_name=product,Cost_Price=cp,Selling_Price=sp,Quantity_left=quantity,Suppliers=suppliers,Tax_method=tax,Quantity=quantity,Summary=summary)
            objec.save()
        else:
            
            for data in obj:
                left_quantity=float(quantity)+float(data.Quantity_left)

                quantity=float(quantity)+float(data.Quantity)
                
            obj.update(Cost_Price=cp,Selling_Price=sp,Suppliers=suppliers,Tax_method=tax,Quantity=quantity,Quantity_left=left_quantity,Summary=summary)

       
    object=Stock.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'pageadd-product.html',{'obj':object,'username':username,'business':business})

@login_required
def productlist(request):

    objec=Stock.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-list-product.html',{'object':objec,'business':business,'username':username})

@login_required
def returnsalepage(request,idd):
    object=Sales.objects.filter(id=idd,user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-edit-return.html',{'object':object,'id':idd,'username':username,'business':business})

@login_required
def addsale(request):
    message1=""
    message2=""
    if request.method=='POST':
        Date=request.POST['date']
        Product=request.POST['product']
        Customer=request.POST['customer']
        Quantity=request.POST['quantity']
        Rate=request.POST['rate']
        Discount=request.POST['discount']
        Vat=request.POST['vat']
        Paid=request.POST['paid']
        Total=request.POST['total']
        Payment_status=request.POST['payment_status']
        Sales_note=request.POST['salesnote']
        obj=Stock.objects.filter(Product_name=Product,user=request.user)
        if len(obj)==0:
            message1="Stock Not Found"
        else:
            for data in obj:
                obj=Stock.objects.filter(Product_name=Product,user=request.user)
                for data in obj:
                
                    Quantity_left_=float(data.Quantity_left)-float(Quantity)
                    sold=float(data.Quantity_sold)+float(Quantity)
                if Quantity_left_<0:
                    message2="Out of stock."
                else:
                    object=Sales.objects.create(user=request.user,Date=Date,Product=Product,Customer=Customer,Quantity=Quantity,Rate=Rate,Discount=Discount,Vat=Vat,Paid=Paid,Total=Total,Payment_status=Payment_status,Sales_note=Sales_note)
                    object.save()
                    obj.update(Quantity_left=Quantity_left_,Quantity_sold=sold)
    object=Stock.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-add-sale.html',{'obj':object,'message1':message1,'message2':message2,'business':business,'username':username})

@login_required
def listsale(request):
    object=Sales.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-list-sale.html',{'object':object,'username':username,'business':business})
@login_required
def editproduct(request,idd):
    object=Stock.objects.filter(user=request.user,id=idd)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'edit-product-page.html',{'objects':object,'username':username,'business':business})
@login_required
def viewproduct(request,idd):
    object=Stock.objects.filter(id=idd,user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'view-product-page.html',{'objects':object,'business':business,'username':username})

@login_required
def viewsales(request,idd):
    object=Sales.objects.filter(id=idd)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    context={
        'object':object,
        'username':username,
        'business':business
    }

    return render(request,'view-sale-page.html',context)

@login_required
def addpurchase(request):
    if request.method=="POST":
        date=request.POST['date']
        purchase_num=request.POST['pn']
        Supplier=request.POST['type']
        Vat=request.POST['vat']
        Discount=request.POST['dis']
        Shipping=request.POST['ship']
        Payment=request.POST['Payment']
        Purchase_note=request.POST['data-long']
    
        objects=Purchase.objects.create(user=request.user,Date=date,Purchase_number=purchase_num,
        Supplier=Supplier,Vat=Vat,Discount=Discount,Shipping=Shipping,
        Payment=Payment,Purchase_note=Purchase_note)
        objects.save()

        object=Purchase.objects.filter(user=request.user,Date=date,Purchase_number=purchase_num,
        Supplier=Supplier,Vat=Vat,Discount=Discount,Shipping=Shipping,
        Payment=Payment,Purchase_note=Purchase_note)
        for data in object:
            obje=data.id
        a=len(Purchase.objects.filter(user=request.user))
        b=int(a)+1
        objects=Usermanage.objects.filter(user=request.user)
        
        for data in objects:
            username=data.Username
        obj=Addbusiness.objects.all()
        for data in obj:
            business=data.Business_name
        return render(request,'add-purchase-product.html',{'obj':obje,'username':username,'business':business,'b':b,'date':date,'purchase_note':Purchase_note,'purchase_num':purchase_num,'supplier':Supplier,'Shipping':Shipping})
    a=len(Purchase.objects.filter(user=request.user))
    b=int(a)+1
    return render(request,'page-add-purchase.html',{'b':b})

@login_required
def listpurchase(request):
    object=Purchase.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-list-purchase.html',{'objects':object,'username':username,'business':business})

@login_required
def editsalepage(request,idd):
    object=Sales.objects.filter(id=idd)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'edit-sale-page.html',{'object':object,'username':username,'business':business})

@login_required
def addreturns(request,ids):
    object=Sales.objects.filter(id=ids,user=request.user)
    try:
        if request.method=='POST':
            Date=request.POST['date']
            Product=request.POST['product']
            Customer=request.POST['customer']
            Quantity=request.POST['quantity']
            Rate=request.POST['rate']
            Discount=request.POST['discount']
            Vat=request.POST['vat']
            Paid=request.POST['paid']
            Total=request.POST['total']
            Payment_status=request.POST['payment_status']
            Return_note=request.POST['salesnote']

            object=Return.objects.create(user=request.user,Date=Date,Product=Product,Customer=Customer,Quantity=Quantity,Rate=Rate,Discount=Discount,Vat=Vat,Paid=Paid,Total=Total,Payment_status=Payment_status,Return_note=Return_note)
            object.save()
            #retrieveing data from the sales object:
            obj=Sales.objects.filter(Date=Date,Product=Product,Customer=Customer,user=request.user)
            for data in obj:
                Quantitya=float(data.Quantity)-float(Quantity)
                total=float(data.Total)-float(Total)
                paid=float(data.Paid)-float(Paid)
            #updating quantity in stock and sales
            obj.update(Quantity=Quantitya,Total=total,Paid=paid)

            #for stock...
            obj_stock=Stock.objects.filter(Product_name=Product,user=request.user)
            for data in obj_stock:
                Quantitys=float(data.Quantity_left)+float(Quantity)
                sold=float(data.Quantity_sold)-float(Quantity)
            obj_stock.update(Quantity_left=Quantitys,Quantity_sold=sold)
        objects=Usermanage.objects.filter(user=request.user)
        for data in objects:
            username=data.Username
        obj=Addbusiness.objects.filter(user=request.user)
        for data in obj:
            business=data.Business_name
        obj=Return.objects.all()
        return render(request,'page-add-return.html',{'username':username,'object':obj,'business':business})
    except:
        objects=Usermanage.objects.filter(user=request.user)
        for data in objects:
            username=data.Username
        obj=Addbusiness.objects.filter(user=request.user)
        for data in obj:
            business=data.Business_name
        obj=Sales.objects.filter(user=request.user,id=ids)
        message="Please validate the total field"
        return render(request,'page-edit-return.html',{'message':message,'username':username,'object':obj,'business':business})
@login_required
def listreturn(request):
    obj=Return.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    objs=Addbusiness.objects.filter(user=request.user)
    for data in objs:
        business=data.Business_name
    return render(request,'list-return-page.html',{'object':obj,'username':username,'business':business})

@login_required
def report(request):
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-report2.html',{'username':username,'business':business})

@login_required
def addpurchaseitems(request,idd):
    object=Purchase.objects.filter(id=idd,user=request.user)
    for objec in object:
        date=objec.Date
        Purchase_num=objec.Purchase_number
        Supplier=objec.Supplier
        tax=objec.Vat
        
    if request.method=="POST":
        # object=Purchase.objects.filter(id=idd,user=request.user)
        # print(object)
        # for objec in object:
        #     date=objec.Date
        #     Purchase_num=objec.Purchase_number
        #     Supplier=objec.Supplier
        #     tax=objec.Vat
        # print(date)
        Product=request.POST['date']
        Quantity=request.POST['quanity']
        Rate=request.POST['rate']
        Total=request.POST['total']
        #for stock maintenance..
        
        objects=Purchase_items.objects.create(user=request.user,Date=date,Purchase_number=Purchase_num,
        Supplier=Supplier,Product_name=Product,Quantity=Quantity,Rate=Rate,Total=Total)
        objects.save()
    

        obj=Stock.objects.filter(Product_name=Product,user=request.user)
        if len(obj)==0:
            
            #saving to stockkkk...
            if tax>0:
                objec=Stock.objects.create(user=request.user,Quantity_sold=0,Product_name=Product,Cost_Price=Rate,Selling_Price=0,Quantity_left=Quantity,Suppliers=Supplier,Tax_method="Inclusive",Quantity=Quantity,Summary="")
                objec.save()
            elif tax<=0:
                objec=Stock.objects.create(user=request.user,Quantity_sold=0,Product_name=Product,Cost_Price=Rate,Selling_Price=0,Quantity_left=Quantity,Suppliers=Supplier,Tax_method="Exclusive",Quantity=Quantity,Summary="")
                objec.save()
        else:
            for data in obj:
                left_quantity=float(Quantity)+float(data.Quantity_left)
                Quantity=float(Quantity)+float(data.Quantity)
            obj.update(Cost_Price=Rate,Quantity=Quantity,Quantity_left=left_quantity)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'add-purchase-product.html',{'obj':idd,'username':username,'business':business})

@login_required
def addreturn(request):
    object=Sales.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-add-return.html',{'object':object,'username':username,'business':business})

@login_required
def invoicebill(request,idd):

    object=Purchase.objects.filter(id=idd,user=request.user)
    for objec in object:
        date=objec.Date
        Purchase_num=objec.Purchase_number
        Supplier=objec.Supplier
        Shipping=objec.Shipping
        notes=objec.Purchase_note
        discount=objec.Discount
        vat=objec.Vat
        paid=objec.Payment
    datas=Purchase_items.objects.filter(Supplier=Supplier,Date=date,user=request.user,Purchase_number=Purchase_num)
    total=0.0
    for data in datas:
        total=round(total+float(data.Total),2)
    #for discoutn
    discount_amount=round((float(discount)/100)*total,2)
    #for total:
    discounts=total-discount_amount
    vat_amount=round((float(vat)/100)*discounts,2)
    net_total=discounts+vat_amount
    remain=round(net_total-float(paid),2)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    context={
        'date':date,
        'purchase':Purchase_num,
        'Supplier':Supplier,
        'object':datas,
        'notes':notes,
        'Shipping':Shipping,
        'total':total,
        'dis':discount_amount,
        'discount':discount,
        'vat':vat_amount,
        'vats':vat,
        'net_total':net_total,
        'paid':paid,
        'remain':remain,
        'username':username,
        'business':business
    }
    return render(request,'pages-invoice.html',context)

@login_required
def profile(request):
    object1=Usermanage.objects.filter(user=request.user)
    object=Addbusiness.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'user-profile-edit.html',{'objects':object1,'object':object,'username':username,'business':business})
@login_required
def addbusiness(request):
    if request.method=='POST':
        Business_name=request.POST['name']
        Business_email=request.POST['email']
        Business_address=request.POST['add']
        obj=Addbusiness.objects.filter(user=request.user)
        obj.update(user=request.user,Business_name=Business_name,Business_Address=Business_address,Business_email=Business_email)
    
    object=Addbusiness.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'user-profile-edit.html',{'object':object,'username':username,'business':business})

@login_required
def adduserdetails(request):
    if request.method=='POST':
        Firstname=request.POST['firstname']
        Lastname=request.POST['lastname']
        Username=request.POST['username']
        City=request.POST['city']
        Gender=request.POST['customRadio1']
        DOB=request.POST['dob']
        Marital_status=request.POST['mar']
        Age=request.POST['age']
        Country=request.POST['country']
        State=request.POST['state']
        Address=request.POST['add']
        obj=Usermanage.objects.filter(user=request.user)
        obj.update(user=request.user,Firstname=Firstname,Lastname=Lastname,Username=Username,
        City=City,Gender=Gender,DOB=DOB,Marital_status=Marital_status,
        Age=Age,Country=Country,State=State,Address=Address)
    
    object=Usermanage.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'user-profile-edit.html',{'objects':object,'username':username,'business':business})

@login_required
def search_report(request):

    if request.method=='POST':
        factor=request.POST['factor']
        search_start=request.POST['search_start']
        search_end=request.POST['search_end']
        if factor=='Sales':
            obj=Sales.objects.filter(Date__range=(search_start,search_end),user=request.user)
            return render(request,'page-report2.html',{'object':obj,'sales':"sales",'start':search_start,'end':search_end})
        if factor=='Purchase':
            obj=Purchase.objects.filter(user=request.user,Date__range=(search_start,search_end))
            return render(request,'page-report2.html',{'objects':obj,'purchase':"purchase",'start':search_start,'end':search_end})
        if factor=='Return':
            obj=Return.objects.filter(user=request.user,Date__range=(search_start,search_end))
            return render(request,'page-report2.html',{'object':obj,'return':"return",'start':search_start,'end':search_end})
        if factor=='Salesbill':
            obj=Salesbill.objects.filter(user=request.user,Date__range=(search_start,search_end))
            return render(request,'page-report2.html',{'objects':obj,'salesbill':"salesbill",'start':search_start,'end':search_end})
    return render(request,'page-report2.html')


@login_required
def addsalebill(request):
    if request.method=="POST":
        date=request.POST['date']
        purchase_num=request.POST['pn']
        Supplier=request.POST['type']
        Vat=request.POST['vat']
        Discount=request.POST['dis']
        Shipping=request.POST['ship']
        Payment=request.POST['Payment']
        Purchase_note=request.POST['data-long']
    
        objects=Salesbill.objects.create(user=request.user,Date=date,Purchase_number=purchase_num,
        Supplier=Supplier,Vat=Vat,Discount=Discount,Shipping=Shipping,
        Payment=Payment,Purchase_note=Purchase_note)
        objects.save()

        object=Salesbill.objects.filter(user=request.user,Date=date,Purchase_number=purchase_num,
        Supplier=Supplier,Vat=Vat,Discount=Discount,Shipping=Shipping,
        Payment=Payment,Purchase_note=Purchase_note)
        for data in object:
            obje=data.id
        a=len(Salesbill.objects.filter(user=request.user))
        b=int(a)+1
        objects=Usermanage.objects.filter(user=request.user)
        
        for data in objects:
            username=data.Username
        obj=Addbusiness.objects.all()
        for data in obj:
            business=data.Business_name
        
        obj_stock=Stock.objects.filter(user=request.user)
        print(obj_stock)
        return render(request,'add-sale-product.html',{'obj':obje,'objj':obj_stock,'username':username,'business':business,'b':b,'date':date,'purchase_note':Purchase_note,'purchase_num':purchase_num,'supplier':Supplier,'Shipping':Shipping})
    a=len(Salesbill.objects.filter(user=request.user))
    b=int(a)+1
    return render(request,'add-sale-bill.html',{'b':b})
@login_required
def addsaleitems(request,idd):
    object=Salesbill.objects.filter(id=idd,user=request.user)
    for objec in object:
        date=objec.Date
        Purchase_num=objec.Purchase_number
        Supplier=objec.Supplier
        tax=objec.Vat
        dis=objec.Discount
        
    if request.method=="POST":
        # object=Purchase.objects.filter(id=idd,user=request.user)
        # print(object)
        # for objec in object:
        #     date=objec.Date
        #     Purchase_num=objec.Purchase_number
        #     Supplier=objec.Supplier
        #     tax=objec.Vat
        # print(date)
        Product=request.POST['date']
        Quantity=request.POST['quanity']
        Rate=request.POST['rate']
        Total=request.POST['total']
        #for stock maintenance..
        obj=Stock.objects.filter(Product_name=Product,user=request.user)
        if len(obj)==0:
            message1="Stock Not Found"
        else:
            for data in obj:
                obj=Stock.objects.filter(Product_name=Product,user=request.user)
                for data in obj:
                
                    Quantity_left_=float(data.Quantity_left)-float(Quantity)
                    sold=float(data.Quantity_sold)+float(Quantity)
                if Quantity_left_<0:
                    message2="Out of stock."
                    return render(request,'add-sale-product.html',{'message1':message2})
                else:
                    discountt=round((float(dis)/100)*float(Total),2)
                    totalis=round(float(Total)-float(discountt),2)
                    total_Vat=round((float(tax)/100)*float(totalis),2)
                    net_amount=totalis+total_Vat
                    objects=Sales_items.objects.create(user=request.user,Date=date,Purchase_number=Purchase_num,
            Supplier=Supplier,Product_name=Product,Quantity=Quantity,Rate=Rate,Total=Total,net_total=net_amount)
                    objects.save()
                    obj.update(Quantity_left=Quantity_left_,Quantity_sold=sold)
           
    

        obj=Stock.objects.filter(Product_name=Product,user=request.user)
        

        
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    obj_stock=Stock.objects.filter(user=request.user)

    return render(request,'add-sale-product.html',{'obj':idd,'objj':obj_stock,'username':username,'business':business})
@login_required
def showsalebill(request):
    object=Salesbill.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-list-salebill.html',{'objects':object,'username':username,'business':business})
@login_required
def invoicebills(request,idd):

    object=Salesbill.objects.filter(id=idd,user=request.user)
    for objec in object:
        date=objec.Date
        Purchase_num=objec.Purchase_number
        Supplier=objec.Supplier
        Shipping=objec.Shipping
        notes=objec.Purchase_note
        discount=objec.Discount
        vat=objec.Vat
        paid=objec.Payment
    datas=Sales_items.objects.filter(Supplier=Supplier,Date=date,user=request.user,Purchase_number=Purchase_num)
    total=0.0
    for data in datas:
        total=round(total+float(data.Total),2)
    #for discoutn
    discount_amount=round((float(discount)/100)*total,2)
    #for total:
    discounts=total-discount_amount
    vat_amount=round((float(vat)/100)*discounts,2)
    net_total=discounts+vat_amount
    remain=round(net_total-float(paid),2)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    context={
        'date':date,
        'purchase':Purchase_num,
        'Supplier':Supplier,
        'object':datas,
        'notes':notes,
        'Shipping':Shipping,
        'total':total,
        'dis':discount_amount,
        'discount':discount,
        'vat':vat_amount,
        'vats':vat,
        'net_total':net_total,
        'paid':paid,
        'remain':remain,
        'username':username,
        'business':business
    }
    return render(request,'pages-invoice.html',context)

@login_required
#for search field....
def product_search(request):
    # search_fields = ["Product_name", "Suppliers", "Summary"]
    if request.method=='POST':
        search_text=request.POST['search']

    # I want to dynamically generate this query
    # qs=Stock.objects.all()
        qs=Stock.objects.filter(Q(Product_name__contains=search_text) | Q(Suppliers__contains=search_text) | Q(Summary__contains=search_text))
        return render(request,'page-list-product.html',{'object':qs})
@login_required
def purchase_search(request):
    # search_fields = ["Product_name", "Suppliers", "Summary"]
    if request.method=='POST':
        search_text=request.POST['search']

    # I want to dynamically generate this query
    # qs=Stock.objects.all()
        qs=Purchase.objects.filter(Q(Supplier_name__contains=search_text) | Q(Shipping__contains=search_text) | Q(Purchase_note__contains=search_text))
        return render(request,'page-list-purchase.html',{'objects':qs})
@login_required
def sale_search(request):
    # search_fields = ["Product_name", "Suppliers", "Summary"]
    if request.method=='POST':
        search_text=request.POST['search']

    # I want to dynamically generate this query
    # qs=Stock.objects.all()
        qs=Sales.objects.filter(Q(Product__contains=search_text) | Q(Customer__contains=search_text) | Q(Sales_note__contains=search_text))
        return render(request,'page-list-sale.html',{'object':qs})

@login_required
def sale_search_bill(request):

    # search_fields = ["Product_name", "Suppliers", "Summary"]
    if request.method=='POST':
        search_text=request.POST['search']

    # I want to dynamically generate this query
    # qs=Stock.objects.all()
        qs=Salesbill.objects.filter(Q(Date__contains=search_text) |Q(Supplier__contains=search_text) | Q(Shipping__contains=search_text) | Q(Purchase_note__contains=search_text))
        return render(request,'page-list-salebill.html',{'objects':qs})
@login_required
def return_search(request):

    # search_fields = ["Product_name", "Suppliers", "Summary"]
    if request.method=='POST':
        search_text=request.POST['search']

    # I want to dynamically generate this query
    # qs=Stock.objects.all()
        qs=Return.objects.filter(Q(Product__contains=search_text) | Q(Customer__contains=search_text) | Q(Return_note__contains=search_text))
        return render(request,'list-return-page.html',{'object':qs})

@login_required
def updateproduct(request):

    if request.method=="POST":
        product=request.POST['product']
        cp=request.POST['cp']
        sp=request.POST['cp']
        tax=request.POST['type']
        suppliers=request.POST['suppliers']
        quantity=request.POST['quantity']
        summary=request.POST['des']
        obj=Stock.objects.filter(Product_name=product)
        sold=int(quantity)
        obj.update(user=request.user,Product_name=product,Cost_Price=cp,Selling_Price=sp,Suppliers=suppliers,Tax_method=tax,Quantity=quantity,Summary=summary)
           
        

       
    object=Stock.objects.filter(user=request.user)
    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'pageadd-product.html',{'obj':object,'username':username,'business':business})
    # return render(request,'page-list-product.html') 

def editbill(request,idd):
    # obj_return=Salesbill.objects.filter(id=idd,user=request.user)
    object=Salesbill.objects.filter(id=idd,user=request.user)
  
    for objec in object:
        date=objec.Date
        Purchase_num=objec.Purchase_number
        Supplier=objec.Supplier
        tax=objec.Vat
        dis=objec.Discount
    obj_sales=Sales_items.objects.filter(user=request.user,Date=date,Purchase_number=Purchase_num,Supplier=Supplier)
    for data in obj_sales:
        print(data.id)
    p=Paginator(obj_sales,1)
    page=request.GET.get('page')
    data=p.get_page(page)
    
    # pagination code for each items ........................
    return render(request,'page-edit-bill.html',{'object':data})
    #harek page ko product lai manually add garne
def updatebillproduct(request,idd):
    message1=""
    message2=""
    if request.method=='POST':
        obj_sbitems=Sales_items.objects.filter(user=request.user,id=idd)
        date=request.POST['date']
        product=request.POST['product']
        quantity=request.POST['quantity']
        rate=request.POST['rate']
        total=request.POST['total']
        obj=Stock.objects.filter(Product_name=product,user=request.user)
        object=Sales_items.objects.filter(user=request.user,id=idd)
        for data in object:
            old_quantity=float(data.Quantity)
        if len(obj)==0:
            message1="Stock Not Found"
            object=Sales_items.objects.filter(user=request.user,id=idd)
            return render(request,'page-edit-bill.html',{'message1':message1,'object':object})
        else:
            for data in obj:
                obj=Stock.objects.filter(Product_name=product,user=request.user)
                for data in obj:
                    a=float(data.Quantity_left)
                    b=float(data.Quantity_sold)
                    Quantity_left_=a+old_quantity-float(quantity)
                    sold=float(old_quantity)+b-float(quantity)
                if Quantity_left_<0:
                    message2="Out of stock."
                    object=Sales_items.objects.filter(user=request.user,id=idd)
                    return render(request,'page-edit-bill.html',{'message2':message2,'object':object})
                else:
                    obj_sbitems.update(Date=date,Product_name=product,Quantity=quantity,Rate=rate,Total=total,net_total=total)
                    obj.update(Quantity_left=Quantity_left_,Quantity_sold=sold)
    obj_sales=Sales_items.objects.filter(user=request.user,id=idd)
    for data in obj_sales:
        print(data.id)
    p=Paginator(obj_sales,1)
    page=request.GET.get('page')
    data=p.get_page(page)
    context={

    }
    return render(request,'page-edit-bill.html',{'object':data})
    #concept is withdrawing hereeeeee........................................................................

@login_required
def editpurchasebill(request,idd):

    # obj_return=Salesbill.objects.filter(id=idd,user=request.user)
    object=Purchase.objects.filter(id=idd,user=request.user)
    for objec in object:
        date=objec.Date
        Purchase_num=objec.Purchase_number
        Supplier=objec.Supplier
        tax=objec.Vat
        dis=objec.Discount
    obj_pur=Purchase_items.objects.filter(user=request.user,Date=date,Purchase_number=Purchase_num,Supplier=Supplier)
    
    p=Paginator(obj_pur,1)
    page=request.GET.get('page')
    data=p.get_page(page)
    
    # pagination code for each items ........................
    return render(request,'page-edit-p-bill.html',{'object':data})
    #harek page ko product lai manually add garne
@login_required
def updatepbillproduct(request,idd):
    message1=""
    message2=""
    if request.method=='POST':
        obj_sbitems=Purchase_items.objects.filter(user=request.user,id=idd)
        date=request.POST['date']
        product=request.POST['product']
        quantity=request.POST['quantity']
        rate=request.POST['rate']
        total=request.POST['total']
        for data in obj_sbitems:
            quantitys=float(data.Quantity)
        obj_sbitems.update(user=request.user,Date=date,Product_name=product,Quantity=quantity,Rate=rate,Total=total)
    

        obj=Stock.objects.filter(Product_name=product,user=request.user)
        if len(obj)==0:
            objec=Stock.objects.create(user=request.user,Quantity_sold=0,Product_name=product,Cost_Price=rate,Selling_Price=0,Quantity_left=quantity,Tax_method="Exclusive",Quantity=quantity,Summary="")
            objec.save()
           
        else:
            obj=Stock.objects.filter(Product_name=product,user=request.user)
            for data in obj:
                left_quantity=float(data.Quantity_left)-quantitys+float(quantity)
                Quantity=float(data.Quantity)-quantitys+float(quantity)
            obj.update(Cost_Price=rate,Quantity=Quantity,Quantity_left=left_quantity)
            print("Updated Successfully..")
    
    obj_pur=Purchase_items.objects.filter(user=request.user,id=idd)
    p=Paginator(obj_pur,1)
    page=request.GET.get('page')
    datas=p.get_page(page)

    objects=Usermanage.objects.filter(user=request.user)
    for data in objects:
        username=data.Username
    obj=Addbusiness.objects.filter(user=request.user)
    for data in obj:
        business=data.Business_name
    return render(request,'page-edit-p-bill.html',{'object':datas,'username':username,'business':business})
