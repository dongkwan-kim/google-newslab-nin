# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from nin2newslab.models import Univ, Modal, UserChoice, Nin2Content, Problem, Nin2Result, Home
from nin2newslab.models import BofuNode, BofuEdge, BofuInterview
from votenewslab.models import Candidate, VoteRegion
import md5
# Create your views here.

# for debug
def printv(s):
    print("")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(s)
    print("_____________________________________")
    print("")


def front(request):
    return render(request, 'front.html')

def contact(request):
    return render(request, "contact.html")

def test(request):
    
    save_p_list()
    save_reg_list()
    
    #clear_graph()
    #save_graph()
    #save_intv()
    return render(request, "test.html")
    
    choice_name = "tuition"
    result = Nin2Result.objects.filter(name=choice_name)[0]
    price_4_pay = 700000
    hour_pay = 6030
    return render(request, "nin2temp/new_choice/choice_result_nin2pay.html", {"result": result, "price": price_4_pay, "hour_pay": hour_pay})
        
def network(request):
    return render(request, "network/network-local.html")

def save_univ():
    for line in open("tuition_stat_noh.txt", "r"):
        line_arr = [emt.strip() for emt in line.split("\t")]
        for idx in range(len(line_arr)):
            try:
                line_arr[idx] = int(int(line_arr[idx])/20)
            except:
                line_arr[idx] = line_arr[idx].replace("_", "")
        print(line_arr)
        new_univ = Univ(name=line_arr[0], avg=line_arr[1], soc=line_arr[2], sci=line_arr[3], art=line_arr[4], eng=line_arr[5], med=line_arr[6])
        new_univ.save()

def clear_graph():
    node_list = BofuNode.objects.all()
    for node in node_list:
        node.delete()
    edge_list = BofuEdge.objects.all()
    for edge in edge_list:
        edge.delete()

def save_graph():
    flag = ""

    node_list = []
    edge_list = []
    node_idx = 1
    edge_idx = 1

    wfdic = {}
    for line in open("wordfreq.txt", "r"):
        if "start" in line:
            continue
        arr = line.split("\t")
        wfdic[arr[3].strip()] = int(arr[0])

    n = 105
    for line in open("coocc.txt", "r"):
        if "LABEL" in line:
            flag = "LABEL"
            continue
        elif "DATA" in line:
            flag = "DATA"
            continue

        if flag == "":
            pass
        elif flag == "LABEL":
            printv(line)
            word = line.split("쫂")[0].strip()
            pos = line.split("쫂")[1].strip()
            node_str = "{'id': "+ str(node_idx)+\
                       ", 'size': "+str(wfdic[line.strip()])+\
                       ", 'value': "+str(wfdic[line.strip()])+\
                       ", 'label': '"+word+\
                       "', 'color': {'border': '#8d827a', 'background': '#d1c5bf', 'highlight': {'border': '#ffffff', 'background': '#eb4343'}}"\
                       ", 'pos': '"+pos+\
                       "'}"
            if len(node_list) < n:
                new_node = BofuNode(node_id=node_idx, node_value=wfdic[line.strip()], node_label=word, node_pos=pos, node_json=node_str)
                new_node.save()
            node_idx += 1
        elif flag == "DATA":
            # {from: 2, to: 8, value: 3, title: '3 emails per week'}
            row = line.strip().split(" ")[edge_idx:n]
            if edge_idx < n:
                for col_idx in range(len(row)):
                    if int(row[col_idx]) > 0:
			edge_str = "{'from': "+str(edge_idx)+\
                                   ", 'to': "+str(edge_idx+col_idx+1)+\
                                   ", 'value': "+str(row[col_idx])+\
                                   ", 'color': { 'color': '#8d827a', 'highlight': '#eb4343'}"\
                                   +"}"
                        new_edge = BofuEdge(edge_from=edge_idx, edge_to=(edge_idx+col_idx+1), edge_value=row[col_idx], edge_json=edge_str)
                        new_edge.save()
            edge_idx += 1

def save_intv():
    intlist = BofuInterview.objects.all()
    for i in intlist:
        i.delete()
    
    int_dict = {}
    for line in open("interview.txt", "r"):
        if "/" in line and "." in line:
            line_arr = line.split()
            for emt in line_arr:
                if "/" in emt:
                    flag = emt
                    int_dict[flag] = []
        if "-" in line:
            line = line.strip().replace("-", "")
            line_arr = line.split("(")
            sen = "(".join(line_arr[:-1]).strip()
            per = line_arr[-1].replace(")", "").strip().replace(",", ", ")
            int_dict[flag].append([sen, per])
    
    for (k, v) in int_dict.items():
        label = k.split("/")[0]
        pos = k.split("/")[1]
        node_id = BofuNode.objects.filter(node_label=label, node_pos=pos)
        if len(node_id) != 0:
            node_id = node_id[0].node_id
        else:
            node_id = -1
        for [s, p] in v:
            if "남" in p:
                icon = "/media/img/favicon/icon1.png"
            else:
                icon = "/media/img/favicon/icon2.png"
            new_int = BofuInterview(intv_id=node_id, intv_key=k, intv_name=p, intv_quote=s, intv_icon=icon)
            new_int.save()

def save_p_list():
    p_list = Candidate.objects.all()
    for p in p_list:
        p.delete()
    
    party_color_dict = {"새누리": "#F44336", "더민주": "#007CB8", "국민의당": "#6B9D30", "정의당": "#FFCA08"}
    
    for line in open("p_list(utf8).txt", "r"):
        if "#" in line:
            continue
        arr = line.split("\t")
        
        cand_name = arr[4]
        try:
            cand_party_color = party_color_dict[arr[2]]
        except:
            cand_party_color = "#A3A3A3"
        
        s = arr[0].replace("경기", "경기도").replace(" ", "")
        cand_region_id = md5.md5(s).hexdigest()

        cand_profile = ", ".join([arr[2], arr[5], arr[6], arr[7]])
        cand_id = arr[3]
        cand_number = int(arr[1])
        new_cand = Candidate(cand_name=cand_name, cand_number=cand_number, cand_party_color=cand_party_color, cand_region_id=cand_region_id, cand_profile=cand_profile, cand_id=cand_id)
        new_cand.save()

def save_reg_list():
    reg_list = VoteRegion.objects.all()
    for r in reg_list:
        r.delete()

    for line in open("fin_reg_list(utf8).txt", "r") :
        if "#" in line:
            continue
        arr = line.split("\t")
        
        for idx in range(len(arr)):
            arr[idx] = arr[idx].strip()

        wide_region = arr[0]
        election_district = arr[1]
        if arr[2] == "":
            admin_region = "avg"
        else:
            admin_region = arr[2]
        for idx in range(3, 12):
            try:
                arr[idx] = float(arr[idx])
            except:
                arr[idx] = 0.0
        minju_trg = arr[3]
        minju_avg = arr[4]
        minju_act = arr[5]
        minju_pas = arr[6]
        third_val = arr[7]
        sanuri_trg = arr[11]
        sanuri_avg = arr[10]
        sanuri_act = arr[9]
        sanuri_pas = arr[8]
        
        s1 = md5.md5(wide_region + election_district.split("(")[0]).hexdigest()
        s2 = md5.md5(admin_region).hexdigest()
        region_id = s1+s2


        new_reg = VoteRegion(region_id=region_id, wide_region=wide_region, election_district=election_district, admin_region=admin_region, minju_trg=minju_trg, minju_avg=minju_avg,  minju_act=minju_act, minju_pas=minju_pas, third_val=third_val, sanuri_trg=sanuri_trg, sanuri_avg=sanuri_avg, sanuri_act=sanuri_act, sanuri_pas=sanuri_pas)
        new_reg.save()
