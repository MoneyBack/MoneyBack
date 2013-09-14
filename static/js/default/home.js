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
			$('#fav_sites').addClass('hide');
			$('#all_sites').removeClass('hide');
			$.each($('#all_sites li a'), function(){
				var siteImage = $(this).children()[0];
				$(siteImage).attr('src', sites[this.id].logo_url);
			});
			// 获得站点数据
			// ...
			// 设置站点数据
			/*
			var merchantImg = $(this).find('img');
			merchantImg.unbind();
			merchantImg.attr('src', '/static/img/default/sites/yhd.png');
			merchantImg.parent().attr('id', '1104');
			var sInfo = merchantImg.parent().siblings('.s_info');
			sInfo.removeClass('none');
			var sInfoLeft = sInfo.find('.s_info_left');
			sInfoLeft.attr('title', 'title-test');
			sInfoLeft.text('value-test');
			var fInfo = merchantImg.parent().siblings('.f_info');
			fInfo.removeClass('none');*/
		}
	});
	$('.s_info .delete').click(function(){
		$(this).parent().addClass('none');
		$(this).parent().siblings('.f_info').addClass('none');
		var siblingA = $(this).parent().siblings('a');
		siblingA.attr('id', '');
		var merchantImg = siblingA.find('img');
		var rnd = Math.floor(Math.random() * 3 + 1);
		merchantImg.attr('src', '/static/img/default/add' + rnd + '.png');
		merchantImg.bind('mouseover', function(){
			merchantImg.attr('src', '/static/img/default/add_hover' + rnd + '.png');
		});
		merchantImg.bind('mouseout', function(){
			merchantImg.attr('src', '/static/img/default/add' + rnd + '.png');
		});
	});
});