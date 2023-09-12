from django.urls import path, include
from administrator.views import *
from administrator.views import CuratorCheckAdmin
from administrator.views import StudentsCheckAdmin


app_name = 'admin'

urlpatterns = [
    path('', admin_view, name='administrator'),
    path('add_student/', AddStudent.as_view(), name='add_student'),
    path('add_сurator/', AddCurator.as_view(), name='add_curator'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls', namespace='profile')),
    path('schedule/', include('schedule.urls')),
    path('admin_check/students/', StudentsCheckAdmin.as_view(), name='students_admin_check'),
    path('admin_check/students/search/', SearchStudentsView.as_view(), name='search_students'),
    path('streams/', StreamListView.as_view(), name='stream_list'),
    path('admin/applications/', ContactListView.as_view(), name='admin_applications'),
    path('admin_check/curators/', CuratorCheckAdmin.as_view(), name='curators_admin_check'),
    path('admin_check/curators/search/', SearchCuratorsView.as_view(), name='search_curators'),
    path('view-notifications/', NotificationListView.as_view(), name='view_notifications'),
    path('view-notifications/course/<int:course_id>/', NotificationListView.as_view(), name='view_notifications_by_course'),
    path('create-notification/', NotificationCreateView.as_view(), name='create_notification'),
    path('search/', SearchView.as_view(), name='search'),

    path('add_course/', AddCourseView.as_view(), name='add_course'),
    path('add_module', AddModuleView.as_view(), name='add_module'),

]
