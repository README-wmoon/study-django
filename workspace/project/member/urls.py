from django.urls import path

from member.views import MemberJoinView, MemberCheckIdView, MemberLoginView, MemberLogoutView, MemberMyPageAppView, \
    MemberCollegeJoinView

app_name = 'member'

urlpatterns = [
    path('join/', MemberJoinView.as_view(), name='join'),
    path('login/', MemberLoginView.as_view(), name='login'),
    path('check-id/', MemberCheckIdView.as_view(), name='check-id'),
    path('mypage/', MemberMyPageAppView.as_view(), name='mypage'),
    path('logout/', MemberLogoutView.as_view(), name='logout'),
    path('collegejoin/', MemberCollegeJoinView().as_view(), name='collegejoin')
]
