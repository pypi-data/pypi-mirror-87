from django.conf import settings as django_settings
from django.conf.urls import include, static, url
from transcribe.views import reports, web

handler404 = 'transcribe.views.web.display404'
handler500 = 'transcribe.views.web.display500'

project_views = [
    url(r'^$', web.landing_page, name='landing_page'),
    url(r'^help/$', web.help, name='help'),
    url(r'^faq/$', web.faq, name='faq'),
    url(r'^dashboard/$', web.DashboardView.as_view(), name='dashboard'),
    url(
        r'^dashboard/(?P<all_tasks>all_tasks)/$',
        web.DashboardView.as_view(),
        name='dashboard_all_tasks',
    ),
    url(r'^projects/$', web.ProjectListView.as_view(), name='projects_list'),
    # url(r'^project/create/$', 'project_create', name='project_create'),
    url(
        r'^project/(?P<pk>\d+)/$',
        web.ProjectDetailView.as_view(),
        name='project_detail',
    ),
    # url(r'^project/(?P<pk>\d+)/edit/$', 'project_edit', name='project_edit'),
    url(
        r'^project/(?P<pk>\d+)/download\.(?P<type>(xml|txt|html))$',
        web.ProjectDownloadView.as_view(),
        name='project_download',
    ),
    # url(r'^project/(?P<pk>\d+)/delete/$', 'project_delete',
    #     name='project_delete'),
    url(
        r'^project/(?P<pk>\d+)/claim/(?P<type>(review|transcription|any))/$',
        web.ProjectClaimTaskView.as_view(),
        name='project_claim_task',
    ),
    url(
        r'^userpreferences/(?P<pk>\d+)/update/$',
        web.UserPreferencesUpdateView.as_view(),
        name='user_preferences_update',
    ),
    url(
        r'^userprojectpreferences/(?P<pk>\d+)/update/$',
        web.UserProjectPreferencesUpdateView.as_view(),
        name='user_project_preferences_update',
    ),
    url(
        r'^task/(?P<pk>\d+)/$',
        web.UserTaskUpdateView.as_view(),
        name='task_workon',
    ),
]

report_views = (
    [
        url(r'^$', reports.reports_list, name='list'),
        url(
            r'^weekly/task/(?P<project>.*)/$',
            reports.weekly_task_report,
            name='weekly-task',
        ),
        url(
            r'^monthly/task/(?P<project>.*)/$',
            reports.monthly_task_report,
            name='monthly-task',
        ),
        url(
            r'^weekly/usertask/$',
            reports.weekly_user_task_report,
            name='weekly-user-task',
        ),
        url(
            r'^monthly/usertask/$',
            reports.monthly_user_task_report,
            name='monthly-user-task',
        ),
        url(
            r'^weekly/(?P<project>.*)/$',
            reports.weekly_projects_report,
            name='weekly-project',
        ),
        url(
            r'^monthly/(?P<project>.*)/$',
            reports.monthly_projects_report,
            name='monthly-project',
        ),
    ],
    'reports',
)

urlpatterns = [
    # url(r'^', include(authentication_views)),
    url(r'^', include(project_views)),
    url(r'^reports/', include(report_views)),
]

if django_settings.DEBUG:
    static = static.static
    urlpatterns += static(
        django_settings.STATIC_URL, document_root=django_settings.STATIC_ROOT
    )
