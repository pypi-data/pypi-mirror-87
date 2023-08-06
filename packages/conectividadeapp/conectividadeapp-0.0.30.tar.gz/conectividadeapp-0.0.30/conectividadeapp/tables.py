import django_tables2 as tables
from django_tables2.utils import Accessor
from utilities.tables import BaseTable, ToggleColumn

from .models import Actor


class ActorTable(BaseTable):
    """     pk = ToggleColumn()
    name = tables.LinkColumn(
        viewname='plugins:conectividadeapp:addactor',
        args=[Accessor('name')]
    ) """

    class Meta(BaseTable.Meta):
        model = Actor
        fields = (
            # 'pk',
            'name',
            'telephone',
            'cellphone',
            'email',
        )
