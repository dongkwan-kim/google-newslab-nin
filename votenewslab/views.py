# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from votenewslab.models import VoteRegion, Candidate, Meta
from django.db.models import Q
import json

def to_utf8(thing):
    if type(thing) == type(""):
        return thing.decode("unicode-escape").encode("utf8")

def autocomplete_ajax(request):
    search_text = request.GET.get("search_text")
    result_json_list = []
    reg_adm_list = VoteRegion.objects.filter(Q(election_district__contains = search_text) | Q(admin_region__contains = search_text)).order_by("election_district")
    for reg_adm in reg_adm_list:
        reg_adm_json = {}
        if reg_adm.admin_region.strip() == "avg":
            reg_adm_json["text"] = ", ".join([reg_adm.wide_region.strip(), reg_adm.election_district.strip()])
        else:
            reg_adm_json["text"] = ", ".join([reg_adm.wide_region.strip(), reg_adm.admin_region.strip(), reg_adm.election_district.strip()])
        result_json_list.append(reg_adm_json)
    return to_utf8(json.dumps(result_json_list))

def vote_home(request):
    if request.is_ajax():
        return HttpResponse(autocomplete_ajax(request))

    if request.method == "POST":
        reg_input = request.POST["reg"]
        reg_arr = reg_input.split(", ")
        if len(reg_arr) == 3:
            select_reg = VoteRegion.objects.filter(wide_region=reg_arr[0], admin_region=reg_arr[1], election_district=reg_arr[2])
        elif len(reg_arr) == 2:
            select_reg = VoteRegion.objects.filter(wide_region=reg_arr[0], election_district=reg_arr[1], admin_region="avg")
        else:
            select_reg = VoteRegion.objects.filter(Q(admin_region__contains=reg_input) | Q(election_district__contains=reg_input))
            select_reg_avg = VoteRegion.objects.filter(Q(admin_region="avg") & Q(election_district__contains=reg_input))
        
        if len(select_reg) == 1:
            reg_id = select_reg[0].region_id
        else:
            if len(select_reg_avg) == 1:
                reg_id = select_reg_avg[0].region_id
            elif len(select_reg) > 1:
                big_msg = "너무 많이 검색됩니다!"
                small_msg = "아래 리스트에서 선택해주세요"
                return render(request, "votetemp/sg_error.html", {"big_msg": big_msg, "small_msg": small_msg, "regs_list": select_reg})
            else:
                big_msg = "검색 결과가 없습니다!"
                small_msg = "검색어를 정확하게 입력해주세요"
                return render(request, "votetemp/sg_error.html", {"big_msg": big_msg, "small_msg": small_msg})

        return redirect("/sudogwon413/"+reg_id+"/")
    
    meta = Meta.objects.filter(meta_name="sudogwon")[0]
    return render(request, "votetemp/sg_home.html", {"meta": meta})

def vote_result(request, reg_id):
    vote_region = VoteRegion.objects.filter(region_id=reg_id)[0]
    if float(vote_region.minju_avg) < float(vote_region.sanuri_avg):
        win_region = "새누리당 우세지역입니다"
        party_color = "#F44336"
    elif float(vote_region.minju_avg) == float(vote_region.sanuri_avg):
        win_region = "자료가 없습니다"
        party_color = "#A3A3A3"
    else:
        win_region = "야권 우세지역입니다"
        party_color = "#007CB8"
    
    if vote_region.admin_region != "avg":
        vr_msg = vote_region.wide_region +" "+vote_region.admin_region + "[" + vote_region.election_district + "]"
    else:
        vr_msg = vote_region.wide_region +" "+vote_region.election_district
        
    cand_list = Candidate.objects.filter(cand_region_id=reg_id[:32])
        
    other_ar_list = VoteRegion.objects.filter(wide_region=vote_region.wide_region, election_district__startswith=vote_region.election_district.split("(")[0]).order_by("admin_region")

    meta = Meta.objects.filter(meta_name="sudogwon")[0]
    return render(request, "votetemp/sg_result.html", {"vr_msg": vr_msg, "vr": vote_region, "wr": win_region, "pc": party_color, "cl": cand_list, "oal": other_ar_list, "meta": meta})
