from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from main.views import MainView
from post.views import PostListView
from product.views import ProductDetailView
from view.views import StudentRegisterView, StudentResultView, StudentRegisterFormView, MemberRegisterFormView, \
    MemberRegisterView, UserCalculatorViewForm, UserCalculatorView, UserResultView, PlaceTravelViewForm, \
    PlaceTravelResultView, PlaceTravelView, ProductInfoAPI, MemberResultView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('member/', include('member.urls')),
    path('post/', include('post.urls')),
    # path('product/', include('product.urls')),
    # path('products/', include('product.urls')),
    path('student/register/form/', StudentRegisterFormView.as_view(), name='student-register-form'),
    path('student/register/', StudentRegisterView.as_view(), name='student-register'),
    path('student/result/', StudentResultView.as_view(), name='student-result'),
    path('member/register/form/', MemberRegisterFormView.as_view(), name='member-register-form'),
    path('member/register/', MemberRegisterView.as_view(), name='member-register'),
    path('member/result/', MemberResultView.as_view(), name='member-result'),
    path('product/detail/', ProductDetailView.as_view(), name='product-detail'),
    # path('products/<int:product_id>', ProductDetailAPI.as_view(), name='product-detail'),
    path('', MainView.as_view()),
]













