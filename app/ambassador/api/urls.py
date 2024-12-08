from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path('v1/ambassador/', include('ambassador.api.v1.urls')),
]
