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
		var email = $('#iemail').val();

		if (email != '') {
			$.post('/api/user/password/forget', {
				email: email
			}, function(data) {
				var data = JSON.parse(data);
				if (data.status == '200') {
					tipShow($('#tip-send'));
				}
				if (data.status == '422') {
					tipShow($('#err-no-exist'));
				}
				if (data.status == '700') {
					tipShow($('#err-captcha'));
				}
				if (data.staus == '701') {
					tipShow($('#err-server'));
				}

			})
		} else tipShow($('#err-null-email'));
	}
	//（不加密前）判断新密码和旧密码一致性
	function forget() {
		var email = $('#iemail').val(),
			password = $('#ipassword').val(),
			repassword = $('#irepassword').val(),
			captcha = $('#captcha').val();
      	//每项是否为空
		if (email && password && repassword && captcha != '') {
			if (password != repassword) {
				$('#irepassword').val('');
				tipShow($('#err-repsw'));
			} else {
				$.post('/api/user/password/verify', {
					email: email,
					verify_code: captcha,
					new_password: password
				}, function(data) {
					var data = JSON.parse(data);
					if (data.status == '200') {
						window.location.replace("login.html");
					}
					if (data.status=='111') {
						tipShow($('#err-capt'));
					}
					if (data.status == '130') {
						tipShow($('#err-psw-len'));
					}
					if (data.status == '131') {
						tipShow($('#err-psw-type'));
					}
					if (data.status == '422') {
                        tipShow($('#err-no-exist'));     
					}
					if (data.status == '431') {
						tipShow($('#err-capt'));
					}
					if (data.status == '700') {
						tipShow($('#err-server'));
					}
				})
			}
		} else tipShow($('#err-null'));

	}
	$("#btn-captcha").on('click', test);
	$('#btn-forget').on('click', forget);
})