function twitter_share(){
	var tw_content = "twitter sharing test";
	var url = location.href;
	var pop_opt = "width=600, height=400, resizable=no, scrollbars=no, status=no;";
	var wp = window.open("http://twitter.com/share?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(tw_content), 'twitter', pop_opt); 
	if (wp) {
		wp.focus();
	}     
}

function facebook_share(){
	var url = location.href;
	
	var pop_opt = "width=600, height=400, resizable=no, scrollbars=no, status=no;";
	var wp = window.open("http://www.facebook.com/share.php?u=" + encodeURIComponent(url), 'facebook', pop_opt); 
	if (wp) {
		wp.focus();
	} 

}
 
$(document).ready(function(){
	$('#fr_drop1').click(function (){
		$('fr_dropdown').html('tofu1 <span class="caret"></span>');
	});
});


