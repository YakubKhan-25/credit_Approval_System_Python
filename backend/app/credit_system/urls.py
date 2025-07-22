"""credit_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core.views.register_view import register_customer
from core.views.loan_view import (
    check_eligibility_view,
    createLoan,
    view_loan_by_id,
    view_loans_by_customer,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_customer),
    path("check-eligibility/", check_eligibility_view),
    path("create-loan/", createLoan),
    path("view-loan/<int:loan_id>/", view_loan_by_id),
    path("view-loans/<int:customer_id>/", view_loans_by_customer),
]
