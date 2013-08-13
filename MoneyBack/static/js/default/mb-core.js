var version = '1.0.0';

$(document).ready(function(){
	$('#searchI').mousedown(function(){
		$('#searchBoxInner').addClass('searchBoxInner-focus');
	});
	$('#searchI').blur(function(){
		$('#searchBoxInner').removeClass('searchBoxInner-focus');
	});
});