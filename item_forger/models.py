from django.utils.translation import ugettext_lazy as _
from django.db.models import CharField, TextField, IntegerField, AutoField, ForeignKey
from mezzanine.core.models import TimeStamped
from .queries import ItemCollectionQuerySet


class RPItem(TimeStamped):
    """
    from TimeStamped:
        updated = models.DateTimeField(...)
        created = models.DateTimeField(...)
    """

    ARMOR = 10
    POTION = 20
    RING = 30
    AMULET = 40
    ROD = 50
    SCROLL = 60
    STAFF = 70
    WAND = 80
    WEAPON = 90
    WONDEROUS_ITEM = 100
    TRINKET = 110
    ITEM_TYPE = (
        (ARMOR, _("Armor")),
        (POTION, _("Potion")),
        (RING, _("Ring")),
        (AMULET, _("Amulet")),
        (ROD, _("Rod")),
        (SCROLL, _("Scroll")),
        (STAFF, _("Staff")),
        (WAND, _("Wand")),
        (WEAPON, _("Weapon")),
        (WONDEROUS_ITEM, _("Wonderous Item")),
        (TRINKET, _("Trinket")),
    )

    MUNDANE = 10  # Black
    COMMON = 20  # Grey ?
    UNCOMMON = 30  # Green
    RARE = 40  # Blue
    VERY_RARE = 50  # Silver
    LEGENDARY = 60  # Gold
    ARTIFACT = 70  # Orange
    RARITY_LEVEL = (
        (MUNDANE, _("Mundane")),
        (COMMON, _("Common")),
        (UNCOMMON, _("Uncommon")),
        (RARE, _("Rare")),
        (VERY_RARE, _("Very Rare")),
        (LEGENDARY, _("Legendary")),
        (ARTIFACT, _("Artifact")),
    )
    YES = "Yes"
    NO = "No"
    SPECIAL = "Special"
    ATTUNEMENT = ((YES, _("Yes")), (NO, _("No")), (SPECIAL, _("Special")))

    id = AutoField(primary_key=True)
    # Creator of item should be added
    campaign = CharField(max_length=200, null=True, blank=True, default=None)
    name = CharField(max_length=200)
    rarity = IntegerField(
        verbose_name=_("Item Rarity"),
        choices=RARITY_LEVEL,
        default=MUNDANE,
        null=True,
        blank=True,
    )
    attunement = CharField(
        verbose_name=_("Requires Attunemnet"),
        choices=ATTUNEMENT,
        max_length=10,
        default=YES,
        null=True,
        blank=True,
    )
    type = IntegerField(
        verbose_name=_("Item type"),
        choices=ITEM_TYPE,
        default=None,
        null=True,
        blank=True,
    )
    value = CharField(max_length=100, null=True, blank=True, default=None)
    description = TextField()
    benefits = TextField()
    # tags for the item should go here as well. for searching. later edition.\

    # Add this in when things are stable. The figure out proper error checking. Crispy
    # doesn't do it automatically
    # class Meta:
    #     unique_together= ("name", 'campaign') #and user
    objects = ItemCollectionQuerySet.as_manager()

    def __str__(self):
        return self.name

    @property
    def rarity_text(self):
        if self.rarity is None:
            return "---"
        rarity_text = {key: value for key, value in self.RARITY_LEVEL}
        return rarity_text[self.rarity]

    @property
    def type_text(self):
        if self.type is None:
            return "---"
        type_text = {key: value for key, value in self.ITEM_TYPE}
        return type_text[self.type]

    @property
    def get_notes(self):
        return Notes.objects.filter(item=self.id)


class Notes(TimeStamped):

    # user
    item = ForeignKey("RPItem", null=True, blank=True)
    note = TextField()
