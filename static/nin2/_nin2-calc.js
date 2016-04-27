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

function get_date_state(){
	var w_days = 0;
	var w_ends = 0;
	week_arr = document.getElementsByClassName("btn-week");	
	for(var index = 0; index < week_arr.length; index++){
		if(week_arr[index].classList.contains("active")){
			if(week_arr[index].classList.contains("btn-weekends")){
				w_ends++;
			} else {
				w_days++;
			}
		}
	}
	// 주일숫자, 주말숫자
	return [w_days, w_ends];
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
	tr = (tr+"").split(",");
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
	tr = (tr+"").split(",");
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
	
	console.log("_________________")
	console.log(nighttime +"*"+w_days+"="+nighttime*w_days);
	console.log(time_arr);
	console.log("_________________")
	
	return time_arr;
}

function get_yookgab(price, timerange_arr, date_state_arr, ecb_arr){
	var daytime = timerange_arr[0];
	var nighttime = timerange_arr[1];
	var w_days = date_state_arr[0];
	var w_ends = date_state_arr[1];
	
	var night_factor = 1.5;
	var ends_factor = 2;
	var insur_factor = 1;


	/*
	 * I need Logic
	 * */

	var yg_arr = new Array();
	yg_arr[1] = price * daytime * w_days;
	yg_arr[2] = price * daytime * w_ends * ends_factor;
	yg_arr[3] = price * nighttime * w_days * night_factor;
	yg_arr[4] = price * nighttime * w_ends * ends_factor * night_factor;
	yg_arr[5] = 0; //주휴수당
	yg_arr[0] = yg_arr[1] + yg_arr[2] + yg_arr[3] + yg_arr[4] + yg_arr[5];
	
	console.log("_________________")
	console.log(nighttime +"*"+w_days+"="+nighttime*w_days);
	console.log(yg_arr);
	console.log("_________________")
	
	return yg_arr;
}

function modify_yg_table(price, tr_arr, date_state_arr, ecb_arr){
	var yg_arr = get_yookgab(price, tr_arr, date_state_arr, ecb_arr);
	$('#result').text(get_readable_won(yg_arr[0]));
	$('#dt-wd').text(get_readable_won(yg_arr[1]));
	$('#dt-we').text(get_readable_won(yg_arr[2]));
	$('#nt-wd').text(get_readable_won(yg_arr[3]));
	$('#nt-we').text(get_readable_won(yg_arr[4]));
	$("#wkhol").text("구현할거임"/*get_readable_won(yg_arr[5])*/);
}

function toggle_alert(flag){
	var div_front = '<div class="alert alert-danger alert-fixed text-center" role="alert"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span><span>'
	var msg = "";
	var div_end = '</span></div>'
	$(".alert").remove();
	if(flag){
		msg = " 시간 범위를 00:00부터 24:00까지로 변경했습니다";
	} else {
		msg = " 시간 범위를 12:00부터 다음날 12:00까지로 변경했습니다";
	}
	var alert_width = $(document).width() * 0.66;
	$(".nin-head").append(div_front + msg + div_end);
	$(".alert-fixed").css("width", alert_width);
	$(".alert-fixed").css("margin-left", -alert_width * 0.5);
	$(".alert-fixed").css("display", "inline");
}

/* variable default settings */
var today = new Date();
var year = today.getFullYear();
var month = today.getMonth() + 1;
var date_stat =  getDayStatOfMonth(year, month, get_chosen_days());
var tr_mode = 1;
var price = document.getElementById('seegeup').value;
var timerange = document.getElementById('timerange').value;
var work_time = get_time_from_tr(timerange, tr_mode);
var ecb_arr = [false, false];
var is_there= false;

/* event handle */
$(document).ready(function (){
	$('#view-seegeup').text(get_readable_won(price));
	$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
	$('#year-month').text(year+"년 "+month+"월");
	modify_yg_table(price, work_time, date_stat, ecb_arr);
});

$(".extra-cond").click(function(){
	price = document.getElementById('seegeup').value;
	timerange = document.getElementById('timerange').value;
	work_time = get_time_from_tr(timerange, tr_mode);
	
	var idx = $(".extra-cond").index(this);
	ecb_arr[idx] = !ecb_arr[idx];
	modify_yg_table(price, work_time, date_stat, ecb_arr);
});

$("#seegeup").on("slide", function(e){
	price = e.value;
	$('#view-seegeup').text(get_readable_won(e.value));
	modify_yg_table(price, work_time, date_stat, ecb_arr);
});

$("#timerange").on("slide", function(e){
	timerange = e.value;
	$('#view-timerange').text(get_readable_tr(e.value, tr_mode));
	modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
});

$(".slider-horizontal").on("click", function(e){
	price = document.getElementById('seegeup').value;
	timerange = document.getElementById('timerange').value;
	$('#view-seegeup').text(get_readable_won(price));
	$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
	modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
});

$(".btn-week").click(function() {
	var idx = ($(".btn-week").index(this) + 1)%7;
	var chosen_days_arr = get_chosen_days();
	chosen_days_arr[idx] = !chosen_days_arr[idx];
	date_stat =  getDayStatOfMonth(year, month, chosen_days_arr);
	modify_yg_table(price, work_time, date_stat, ecb_arr);
});

$('#chan-timerange').click(function() {
	/* alert */
	toggle_alert(is_there);
	setTimeout(function() {
 		$(".alert").fadeTo(500, 0).slideUp(500, function(){
        	$(this).remove(); 
	    });
	}, 3*1000);
	is_there = !is_there;
	
	/* modify yg */
	tr_mode = 3 - tr_mode; // 1<->2
	$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
	modify_yg_table(price, get_time_from_tr(timerange, tr_mode), date_stat, ecb_arr);
});

$(".m-row").click(function(){
	var test = $(this).children();
	get_each_time(get_time_from_tr(timerange, tr_mode), date_stat);
});
