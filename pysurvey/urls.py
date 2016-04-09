"""pysurvey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import createSurvey.views
import jobSurvey.views

urlpatterns = [
    url(r'^log_in/', createSurvey.views.AuthLogin.as_view(), name="log_in"),
    url(r'^sign_up/', createSurvey.views.SignUp.as_view(), name="sign_up"),
    url(r'^logout/', createSurvey.views.log_out, name="log_out"),
    url(r'^$', createSurvey.views.Index.as_view(), name="index"),
    url(r'^new_survey', createSurvey.views.NewSurvey.as_view(), name="new_survey"),
    url(r'^preview_survey/(?P<id>[0-9]+)/$', createSurvey.views.PreviewSurvey.as_view(), name="preview_survey"),
    url(r'^make_survey/(?P<id>[0-9]+)/$', createSurvey.views.MakeSurvey.as_view(), name="make_survey"),
    url(r'^result/(?P<id>[0-9]+)/$', createSurvey.views.ResultSurvey.as_view(), name="result"),
    url(r'^download/(?P<type>.*)/(?P<survey_id>[0-9]+)/$', createSurvey.views.result_download, name='result_download'),
    url(r'^studenti/valore/$', jobSurvey.views.StudentiValore.as_view(), name='studenti_valore'),
    url(r'^studenti/$', jobSurvey.views.Studenti.as_view(), name='studenti'),
    url(r'^aziende/$', jobSurvey.views.Aziende.as_view(), name='aziende'),
    url(r'^lavori/$', jobSurvey.views.Lavori.as_view(), name='lavori'),
    url(r'^grazie/$', jobSurvey.views.Grazie.as_view(), name='grazie'),
    url(r'^risultati/aziende/$', jobSurvey.views.RisultatiAziende.as_view(), name='risultati_aziende'),
    url(r'^admin/', include(admin.site.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
