from django.urls import path
from gestion_rv.views import appointment_detail, appointment_list,index , create_appointment,success_page,modify_appointment,cancel_appointment
urlpatterns = [
    path ('',index, name ='index'),
    path('appointment_list/',appointment_list, name='appointment_list'),
    path('<int:pk>/',appointment_detail, name='appointment_detail'),
    path('create-appointment/', create_appointment, name='create_appointment'),
    path('success/',success_page, name='success_page'),
    path('modify-appointment/<int:appointment_id>/',modify_appointment, name='modify_appointment'),
    path('cancel-appointment/<int:appointment_id>/',cancel_appointment, name='cancel_appointment'),
]
