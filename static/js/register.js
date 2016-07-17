$(function() {
	//错误显示函数
	function tipShow(obj) {
		var tip = $('.tip');
		tip.addClass('hidden');
		tip.removeClass('slow-out');
		obj.removeClass('hidden');
		obj.addClass('slow-show');
		setTimeout(function() {
			obj.addClass('slow-out');
		}, 3000);
	}

	function test() {
		var email = $('#email').val();
		if (email != '') {
			$.post('/api/user/verify/send', {
				email: email
			}, function(data) {
				var data = JSON.parse(data);
				if (data.status == '200') {
					$('#btn-captcha').addClass('btn-cap-freeze').attr('disabled', 'true');
					setTimeout(function() {
						$('#btn-captcha').removeClass('btn-cap-freeze').removeAttr('disabled');
					}, 60000)
					tipShow($('#tip-send'));
				}
				if (data.status == '420') {
					tipShow($('#err-exist'));

				}
				if (data.status == '700') {
					tipShow($('#err-captcha'));

				}
				if (data.status == '701') {
					tipShow($('#err-server'));

				}
				if (data.status == '120') {
					tipShow($('#err-email'));
				}

			})
		} else tipShow($('#err-null-email'));
	}
	//（不加密前）判断新密码和旧密码一致性
	function register() {
		var email = $('#email').val(),
			password = $('#password').val(),
			captcha = $('#captcha').val();
			name= $('#name').val(),
		    sex=$('input[name="Sex"]:checked').val(),
		    sexNum=0;
		    if (sex=='male') {
		    	sexNum=0;
		    }else sexNum=1;
			//每项是否为空
		if (email && password && captcha && name != '') {
			if (name.length<=20) {
				$.post('/api/user/register', {
					email: email,
					verify_code: captcha,
					password: password,
					name:name,
					is_male:sexNum
				}, function(data) {
					var data = JSON.parse(data);
					if (data.status == '200') {
						tipShow('#tip-success');
						setTimeout(function() {
							window.location.replace("login.html");
						}, 500)
					}
					if (data.status == '130') {
						tipShow($('#err-psw-len'));
					}
					if (data.status == '131') {
						tipShow($('#err-psw-type'));
					}
					if (data.status == '420') {
						tipShow($('#err-exist'));
					}
					if (data.status == '431') {
						tipShow($('#err-capt'));
					}
					if (data.status == '700') {
						tipShow($('#err-server'));
					}
				})
			}else tipShow($('#err-name-len'));
				
			}else tipShow($('#err-null'));
	}
	$("#btn-captcha").on('click', test);
	$('#btn-register').on('click', register);
})