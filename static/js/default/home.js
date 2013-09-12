$(document).ready(function(){
	var sites = homeData.sites;
	$('.merchant').click(function(){
		if (!!this.id) {
			window.open(sites[this.id].click_url, '_blank');
			$.ajax({
				type: "POST",
				url: "/openSite",
				data: {siteId:this.id},
				success: function(data) {}
			});
		} else {
			// 添加站点
		}
	});
	$('.s_info .delete').click(function(){
		alert('test');
	});
});