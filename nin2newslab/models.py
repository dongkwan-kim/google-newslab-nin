# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from math import ceil
import json
from nin2newslab.class_nin2io import ThumbnailGrid, RadioMatrix, SelectMatrix, FormHorizontal

# for debug
def printv(s):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(s)
    print("_____________________________________")

def to_utf8(thing):
    return thing.decode("unicode-escape").encode("utf8")


class Modal(models.Model):
    name = models.CharField(max_length=10)
    modal_id = models.CharField(max_length=15)
    modal_title = models.CharField(max_length=25)
    modal_name = models.CharField(max_length=10)
    modal_body = models.TextField()

# NinX2
class UserChoice(models.Model):
    date = models.CharField(max_length=30)
    user_id = models.CharField(max_length=20)
    name = models.CharField(max_length=10) 
    chosen_json = models.TextField(default="{}")
    user_json = models.TextField(default="{}")

class Nin2Content(models.Model):
    n2c_title = models.CharField(max_length=20)
    n2c_explain = models.TextField(default = "")
    n2c_path = models.CharField(max_length=10)

class Problem(models.Model):
    name = models.CharField(max_length=10) 
    idx = models.IntegerField()
    html_type = models.CharField(max_length=20)
    problem_str = models.TextField(default="")
    explain_str = models.TextField(default="")
    choice_list = models.TextField(default="")

    def get_name(self):
        return self.name

    def get_idx_str(self):
       	return str(self.idx)
    
    def get_html_type(self):
        return self.html_type

    def get_problem(self):
       	return self.problem_str

    def get_explain(self):
       	return self.explain_str

    def get_choice_list(self):
        its_type = self.get_html_type()
        divided_list = self.choice_list.strip().split("\n")
        # vertical-text: line\n
        if(its_type == "vertical-text"):
       	    return divided_list
        # thumnail-grid: label/explain/value/ment\n
        elif(its_type == "thumbnail-grid"):
            return [ThumbnailGrid(line.strip()) for line in divided_list]
        # radio-matrix: label/radio1/radio2/...\n
        elif(its_type == "radio-matrix"):
            return [RadioMatrix(line.strip()) for line in divided_list]
        # select-matrix: label/select1/select2/...\n
        elif(its_type == "select-matrix"):
            return [SelectMatrix(line.strip()) for line in divided_list]
        # form-horizontal: label/type/name/id/placeholder
        elif(its_type == "form-horizontal"):
            return [FormHorizontal(line.strip()) for line in divided_list]

class Nin2Result(models.Model):
    name = models.CharField(max_length=10)
    title = models.CharField(max_length=20)
    card_content = models.TextField()
    card_reveal_title = models.CharField(max_length=30)
    card_reveal_content = models.TextField()
    link_url = models.TextField()

class Home(models.Model):
    name = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    explain = models.TextField(default="")
    input_type = models.TextField(default="label/type/name/id/placeholder")

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title

    def get_explain(self):
        return self.explain

    def get_input(self):
        # label/type/name/id/placeholder
        return [FormHorizontal(line) for line in self.input_type.strip().split("\n")]

class Univ(models.Model):
    name = models.CharField(max_length = 25)
    soc = models.IntegerField()
    sci = models.IntegerField()
    art = models.IntegerField()
    eng = models.IntegerField()
    med = models.IntegerField()
    
    def get_tut_str(self):
        tut_list = [self.soc, self.sci, self.art, self.eng, self.med]
        return ",".join([str(x) for x in tut_list])

# Bofu Network
class BofuNode(models.Model):
    node_id = models.IntegerField()
    node_value = models.IntegerField()
    node_label = models.CharField(max_length=7)
    node_pos = models.CharField(max_length=4)
    node_json = models.TextField()

    def export_json(self):
        return node_json

class BofuEdge(models.Model):
    edge_from = models.IntegerField()
    edge_to = models.IntegerField()
    edge_value = models.IntegerField()
    edge_json = models.TextField()

    def export_json(self):
        return edge_json

class BofuInterview(models.Model):
    intv_id = models.IntegerField(default=0)
    intv_key = models.CharField(max_length=15)
    intv_name = models.CharField(max_length=30)
    intv_quote = models.TextField()
    intv_icon = models.CharField(max_length=5)

class Meta(models.Model):
    meta_name = models.CharField(max_length=10)
    meta_title = models.CharField(max_length=20)
    meta_type = models.CharField(max_length=15)
    meta_url = models.TextField()
    meta_description = models.TextField()
    meta_image = models.TextField()
