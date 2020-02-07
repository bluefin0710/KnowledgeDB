#from django.conf.urls import url
#from django.contrib.auth import views as auth_views
#from django.contrib.auth import views as auth_views
#from django.conf import settings
#from django.conf.urls.static import static
from django.urls import path
from . import views

#from posts.views import (
#        Indexlistview,
#        Postdetailview,
#        Searchlistview,
#        EquipmentListView,
#        CategoryListView,
#        SubcategoryListView,
#        StateListView,
#        SearchPostView,
#        EquipmentPostView,
#        CategoryPostView,
#        SubcategoryPostView,
#        StatePostView,
#        PopupEquipmentCreate,
#        PopupSubcategoryCreate,
##        PostDeleteView,
#        )

app_name = 'posts'
urlpatterns = [
    path('',views.Indexlistview.as_view(), name='index_listview'),

#    path('signup/', views.signup, name='signup'),
#    path('login/', auth_views.LoginView.as_view(template_name='posts/login.html'), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#-- Password Change
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
#-- Password Reset
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),


    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
#    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
#    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
#    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
#    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
#    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
#    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),




    path('mypage/', views.MypageView.as_view(), name='mypage'),

#    path('print', views.PrintView.as_view(), name='print'),
#    path('excel', views.ExcelView.as_view(), name='excel'),
#    path('csv', views.CsvView.as_view(), name='csv'),
    path('<int:pk>/print/', views.PrintView.as_view(), name='post_print'),
  
    path('<int:pk>/', views.Postdetailview.as_view(), name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
#    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
       
    path('new/', views.post_new, name='post_new'),
    path('list/', views.Searchlistview.as_view(), name='search_listview'),

    path('equipments/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('subcategories/', views.SubcategoryListView.as_view(), name='subcategory_list'),
    path('states/', views.StateListView.as_view(), name='state_list'),

    path('equipment/<str:equipment_slug>/',
         views.EquipmentPostView.as_view(), name='equipment_post'),
    path('category/<str:category_slug>/',
         views.CategoryPostView.as_view(), name='category_post'),
    path('subcategory/<str:subcategory_slug>/',
         views.SubcategoryPostView.as_view(), name='subcategory_post'),
    path('state/<str:state_slug>/', views.StatePostView.as_view(), name='state_post'),

    path('search/', views.SearchPostView.as_view(), name='search_post'),

    path('popup/equipment_create/',
         views.PopupEquipmentCreate.as_view(), name='popup_equipment_create'),
    path('popup/subcategory_create/',
         views.PopupSubcategoryCreate.as_view(), name='popup_subcategory_create'),

##    url(r'^$',views.index, name='index'),
#    url(r'^$',INDEXlistview.as_view(), name='index_listview'),
##    url(r'^login/', auth_views.LoginView.as_view(template_name='posts/login.html'), name='login'),
##   url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
##    url(r'^(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
#    url(r'^(?P<pk>[0-9]+)/$', Postdetailview.as_view(), name='post_detail'),
#    url(r'^(?P<pk>[0-9]+)/edit/', views.post_edit, name='post_edit'),
##    url(r'^(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
##    url(r'^(?P<pk>[0-9]+)/edit/', views.post_edit, name='post_edit'),
#    url(r'^new/', views.post_new, name='post_new'),
#    url(r'^list/', Searchlistview.as_view(), name='search_listview'),
#
#    url(r'^equipments/', EquipmentListView.as_view(), name='equipment_list'),
#    url(r'^categories/', CategoryListView.as_view(), name='category_list'),
#    url(r'^subcategories/', SubcategoryListView.as_view(), name='Subcategory_list'),
#    url(r'^states/', StateListView.as_view(), name='State_list'),
##    url(r'^posts/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
##    url(r'^posts/(?P<post_id>[0-9]+)/edit/', views.post_edit, name='post_edit'),
##    url(r'^posts/new/', views.post_new, name='post_new'),
##    url(r'^posts/list/', PostView.as_view(), name='post_view'),
#
##   url(r'^templates/',views.index_template, name='index_template')
##    path('post/new/', views.post_new, name='post_new'),

]
#urlpatterns += static(settings.MEDIA_URL,
#                      document_root=settings.MEDIA_ROOT)
