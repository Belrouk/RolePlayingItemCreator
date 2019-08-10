from django.db.models import (
    Manager,
    Prefetch,
    Q,
    QuerySet,
)


class ItemCollectionQuerySet(QuerySet):
    # def prefetch(self, *args, **kwargs):
    #     return self.prefetch_related()

    def filter_item_query(self, rarity, attunement, type, campaign, *args, **kwargs):
        query = self
        if rarity and int(rarity) > 0:
            query = query.filter(rarity=rarity)
        if attunement:
            query = query.filter(attunement=attunement)
        if type and int(type) > 0:
            query = query.filter(type=type)
        if campaign:
            query = query.filter(campaign=campaign)
        return query
