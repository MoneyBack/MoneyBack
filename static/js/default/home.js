$(document).ready(function(){
	var sites = homeData.sites;
	$('.merchant_s').click(function(){
		if (!!this.id) {
			// 设置站点数据
			var merchantImg = $('#current').find('img');
			merchantImg.unbind();
			merchantImg.attr('src', '/static/img/default/sites/' + sites[this.id].pretty_logo + '.png');
			merchantImg.parent().attr('id', this.id);
			var sInfo = merchantImg.parent().siblings('.s_info');
			sInfo.removeClass('none');
			var sInfoLeft = sInfo.find('.s_info_left');
			sInfoLeft.attr('title', sites[this.id].rebate_info);
			sInfoLeft.text(sites[this.id].rebate_info);
			var fInfo = merchantImg.parent().siblings('.f_info');
			fInfo.removeClass('none');
			mbMark = fInfo.find('.mb_mark');
			mbPrefer = fInfo.find('.mb_prefer');
			if (sites[this.id].rebate != 1) {
				mbMark.addClass('invisible');
			} else {
				mbMark.removeClass('invisible');
			}
			if (sites[this.id].type != 3) {
				mbPrefer.addClass('invisible');
			} else {
				mbPrefer.removeClass('invisible');
			}
		}
		$('#backdrop').addClass('hide');
		$('#homeContainer').removeClass('blur');
		$('#all_sites').addClass('hide');
	});
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
			// 打开添加站点面板
			$(this).attr('id', 'current');
			$('#backdrop').removeClass('hide');
			$('#homeContainer').addClass('blur');
			$('#all_sites').removeClass('hide');
			$.each($('#all_sites li a'), function(){
				var siteImage = $(this).children()[0];
				$(siteImage).attr('src', sites[this.id].logo_url);
			});
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