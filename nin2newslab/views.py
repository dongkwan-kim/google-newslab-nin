# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from nin2newslab.models import Univ, Modal, UserChoice, Nin2Content, Problem, Nin2Result, Home, Meta
from nin2newslab.models import BofuNode, BofuEdge, BofuInterview
from django.db.models import Q

import datetime
import random
import json

from math import ceil
# for debug
def printv(s):
    print("")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(s)
    print("_____________________________________")
    print("")

def to_utf8(thing):
    if type(thing) == type(""):
        return thing.decode("unicode-escape").encode("utf8")

def make_id(length):
    ret_str = ""
    for i in range(length):
        ret_str += str(random.randint(0,9))
    return ret_str

# calc 
def calc_home(request):
    modals = Modal.objects.filter(name="calc")
    meta = Meta.objects.filter(meta_name="calc")[0]
    return render(request, "nin2temp/rcalc/calc_home.html", {"modals": modals, "meta": meta})

# choice
def get_price_4_pay(chosen_dict, choice_name):
    price_4_pay = 0
    if choice_name == "tuition":
        data_0 = chosen_dict["0"].split(",")
        price_4_pay = int(data_0[0]) * int(data_0[1]) * 10000

    elif choice_name == "europe":
        data_0 = chosen_dict["0"].split(",")
        data_1 = chosen_dict["1"].split(",")

        choice_list_0 = Problem.objects.filter(name=choice_name, idx=0)[0].get_choice_list()
        choice_list_1 = Problem.objects.filter(name=choice_name, idx=1)[0].get_choice_list()

        idx_board = dict([("c"+str(i+1), i) for i in range(max(len(choice_list_0), len(choice_list_1)))])

        for fidx in range(len(data_1)):
            index_0 = idx_board[data_0[fidx]]
            index_1 = idx_board[data_1[fidx]]
            its_price = int(choice_list_0[index_0].value)
            its_day = int(choice_list_1[0].select_list[index_1])
            price_4_pay += its_price * its_day
        price_4_pay += 900000

    elif choice_name == "date":
        data_0 = chosen_dict["0"].split(",")
        data_1 = chosen_dict["1"].split(",")

        choice_list_0 = Problem.objects.filter(name=choice_name, idx=0)[0].get_choice_list()

        idx_board = dict([("c"+str(i+1), i) for i in range(len(choice_list_0))])
        div_board = dict([("c"+str(i+1), 1-i/2.0) for i in range(3)])

        for fidx in range(len(data_1)):
            index_0 = idx_board[data_0[fidx]]
            its_price = int(choice_list_0[index_0].value)
            div_rate = div_board[data_1[fidx]]
            price_4_pay += its_price * div_rate

    elif choice_name == "apple":
        data_0 = chosen_dict["0"].split(",")
        
        choice_list_0 = Problem.objects.filter(name=choice_name, idx=0)[0].get_choice_list()
        idx_board = dict([("c"+str(i+1), i) for i in range(len(choice_list_0))])
        
        for fidx in range(len(data_0)):
            index_0 = idx_board[data_0[fidx]]
            its_price = int(choice_list_0[index_0].value)
            price_4_pay += its_price
    return price_4_pay

def get_choice_from_POST(post_query_dict):
    temp_list = []
    key_list = post_query_dict.keys()
    key_list.sort()
    for reqkey in key_list:
        if "choice" in reqkey:
            p_list = post_query_dict.getlist(reqkey)
            if len(p_list) == 1:
                temp_list.append(post_query_dict[reqkey])
            else:
                temp_list.append(",".join(p_list))
    return ",".join(temp_list)

def get_render_html(html_type):
    return "nin2temp/new_choice/choice_question_"+html_type.replace("-", "_")+".html"

def get_prev_choice(choice_name, prev_choice_list, p_idx):
    prev_problem = Problem.objects.filter(name=choice_name, idx=p_idx)[0]
    choice_list = prev_problem.get_choice_list()
    idx_board = dict([("c"+str(i+1), i) for i in range(len(choice_list))])
    chosen_list = []
    for choice in prev_choice_list:
        index = idx_board[choice]
        chosen_list.append(choice_list[index])
    return chosen_list

def choice_main(request):
    n2c_list = Nin2Content.objects.all()
    return render(request, "nin2temp/choice/choice_main.html", {"n2c": n2c_list})

def choice_home(request, choice_name):
    if request.method == "POST":
        # welcome, new user!
        user_json_data = to_utf8(json.dumps(request.POST))
        date_data = datetime.datetime.now()
        id_data = make_id(16)
        new_user = UserChoice(name=choice_name, user_json=user_json_data, date=date_data, user_id=id_data)
        new_user.save()

        redir_url = "../"+id_data+"/"
        return redirect(redir_url)
    else:
        meta = Meta.objects.filter(meta_name=choice_name)[0]
        home_content = Home.objects.filter(name=choice_name)[0]
        return render(request, "nin2temp/new_choice/choice_home.html", {"meta":meta, 'home': home_content, 'name': choice_name})

def search_univ_for_ajax(request):
    search_text = request.GET.get("search_text")
    if search_text is not None and search_text != u"":
        univ_list = Univ.objects.filter(name__contains = search_text)
        univ_json_list = []
        for univ in univ_list:
            univ_json = {}
            univ_json["name"] = univ.name
            univ_json["tut"] = univ.get_tut_str()
            univ_json_list.append(univ_json)
        return to_utf8(json.dumps(univ_json_list))
    else:
        return "{}"

def choice_nump(request, choice_name, id_data):
    # univ search for tuition
    if request.is_ajax():
        return HttpResponse(search_univ_for_ajax(request))
    
    id_list = UserChoice.objects.filter(name=choice_name, user_id=id_data)
    your_id = id_list[len(id_list) - 1]
    
    # not first problem
    if request.method == "POST":
        chosen_dict = json.loads(your_id.chosen_json)
        chosen_len = len(chosen_dict)
        if int(request.POST["pidx"]) < chosen_len:
            chosen_len = int(request.POST["pidx"])
        chosen_dict[str(chosen_len)] = get_choice_from_POST(request.POST)
        your_id.chosen_json = to_utf8(json.dumps(chosen_dict))
        your_id.save()
        
        next_num = chosen_len + 1
        # last problem
        if next_num == len(Problem.objects.filter(name=choice_name)):
            redir_url = "../result/"+str(id_data) + "/"
            return redirect(redir_url)
        
        # not first and not last
        else:
            problem = Problem.objects.filter(name=choice_name, idx=next_num)[0]
            render_html = get_render_html(problem.get_html_type())
            if choice_name == "europe" or choice_name =="date":
                prev_choice_list = chosen_dict[str(chosen_len)].split(",")
                prev_choice_obj = get_prev_choice(choice_name, prev_choice_list, chosen_len)
                return render(request, render_html, {"problem": problem, "name": choice_name, "prev_choice_list": prev_choice_obj})
            else:
                return render(request, render_html, {"problem": problem, "name": choice_name})
    # first problem
    else:
        problem = Problem.objects.filter(name=choice_name, idx=0)[0]
        render_html = get_render_html(problem.get_html_type())
        if choice_name == "tuition":
            univ_list = Univ.objects.all()
            return render(request, render_html, {"problem": problem, "name": choice_name, "univ_list": univ_list})
        else:
            return render(request, render_html, {"problem": problem, "name": choice_name})

def choice_result(request, choice_name, id_data):
    id_list = UserChoice.objects.filter(name=choice_name, user_id=id_data)
    your_id = id_list[len(id_list) - 1]
    chosen_dict = json.loads(your_id.chosen_json)
    hour_pay = int(json.loads(your_id.user_json)["won"])
    price_4_pay = get_price_4_pay(chosen_dict, choice_name)
    result = Nin2Result.objects.filter(name=choice_name)[0]
    meta = Meta.objects.filter(meta_name=choice_name)[0]
    return render(request, "nin2temp/new_choice/choice_result_nin2pay.html", {"result": result, "price": price_4_pay, "hour_pay": hour_pay, "meta": meta})

# network bofu
class Network():
    def __init__(self, v, e):
        self.v = v;
        self.e = e;

def make_random_set(num, scale):
    random_set = []
    black_list = [18, 14, 9, 20, 17]
    while True:
        r_num = random.randrange(1, scale+1)
        if r_num not in random_set and r_num not in black_list:
            random_set.append(r_num)
        if len(random_set) == num:
            break
    return random_set

def splice_quote(quote, keyword, length):
    if keyword in quote:
        start = quote.find(keyword)
        return "..."+quote[start:min(start+length, len(quote))]+"..."
    else:
        return "..."+quote[:length]+"..."

def make_graph(r_set=None, num_of_pe=45, enter_type="web"):
    if r_set == None:
        if enter_type == "web":
            r_set = make_random_set(20, 99)
        else:
            r_set = make_random_set(12, 99)
        is_random_graph = True
    else:
        is_random_graph = False
    
    node_list = []
    edge_list = []
    
    # append nodes by r_set
    exist_nodes = []
    for r_num in r_set:
        s_node = BofuNode.objects.filter(node_id=r_num)[0]
        exist_nodes.append(s_node)
    
    # append edge's value and sort
    edge_val_list = []
    exist_edges = []
    cross_list = [(f, t) for f in r_set for t in r_set if f!=t]
    for (f, t) in cross_list:
        s_edge = BofuEdge.objects.filter(Q(edge_from=f) & Q(edge_to=t))
        if len(s_edge) > 0:
            edge_val_list.append(s_edge[0].edge_value)
            exist_edges.append(s_edge[0])
    edge_val_list.sort(reverse=True)
    
    # append edges whose value is higher than standard
    num_of_pe = min(num_of_pe, len(edge_val_list)-1)
    if enter_type == "web":
        for e in exist_edges:
            if e.edge_value > edge_val_list[num_of_pe]:
                edge_list.append(e)
    else: #mobile
        for e in exist_edges:
            if e.edge_value > edge_val_list[30]:
                edge_list.append(e)
    
    # del alone-node
    for n in exist_nodes:
        is_alone = True
        for e in edge_list:
            if n.node_id == e.edge_from or n.node_id == e.edge_to:
                is_alone = False
                break
        if is_random_graph == False or is_alone == False:
            node_list.append(n.node_json)

    # make edge obj to json
    edge_list = [e.edge_json for e in edge_list]
    
    return Network(node_list, edge_list)

def refresh_ajax(enter_type):
    new_rg = make_graph(enter_type=enter_type)
    network_json = {}
    network_json["node"] = new_rg.v
    network_json["edge"] = new_rg.e
    return to_utf8(json.dumps(network_json))

def interview_ajax(request):
    node_label = request.GET.get("node_label")
    node_pos = request.GET.get("node_pos")
    node_key = node_label+"/"+node_pos
    intv_list = BofuInterview.objects.filter(intv_key=node_key)
    intv_json_list = []
    for intv in intv_list:
        intv_json = {}
        intv_json["label"] = node_label
        intv_json["name"] = intv.intv_name
        intv_json["quote"] = intv.intv_quote
        intv_json["icon"] = intv.intv_icon
        intv_json_list.append(intv_json)
    return to_utf8(json.dumps(intv_json_list))

def autocomplete_ajax(request):
    node_id_list = request.GET.getlist("node_id_list[]")
    search_text = request.GET.get("search_text")
    intv_json_list = [] 
    for node_id in node_id_list:
        intv_list = BofuInterview.objects.filter(intv_id=node_id, intv_quote__contains = search_text)
        for intv in intv_list:
            intv_json = {}
            intv_json["node_id"] = node_id
            intv_json["quote"] = splice_quote(intv.intv_quote, search_text, 20)
            intv_json_list.append(intv_json)
            if len(intv_json_list) > 6:
                break
        if len(intv_json_list) > 6:
            break
    return to_utf8(json.dumps(intv_json_list))

def choose_set_ajax(request, enter_type):
    step = request.GET.get("step")
    if step == "1":
        node_list = BofuNode.objects.all()
        node_json_list = []
        for node in node_list:
            node_json = {}
            node_json["node_id"] = node.node_id
            node_json["node_label"] = node.node_label
            node_json_list.append(node_json)
        return to_utf8(json.dumps(node_json_list))
    if step == "2":
        c_set = request.GET.getlist("chosen_node_id_list[]")
        new_cg = make_graph(r_set=c_set, enter_type=enter_type)
        network_json = {}
        network_json["node"] = new_cg.v
        network_json["edge"] = new_cg.e
        return to_utf8(json.dumps(network_json))

    return "done, but not implemented"

def network(request, enter_type):
    
    if request.is_ajax():
        ajax_name = request.GET.get("ajax_name")
        if ajax_name == "refresh":
            return HttpResponse(refresh_ajax(enter_type))
        elif ajax_name == "interview":
            return HttpResponse(interview_ajax(request))
        elif ajax_name == "autocomplete":
            return HttpResponse(autocomplete_ajax(request))
        elif ajax_name == "choose_set":
            return HttpResponse(choose_set_ajax(request, enter_type))
    
    rg = make_graph(enter_type=enter_type)
    node_list = rg.v
    edge_list = rg.e
    
    meta = Meta.objects.filter(meta_name="albawords")[0]
    if enter_type == "web":
        return render(request, "network/network-server.html", {"meta":meta, "nodes": node_list, "edges": edge_list})
    else:
        # maybe mobile
        return render(request, "network/network-mobile.html", {"meta":meta, "nodes": node_list, "edges": edge_list})

def network_web(request):
    return network(request, "web")

def network_mobile(request):
    return network(request, "mobile")
