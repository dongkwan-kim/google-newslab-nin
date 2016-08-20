/* help function with calc */
function get_sum(arr){
	var sum = 0;
	for(var idx = 0; idx < arr.length; idx++){
		sum += arr[idx];
	}
	return sum;
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
			return (start_time+12)%24 + "시 ~ 다음날 " + (end_time+12)%24 + "시";
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
	daytime = Math.max((daytime - $("#meal-time").val()), 0);
	return [daytime, nighttime];
}

function get_work_day_of_week(chosen_days){
	var cnt = 0;
	for(var idx=0; idx < chosen_days.length; idx++){
		if(chosen_days[idx]){
			cnt += 1;
		}
	}
	return cnt;
}

function get_yookgab(price, timerange_arr, chosen_days, ecb_arr){
	var daytime = timerange_arr[0];
	var nighttime = timerange_arr[1];
	var totaltime = daytime + nighttime;
	var wday_of_week = get_work_day_of_week(chosen_days);
	var whour_of_week = totaltime * wday_of_week;
	console.log(daytime+"\t"+nighttime);
	var ilban_of_week = 0;
	var joohyoo_of_week = 0;
	var yageun_plus_of_week = 0;
	var yeonjang_plus_of_week = 0;
	var hyooil_plus_of_week = 0;
	
	if(whour_of_week == 40){
		ilban_of_week = 173.6 * price;	
		joohyoo_of_week = 35.4 * price;
	} else {
		//ilban soodang
		ilban_of_week = whour_of_week * price * 4.345;
		
		//joohyoo soodang: >=15h
		if(whour_of_week >= 15){
			joohyoo_of_week = Math.min(whour_of_week/5, 8) * price * 4.345;
		}
	}
	
	//5in>=
	if(ecb_arr[0] == false){
		//yageun plus+ soodang
		yageun_plus_of_week = nighttime * wday_of_week * price * 0.5 * 4.345;
	
		//yeonjang plus+ soodang: >=40h
		if(whour_of_week > 40){
			yeonjang_plus_of_week = (whour_of_week - 40) * price * 0.5 * 4.345;
		}

		//hyooil plus+ soodang: ==7d
		if(wday_of_week == 7){
			hyooil_plus_of_week = (totaltime/7) * price * 0.5 * 4.345;
		}
	}

	var yg_arr = new Array();
	yg_arr[0] = 0
	yg_arr[1] = parseInt(ilban_of_week);
	yg_arr[2] = parseInt(joohyoo_of_week);
	yg_arr[3] = parseInt(yageun_plus_of_week);
	yg_arr[4] = parseInt(yeonjang_plus_of_week);
	yg_arr[5] = parseInt(hyooil_plus_of_week);
	yg_arr[0] = get_sum(yg_arr);
	
	return yg_arr;
}

function modify_yg_table(price, tr_arr, chosen_days, ecb_arr){
	var yg_arr = get_yookgab(price, tr_arr, chosen_days, ecb_arr);
	$('#result').text(get_readable_won(yg_arr[0]));
	$('#rt').text(get_readable_won(yg_arr[1]));
	$('#wkhol').text(get_readable_won(yg_arr[2]));
	$('#nt').text(get_readable_won(yg_arr[3]));
	$('#extnd').text(get_readable_won(yg_arr[4]));
	$('#holid').text(get_readable_won(yg_arr[5]));
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

function get_pr(){
	return parseInt($("#seegeup").val());
}

function get_tr(){
	var data_arr =  tr_slider.noUiSlider.get();
	return [parseInt(data_arr[0]), parseInt(data_arr[1])];
}

$(document).ready(function(){
	var tr_mode = 1;
	var price = get_pr();
	var timerange = get_tr();
	var chosen_days = get_chosen_days();
	var ecb_arr = [false];
	var is_there= false;
	
	$('#view-seegeup').text(get_readable_won(price));
	$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
	modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
	
	$("#seegeup").change(function(){
		});
	
	var is_first = true;
	$("#refr-seegeup").click(function(){
		$("#seegeup").val(6030);
		price = get_pr();
		$('#view-seegeup').text(get_readable_won(price));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
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
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
	});
	
	$("#meal-time").change(function(){
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
	});

	$(".extra-cond").click(function(){
		price = get_pr();
		timerange = get_tr();
	
		var idx = $(".extra-cond").index(this);
		ecb_arr[idx] = !ecb_arr[idx];
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
		if(idx == 0){
			if(ecb_arr[idx]){
				$("#modal-trigger-nt").css("color", "#cccccc");
				$("#modal-trigger-extnd").css("color", "#cbcbcb");
				$("#modal-trigger-holid").css("color", "#cbcbcb");
			} else {
				$("#modal-trigger-nt").css("color", "#000000");
				$("#modal-trigger-extnd").css("color", "#000000");
				$("#modal-trigger-holid").css("color", "#000000");
			}
		}
	});

	tr_slider.noUiSlider.on("update", function(){
		//price = get_pr();
		timerange = get_tr();

		$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
	});
	
	$(".btn-week").click(function() {
		if($(this).hasClass("active")){
			$(this).removeClass("active");
			var idx = $(".btn-week").index(this);
			var day_list = ["월", "화", "수", "목", "금", "토", "일"];
			$(this).text(day_list[idx]);
		} else {
			$(this).addClass("active");
			$(this).html('<i class="material-icons">done</i>');
		}
		price = get_pr();
		timerange = get_tr();
		chosen_days = get_chosen_days();
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
	});	

	$('#chan-timerange').change(function() {
		/* alert */
		toggle_alert(is_there);
		is_there = !is_there;
	
		/* modify yg */
		tr_mode = 3 - tr_mode; // 1<->2
		$('#view-timerange').text(get_readable_tr(timerange, tr_mode));
		modify_yg_table(price, get_time_from_tr(timerange, tr_mode), chosen_days, ecb_arr);
		
	});

	$("tr.modal-trigger").click(function(){
		var idx = $("tr.modal-trigger").index(this);
		var this_id = $(this).attr("id");
		var modal_id = this_id.replace("-trigger", "");
		$("#"+modal_id).openModal();
	});
	
});
