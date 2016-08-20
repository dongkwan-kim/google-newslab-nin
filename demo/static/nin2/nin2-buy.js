
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

function get_readable_hour(hour){
	int_part = Math.floor(hour);
	frac_part = Math.ceil((hour - int_part)*60);
	if(frac_part == 0 && int_part == 0){
		return frac_part + "분";
	} else if (frac_part == 0){
		return int_part + "시간";
	} else if (int_part == 0){
		return frac_part + "분";
	}else {
		return int_part + "시간 " + frac_part + "분";
	}
}
