$(document).ready(function(){
	var sites = homeData.sites;
	$('.merchant').click(function(){
		window.open(sites[this.id].click_url, '_blank');
		$.ajax({
			type: "POST",
			url: "/openSite",
			data: {siteId:this.id},
			success: function(data) {}
		});
	});
});