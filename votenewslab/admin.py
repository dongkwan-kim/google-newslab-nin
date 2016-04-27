# -*- coding: utf-8 -*-
from django.contrib import admin
from votenewslab.models import VoteRegion, Candidate, Meta

class VoteRegionAdmin(admin.ModelAdmin):
    list_display = ("region_id", "wide_region", "election_district", "admin_region", "minju_trg", "minju_avg", "minju_act", "minju_pas", "third_val", "sanuri_trg", "sanuri_avg", "sanuri_act", "sanuri_pas")

class CandidateAdmin(admin.ModelAdmin):
    list_display = ("cand_name", "cand_number", "cand_party_color", "cand_region_id", "cand_profile", "cand_id")

class MetaAdmin(admin.ModelAdmin):
    list_display = ("meta_name", "meta_title", "meta_type", "meta_url", "meta_description", "meta_image")


admin.site.register(VoteRegion, VoteRegionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Meta, MetaAdmin)
