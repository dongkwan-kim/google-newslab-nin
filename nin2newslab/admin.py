# -*- coding: utf-8 -*-
from django.contrib import admin
from nin2newslab.models import Univ, Modal, UserChoice, Nin2Content, Problem, Nin2Result, Home, Meta
from nin2newslab.models import BofuNode, BofuEdge, BofuInterview

# Register your models here.

class ModalAdmin(admin.ModelAdmin):
    list_display = ("name", "modal_id", "modal_title", "modal_name",  "modal_body")

class UserChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'date', 'chosen_json', "user_json")
    list_filter = ("name",)

class Nin2ContentAdmin(admin.ModelAdmin):
    list_display = ('n2c_title', 'n2c_explain', 'n2c_path')

class ProblemAdmin(admin.ModelAdmin):
    list_display = ("name", "idx", "html_type", "problem_str", "explain_str", "choice_list")
    list_filter = ("name", "html_type")

class Nin2ResultAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "card_content", "card_reveal_title", "card_reveal_content", "link_url")
    list_filter = ("name",)

class HomeAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "explain", "input_type")
    list_filter = ("name",)

class UnivAdmin(admin.ModelAdmin):
    list_display = ("name", "soc", "sci", "art", "eng", "med")

class BofuNodeAdmin(admin.ModelAdmin):
    list_display = ("node_id", "node_value", "node_label", "node_pos", "node_json")

class BofuEdgeAdmin(admin.ModelAdmin):
    list_display = ("edge_from", "edge_to", "edge_value", "edge_json")

class BofuInterviewAdmin(admin.ModelAdmin):
    list_display = ("intv_id", "intv_key", "intv_name", "intv_quote", "intv_icon")

class MetaAdmin(admin.ModelAdmin):
    list_display = ("meta_name", "meta_title", "meta_type", "meta_url", "meta_description", "meta_image")

admin.site.register(Modal, ModalAdmin)
admin.site.register(UserChoice, UserChoiceAdmin)
admin.site.register(Nin2Content, Nin2ContentAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Nin2Result, Nin2ResultAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Univ, UnivAdmin)
admin.site.register(BofuNode, BofuNodeAdmin)
admin.site.register(BofuEdge, BofuEdgeAdmin)
admin.site.register(BofuInterview, BofuInterviewAdmin)
admin.site.register(Meta, MetaAdmin)
