from django.contrib import admin
from django.urls import path
from App import views
from .views import get_berths
from .views import get_autocomplete_suggestions


urlpatterns = [
    path('',views.index_pg, name= 'signin'),
    path('signup/',views.signup_pg, name= 'signup'),
    path('forgotpass/', views.forgotpass_pg, name='forgotpass'),
    path('resetpasssent/<str:reset_id>/', views.resetpasssent_pg, name='resetpasssent'),
    path('resetpass/<str:reset_id>/', views.resetpass_pg, name='resetpass'),

    path('LineUpForm/',views.LineupForm_pg,name='lineupform'),
    path('ExtractData/',views.ExtractData_pg,name='extractdata'),
    path('UpdateLineup/<int:id>',views.UpdateLineup_pg,name='UpdateLineup'),
    path('DeleteLineup/<int:id>',views.DeleteLineup_pg,name='DeleteLineup'),
    path('AddPortBerth/',views.AddPortBerth_pg,name='addportberth'),
    path('GetCookies/',views.set_cookies,name='getcookies'),
    path('get-berths/', views.get_berths, name='get_berths'),
    path('get-updated-berths/', views.get_updated_berths, name='get_updated_berths'),
    path('get-autocomplete-suggestions/', get_autocomplete_suggestions, name='get_autocomplete_suggestions'),

]