# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse


from royaleaccounts.utils import unique_slug_generator
from tags.models import Tag

import os
import PIL
from PIL import Image
from decimal import *


ARENA_CHOICES = (
	("GS", "Goblin Stadium"),
	("BP", "Bone Pit"),
	("BB" ,"Barbarian Bowl"),
	("PP", "PEKKAs Playhouse"),
	("SV", "Spell Valley"), 
	("BW", "Builder's Workshop"), 
	("RA", "Royal Arena"),
	("FP", "Frozen Peak"), 
	("JA", "Jungle Arena"),
	("HM", "Hog Mountain"), 
	("EV", "Electro Valley"),
	("LA", "Legendary Arena"),
	("C1", "Challenger 1"),
	("C2", "Challenger 2"), 
	("C3", "Challenger 3"),
	("M1", "Master 1"),
	("M2", "Master 2"), 
	("M3", "Master 3"),
	("C", "Champion"), 
	("GC", "Grand Champion"),
	("UC", "Ultimate Champion"),
)

DEVICE_CHOICES = (
	("A", "Android"),
	("I", "iOS"),
	("B", "Android Or iOS"),
)

CARD_CHOICES = (
	("W", "Witch"),
	("SG", "Spear Goblins"),
	("BO", "Bomber"),
	("M", "Musketeer"),
	("TM", "Three Musketeers"),
	("G", "Giant"),
	("SA", "Skeleton Army"),
	("K", "Knight"),
	("A", "Archers"),
	("G", "Goblins"),
	("V", "Valkyrie"),
	("MP", "Mini P.E.K.K.A"),
	("BD", "Baby Dragon"),
	("P", "Prince"),
	("MI", "Minions"),
	("S", "Skeletons"),
	("B", "Balloon"),
	("GS", "Giant Skeleton"),
	("BA", "Barbarians"),
	("MH", "Minion Horde"),
	("HR", "Hog Rider"),
	("PK", "P.E.K.K.A"),
	("L", "Lava Hound"),
	("F", "Fire Spirits"),
	("WI", "Wizard"),
	("RR", "Royale Recruits"),
	("GO", "Golem"),
	("MK", "Mega Knight"),
	("RG", "Royale Giant"),
	("EB", "Elite Barbarians"),
	("SP", "Sparky"),
	("BW", "Bowler"),
	("EX", "Executioner"),
	("CC", "Cannon Cart"),
	("RH", "Royal Hogs"),
	("DP", "Dark Prince"),
	("H", "Hunter"),
	("LU", "Lumberjack"),
	("RA", "Rascals"),
	("ID", "Inferno Dragon"),
	("EW", "Electro Wizard"),
	("NW", "Night Witch"),
	("BR", "Battle Ram"),
	("FM", "Flying Machine"),
	("Z", "Zappies"),
	("MA", "Magic Archer"),
	("SB", "Skeleton Barrel"),
	("MM", "Mega Minion"),
	("GU", "Guards"),
	("GR", "Royale Ghost"),
	("PR", "Princess"),
	("IW", "Ice Wizard"),
	("BN", "Bandit"),
	("MN", "Miner"),
	("GG", "Goblin Gang"),
	("DG", "Dart Goblin"),
	("IG", "Ice Golem"),
	("B", "Bats"),
	("IS", "Ice Spirit"),

	("BH", "Barbarian Hut"),
	("XB", "X-Bow"),
	("EC", "Elixir Collector"),
	("GH", "Goblin Hut"),
	("IT", "Inferno Tower"),
	("MT", "Mortar"),
	("T", "Tesla"),
	("BT", "Bomb Tower"),
	("FU", "Furnace"),
	("C", "Cannon"),
	("TB", "Tombstone"),
	
	("RE", "Rage"),
	("ZA", "Zap"),
	("AW", "Arrows"),
	("FI", "Fireball"),
	("LI", "Lightning"),
	("RO", "Rocket"),
	("FR", "Freeze"),
	("PO", "Poison"),
	("GY", "Graveyard"),
	("GB", "Goblin Barrel"),
	("TN", "Tornado"),
	("CL", "Clone"),
	("BB", "Barbarian Barrel"),
	("HE", "Heal"),
	("GN", "Giant Snowball"),
	("TL", "The Log"),
	("MR", "Mirror"),
)

CLAN_RANK_CHOICES = (
	("M", "Member"),
	("E", "Elder"),
	("C", "Co-Leader"),
	("L", "Leader"),
)

def get_filename_extension(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def image_upload_path(instance, filename):
	new_filename = instance.account.slug
	name, ext = get_filename_extension(filename)
	final_filename = '{name}{ext}'.format(name=name, ext=ext)
	return 'accounts/{new_filename}/{final_filename}'.format(
		new_filename=new_filename, 
		final_filename=final_filename
	 )

def main_image_upload_path(instance, filename):
	new_filename = instance.slug
	name, ext = get_filename_extension(filename)
	final_filename = '{name}{ext}'.format(name=name, ext=ext)
	return 'accounts/{new_filename}/{final_filename}'.format(
		new_filename=new_filename, 
		final_filename=final_filename
	 )


class DeckCard(models.Model):
	name = models.CharField(max_length=2, choices=CARD_CHOICES)
	level = models.SmallIntegerField()

	@property
	def friendly_name(self):
		name = self.name
		for n in CARD_CHOICES:
			if n[0] == name:
				return n[1]
		return name
	 

	def __str__(self):
		return "{name} level {level}".format(name=self.friendly_name, level=self.level)


class Account(models.Model):
	slug = models.SlugField(blank=True, null=True, unique=True)

	usd_price = models.DecimalField(decimal_places=2, max_digits=8)

	device = models.CharField(max_length=7, choices=DEVICE_CHOICES)
	sold = models.BooleanField(default=False)
	description = models.CharField(max_length=300)
	img_med = models.ImageField(upload_to=main_image_upload_path, null=True, blank=True)
	img_sml = models.ImageField(upload_to=main_image_upload_path, null=True, blank=True)
	img_feature = models.ImageField(upload_to=main_image_upload_path, null=True, blank=True)

	# account access info
	supercell_account_email = models.EmailField(max_length=255)
	supercell_email_password = models.CharField(max_length=255)

	# account stats
	name = models.CharField(max_length=50)
	name_change = models.BooleanField(default=True)
	king_tower = models.SmallIntegerField()
	gold = models.IntegerField()
	gems = models.IntegerField()
	arena = models.CharField(max_length=2, choices=ARENA_CHOICES)
	trophies = models.SmallIntegerField()
	recommended_decks_link = models.CharField(max_length=250, null=True, blank=True)

	wins = models.IntegerField()
	three_crown_wins = models.IntegerField()
	highest_trophies = models.IntegerField()
	cards_found = models.SmallIntegerField()
	total_donations = models.IntegerField()

	tournament_matches_played = models.SmallIntegerField()
	tournament_cards_won = models.IntegerField()

	clan_name = models.CharField(max_length=50)
	clan_member_rank = models.CharField(max_length=2, choices=CLAN_RANK_CHOICES)
	clan_trophies = models.SmallIntegerField()
	clan_war_day_wins = models.SmallIntegerField()
	clan_war_cards_won = models.IntegerField()
	
	challenge_max_wins = models.SmallIntegerField()
	challenge_cards_won = models.IntegerField()	
	
	deck = models.ManyToManyField(DeckCard, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)

	def __str__(self):
		return "Arena: {arena}, K.T: {king_tower}, Price: {price}".format(
			arena=self.arena, king_tower=self.king_tower, price=self.usd_price
		)

	def get_absolute_url(self):
		return reverse("accounts:detail", kwargs={"slug": self.slug})

	def get_device_readable(self):
		device = self.device
		for d in DEVICE_CHOICES:
			if d[0] == device:
				return d[1]
		return device

	def get_arena_readable(self):
		arena = self.arena
		for a in ARENA_CHOICES:
			if a[0] == arena:
				return a[1]
		return arena

	def get_slug_arena(self):
		arena = self.arena
		for a in ARENA_CHOICES:
			if a[0] == arena:
				return a[1].replace(' ', '-')
		return arena

	def get_clan_member_rank_readable(self):
		rank = self.clan_member_rank
		for r in CLAN_RANK_CHOICES:
			if r[0] == rank:
				return r[1]
		return rank

	def price(self, conversion_rate):
		return Decimal(Decimal(self.usd_price) * Decimal(conversion_rate)
			).quantize(Decimal('.01'), rounding=ROUND_UP)

                
	@property
	def title(self):
		return 'Level {king_tower} in {arena}'.format(king_tower=self.king_tower, 
			arena=self.get_arena_readable())


# Assigns a slug to a model object if its slug field is emtpy, before saving.
def account_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance, 0)

pre_save.connect(account_pre_save_receiver, sender=Account)


class AccountImage(models.Model):
	image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
	description = models.CharField(max_length=100)
	account = models.ForeignKey(Account)

	def __str__(self):
		return "Arena: {arena}, K.T: {king_tower}".format(
			arena=self.account.arena, king_tower=self.account.king_tower
		)




	
