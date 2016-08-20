/* help function with calc */

// chosen_days_arr: array of boolean type: sun~sat
function getDayStatOfMonth(year, month, chosen_days_arr){
	var cnt_day = 0;
	var cnt_end = 0;
	var day_range = (new Date(year, month, "0")).getDate();
	for(var didx = 1; didx <= day_range; didx++){
		var temp_day = (new Date(year, month-1, didx)).getDay();
		if(chosen_days_arr[temp_day]){
			if(temp_day >= 1 && temp_day <= 5){
				cnt_day++;
			} else {
				cnt_end++;
			}
		}
	}
	return [cnt_day, cnt_end];
}

function get_chosen_days(){
	var w_days = 0;
	var w_ends = 0;
	var chosen_days = new Array();
	week_arr = document.getElementsByClassName("btn-week");	
	for(var index = 0; index < week_arr.length; index++){
		if(week_arr[index].classList.contains("active")){
			chosen_days.push(true);
		} else {
			chosen_days.push(false);
		}
	}
	chosen_days.unshift(chosen_days.pop());
	return chosen_days;
}

function get_readable_won(won_value){
	if(won_value%10000 == 0 && won_value/10000 == 0){
		return "0 원"
	} else if (Math.floor(won_value/10000) == 0) {
		return won_value%10000 + "원" 
	} else if (won_value%10000 == 0){
		return Math.floor(won_value/10000) + "만 원" 
	} else {
		return Math.floor(won_value/10000) + "만 " + won_value%10000 + "원" 
	}
}

function get_readable_tr(tr, mode){
	// mode 1: 주간; mode 2: 야간
	var start_time = parseInt(tr[0]);
	var end_time = parseInt(tr[1]);
	if(mode == 1){
		return start_time + "시 ~ " + end_time + "시";
	} else {
		if(end_time >= 12 && start_time < 12){
			return (start_time+12)%24 + "시 ~ 다음 " + (end_time+12)%24 + "시";
		} else {
			return (start_time+12)%24 + "시 ~ " + (end_time+12)%24 + "시";
		}
	}
}

function get_time_from_tr(tr, mode){
	// mode 1: 00~24; mode 2: 12~24~00~12
	// 야간: 22~06
	var start_time = parseInt(tr[0]);
	var end_time = parseInt(tr[1]);
	
	var daytime = 0;
	var nighttime = 0;
	var total_time = end_time - start_time;
	if(mode == 1){
		if(end_time <= 6 || start_time >= 22){
			nighttime = end_time - start_time;
		} else {
			if (start_time <= 6) {
				nighttime += 6 - start_time;
			} 
			if (end_time >= 22){
				nighttime += end_time - 22;
			}
		}
	} else {
		if(end_time <= 10 || start_time >= 18){
			nighttime = 0;
		} else if (start_time <= 10 && end_time >= 18){
			nighttime = 18 - 10;
		} else if(end_time >= 18){
			nighttime = 18 - start_time;
		} else if(start_time <= 10){
			nighttime = end_time - 10;
		} else {
			nighttime = end_time - start_time;
		}
	}
	daytime = total_time - nighttime;
	return [daytime, nighttime];
}

function get_each_time(timerange_arr, date_state_arr){
	var daytime = timerange_arr[0];
	var nighttime = timerange_arr[1];
	var w_days = date_state_arr[0];
	var w_ends = date_state_arr[1];


	var time_arr = new Array();
	time_arr[1] = daytime * w_days;
	time_arr[2] = daytime * w_ends;
	time_arr[3] = nighttime * w_days;
	time_arr[4] = nighttime * w_ends;
	time_arr[0] = time_arr[1] + time_arr[2] + time_arr[3] + time_arr[4];
	
	return time_arr;
}

function get_yookgab(price, timerange_arr, date_state_arr, ecb_arr){
	var daytime = timerange_arr[0];
	var nighttime = timerange_arr[1];
	var w_days = date_state_arr[0];
	var w_ends = date_state_arr[1];
	
	var night_factor = 1.5;
	var tax_insur_factor = 0.08344;
	var tax_incom_factor = 0.033;


	/*
	 * I need Logic
	 * */
	
	
	
	var yg_arr = new Array();
	yg_arr[1] = price * daytime * w_days;
	yg_arr[2] = price * daytime * w_ends;
	yg_arr[3] = 0; //주휴수당
	yg_arr[0] = yg_arr[1] + yg_arr[2] + yg_arr[3];
	
	return yg_arr;
}

function modify_yg_table(price, tr_arr, date_state_arr, ecb_arr){
	var yg_arr = get_yookgab(price, tr_arr, date_state_arr, ecb_arr);
	$('#result').text(get_readable_won(yg_arr[0]));
	$('#dt').text(get_readable_won(yg_arr[1]));
	$('#nt').text(get_readable_won(yg_arr[2]));
	$("#wkhol").text("구현할거임"/*get_readable_won(yg_arr[3])*/);
}

function toggle_alert(flag){
	var msg = "";
	if(flag){
		msg = " 시간 범위를 00:00부터 24:00까지로 변경했습니다";
	} else {
		msg = " 시간 범위를 12:00부터 다음날 12:00까지로 변경했습니다";
	}
	Materialize.toast(msg, 2500);
}

function get_prev_ym(year, month){
	if(month == 1){
		month = 12;
		year -= 1;
	} else {
		month -= 1;
	}
	return [year, month];
}

function get_next_ym(year, month){
	if(month == 12){
		month = 1;
		year += 1;
	} else {
		month += 1;
	}
	return [year, month];
}

function get_pr(){
	return parseInt($("#seegeup").val());
}

function get_tr(){
	var data_arr =  tr_slider.noUiSlider.get();
	return [parseInt(data_arr[0]), parseInt(data_arr[1])];
}

$(document).ready(function(){
	var today = new Date();
	var c_year = today.getFullYear();
	var c_month = today.getMonth() + 1;
	var date_stat =  getDayStatOfMonth(c_year, c_month, get_chosen_days());
	var tr_mode = 1;
	var price = get_pr();
	var timerange = get_tr();
	var ecb_arr = [false, false];
	var is_there= false;
	
	$('#view-seegeup').text(get_readable_won(price));
	$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
	$('#modal-year-month, #year-month').text(c_year+"년 "+c_month+"월");
	modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);

	$("#seegeup").change(function(){
		});
	
	var is_first = true;
	$("#refr-seegeup").click(function(){
		$("#seegeup").val(6030);
		price = get_pr();
		$('#view-seegeup').text(get_readable_won(price));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
		is_first = true;
	});
	$(".sg-btn").click(function(){
		var idx = $(".sg-btn").index(this);
		var rv = Math.pow(10, 4-idx);
		if(is_first){
			$("#seegeup").val(rv);
			is_first = false;
		} else {
			$("#seegeup").val(parseInt($("#seegeup").val())+rv);
		}
		price = get_pr();
		$('#view-seegeup').text(get_readable_won(price));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
	});

	$(".extra-cond").click(function(){
		price = get_pr();
		timerange = get_tr();
	
		var idx = $(".extra-cond").index(this);
		ecb_arr[idx] = !ecb_arr[idx];
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
	});

	tr_slider.noUiSlider.on("update", function(){
		//price = get_pr();
		timerange = get_tr();

		$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
	});

	$(".date-mover").click(function(){
		var idx = $(".date-mover").index(this);
		var new_ym;
		if(idx == 0){
			new_ym = get_prev_ym(c_year, c_month);
		} else {
			new_ym = get_next_ym(c_year, c_month);
		}
		c_year = new_ym[0];
		c_month = new_ym[1];
		date_stat = getDayStatOfMonth(c_year, c_month, get_chosen_days());
		$('#modal-year-month, #year-month').text(c_year+"년 "+c_month+"월");
	
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
	});
	
	$(".btn-week").click(function() {
		if($(this).hasClass("active")){
			$(this).removeClass("active");
		} else {
			$(this).addClass("active");
		}
		price = get_pr();
		timerange = get_tr();
		var idx = ($(".btn-week").index(this) + 1)%7;
		var chosen_days_arr = get_chosen_days();
		date_stat =  getDayStatOfMonth(c_year, c_month, chosen_days_arr);
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
	});	

	$('#chan-timerange').click(function() {
		/* alert */
		toggle_alert(is_there);
		is_there = !is_there;
	
		/* modify yg */
		tr_mode = 3 - tr_mode; // 1<->2
		$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
		
		/* icon change*/
		icon_arr = ["wb_sunny", "brightness_3"];
		$("#chan-timerange").text(icon_arr[tr_mode-1]);
	});

	$("tr.modal-trigger").click(function(){
		var idx = $("tr.modal-trigger").index(this);
		var this_id = $(this).attr("id");
		var modal_id = this_id.replace("-trigger", "");
		var time_arr = get_each_time(get_time_from_tr(timerange, tr_mode), date_stat);
		$("#"+modal_id+"-hour").text(time_arr[(idx+1)%5]);
		if(~this_id.indexOf("we")){
			// weekends
			$("#"+modal_id+"-day").text(date_stat[1]);
		} else {
			// weekdays
			$("#"+modal_id+"-day").text(date_stat[0]);
		}
		$("#"+modal_id).openModal();
	});
	
	$("p.modal-trigger").click(function(){
		$("#modal-date-mover").openModal();
	});
});
