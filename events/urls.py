from django.urls import path
from events.views import home,dashboard,event_detail,add_event,add_category,add_participant,delete_event,update_event

urlpatterns = [
    path(' ',home , name='home'),
    path('dashboard_o/', dashboard, name='dashboard_o'),
     path("event/<int:id>/", event_detail, name="event-detail"),
    path("event/add/", add_event, name="add_event"),
    path("event/update/<int:id>/", update_event, name="update_event"),
    path("event/delete/<int:id>/", delete_event, name="delete_event"),
    path("category/add/", add_category, name="add_category"),
    path("participant/add/", add_participant, name="add_participant"),

] 