from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('dashboard',views.index,name="index"),
    path('profile',views.profile,name='profile'),
    path('addbusiness',views.addbusiness),
    path('adduserdetails',views.adduserdetails),
    path('',views.logins,name='login'),
    path('add-product',views.addproduct,name='add-product'),
    path('list-product',views.productlist,name='list-product'),
    path('add-sale',views.addsale,name='add-sale'),
    path('list-sale',views.listsale,name='list-sale'),
    path('edit-product<int:idd>',views.editproduct),
    path('view-product<int:idd>',views.viewproduct),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search-report',views.search_report),

    path('add-purcahse',views.addpurchase,name="add-purchase"),
    path('report',views.report,name="report"),
    path('list-purchase',views.listpurchase,name='list-purchase'),
    path('list-return',views.listreturn,name="list-return"),
    path('add-return',views.addreturn,name="add-return"),
    path('add-purchase-items<int:idd>',views.addpurchaseitems,name="add-purchase-item"),
        path('add-sale-items<int:idd>',views.addsaleitems,name=""),

    # path('add-purchase-items',views.addpurchaseitems,name="add-purchase-items"),
    path('view<int:idd>',views.invoicebill,name='view-bill'),
    path('view-sales-page-<int:idd>',views.viewsales,name='sales-view'),
    path('edit-sales-page<int:idd>',views.editsalepage),
    path('return-sales-page<int:idd>',views.returnsalepage,name=""),
    path('add-return<int:ids>',views.addreturns),
    path('add-sale-bill',views.addsalebill),
    path('show-sale-bill',views.showsalebill),
     path('views<int:idd>',views.invoicebills),
     path('searchstock',views.product_search),
     path('searchreturn',views.return_search),
    path('searchpurchase',views.purchase_search),
    path('searchsale',views.sale_search),
    path('searchsalebill',views.sale_search_bill),
    path('updateproduct',views.updateproduct),
    path('editbill<int:idd>',views.editbill),
    path('editpurchasebill<int:idd>',views.editpurchasebill),
    path('updateproductbill<int:idd>',views.updatebillproduct),
    path('updatepbill<int:idd>',views.updatepbillproduct),


]
