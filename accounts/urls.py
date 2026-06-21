from django.contrib import admin
from django.urls import include,path
from .views import create_user_role , get_all_user_roles , get_single_user_role, get_user_role_by_id , get_active_user_role,update_user_role , delete_user_role ,  delete_user_role_update , create_user, verification_email ,get_inactive_user_role , get_active_user_roles_order_by_asc , get_active_user_roles_order_by_desc , get_user_count , get_user_values , get_user_values_list , get_user_names , get_user_aggregate_count, get_user_max_id , get_user_min_id , get_user_avg_id

urlpatterns =[
    path('create_user_role/', create_user_role ,name='create_user_role'),
    path(' get_all_user_roles/', get_all_user_roles,name=' get_all_user_roles'),
    path('get_single_user_role/', get_single_user_role,name='get_single_user_role'),
    path('get_active_user_role/',get_active_user_role, name='get_active_user_role'),
    path('get_user_role_by_id/<int:role_id>/',get_user_role_by_id, name='get_user_role_by_id',),
    path('update_user_role/', update_user_role, name='update_user_role'),
    path('delete_user_role/',delete_user_role, name= 'delete_user_role'),
    path('delete_user_role_update/',  delete_user_role_update , name='delete_user_role_update'),
    path('create_user/',create_user, name='create_user'),
    path('verification_email/', verification_email,name='verification_email'),
    path('get_inactive_user_role/',get_inactive_user_role, name='get_inactive_user_role'),
    path('get_active_user_roles_order_by_asc/',get_active_user_roles_order_by_asc, name='get_active_user_roles_order_by_asc'),
    path('get_active_user_roles_order_by_desc/', get_active_user_roles_order_by_desc, name='get_active_user_roles_order_by_desc'),
    path('get_user_count/',get_user_count, name='get_user_count'),
    path('get_user_values/',get_user_values, name='get_user_values'),
    path('get_user_values_list/',get_user_values_list, name='get_user_values_list'),
    path('get_user_names/',get_user_names,name='get_user_names'),
    path('get_user_aggregate_count/',get_user_aggregate_count,name='get_user_aggregate_count'),
    path('get_user_max_id/',get_user_max_id,name='get_user_max_id'),
    path('get_user_min_id/',get_user_min_id,name='get_user_min_id'),
    path('get_user_avg_id/', get_user_avg_id, name='get_user_avg_id'),
    
]

