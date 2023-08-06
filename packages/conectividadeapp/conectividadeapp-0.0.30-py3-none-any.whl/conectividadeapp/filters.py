import django_filters
from django.db.models import Q

from utilities.filters import NameSlugSearchFilterSet

from .models import Actor


class ActorFilter(NameSlugSearchFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        model = Actor
        fields = [
            'name',
            'telephone',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = (
            Q(name__icontains=value)
            | Q(telephone__icontains=value)
            | Q(cellphone__icontains=value)
            | Q(emails__icontains=value)
        )

        return queryset.filter(qs_filter)
