/**
 * @author Chine
 */
var locked = false;

$(function(){
	$("#commentform").ajaxForm({
		beforeSubmit: checkComment,
		success: dealResponse
	});
	
	$('a.comment-reply-link').live('click', function() {
		var thisTop = $(this).parents('li').offset().top;
		var commentId = $(this).parents('li').attr('id').split('-')[1];
		var replyName = $(this).parent().parent()
					.siblings('div.comment-info')
					.children('cite')
					.children('a').text();
		var replyContent = $(this).parent().siblings('p').text();
		
		var $obj = $('div.post-bottom-section:last');
		var $h4 = $obj.children('h4');
		
		//scroll to the comment form
		$('html, body').scrollTop($obj.offset().top);
		
		$('#id_reply_to_comment').val(commentId);
		$h4.html("回复"+ replyName + "：").attr({
			'rel': 'tooltip',
			'data-original-title': "点此关闭对\""+ replyContent+"\"的回应"
		}).addClass('tt').tooltip({
			placement: 'bottom'
		}).tooltip('show').one('click', function() {
			removeTooltip();
			$('html, body').scrollTop($('#comment-'+commentId).offset().top);
		});
		return false;
	});
	
	$('body').ajaxStart(function(){
		$(this).addClass('modal-open')
			.append("<div id=\"overlay\" class=\"modal-backdrop- fade in\"></div>");
	});

	$('body').ajaxComplete(function(){
		$(this).removeClass('modal-open').children("#overlay").remove();
	});
});

function removeTooltip() {
	$('div.post-bottom-section:last h4').attr({
		'rel': '',
		'data-original-title': ''
	}).removeClass('tt').html("给作者留言").tooltip('hide');
	$('#id_reply_to_comment').val('');
}

function addModalTip(type) {
	$('#resultmodal .modal-body p').html(commentTips[type]);
}

function checkComment(arr, $form, options) {
	if(locked)
		return false;
	
	for(itm in arr) {
		var obj = arr[itm];
		
		var name = obj.name;
		var value = obj.value;
		
		if(name == 'username'|| name=='email_address' || name=="content") {
			if((name=='username' &&　value=='你的昵称')
				|| (name=='email_address' && value=='你的邮箱')) {
				value = '';
			}
			
			if(value == '' || typeof value == undefined) {
				addModalTip('miss');
				$('#resultmodal').modal();
				
				return false;
			}
		}
		
		if(name=='site' && value=='你的网站') {
			obj.value = '';
		}
		
	}
	
	if(!locked)
		locked = true;
}

function dealResponse(responseText,statusText) {
	if(locked) locked = false;
	$('textarea#message').val('');
    $('#end-of-comment').before(responseText);
	$('html, body').scrollTop($('li.newest').offset().top);
    return True;

	$('#resultmodal').off('hidden');
	
	if(responseText == "0") {
		addModalTip('fail');
	} else if(responseText == "-1"){
		addModalTip('nochn');
	} else {
		addModalTip('success');
		$('#resultmodal').on('hidden', function() {
			$.get(ajaxUrl, function(data) {
				if($('div.post-bottom-section:last h4').hasClass('tt')) {
					removeTooltip();
				}
				
				var $objs = $("div.post-bottom-section");
				if($objs.length == 1) {
					$objs.before(data)
				} else {
					$objs.eq(0).replaceWith(data);
				}
				// empty the comment content
				$('textarea#message').val('');
				//scroll to the new comment
				$('html, body').scrollTop($('#comment-'+responseText).offset().top);
			});
		});
	}
	$('#resultmodal').modal();
	if(locked) locked = false;
}
