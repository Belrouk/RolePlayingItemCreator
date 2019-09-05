from django.db.models import (Count, Exists, F, IntegerField, Manager,
                              OuterRef, Prefetch, Q, QuerySet, Subquery,
                              Sum)

from .models import MagicalItem


class ItemCollectionQuerySet(QuerySet):

    def filter_item_query(self, rarity, attunement, type, campaign, *args, **kwargs):
        M = MagicalItem.objects.all()
        if int(rarity) > 0:
            M = M.filter(rarity=rarity)
        if attunement is not None:
            M = M.filter(attunement=attunement)
        if int(type) > 0:
            M = M.filter(type=type)
        if campaign is not None:
            M = M.filter(campaign=campaign)
        return M
