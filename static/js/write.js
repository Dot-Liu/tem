$(function() {
	isLogin();
	getName();

	function isLogin() {
		$.get('/api/user/is/login', function(data) {
			var data = JSON.parse(data),
				status = data.status;
			if (status == 200) {
				if (data.data.is_login == 'false') {
					alert("您的账号未登录，请重新登录");
					location.href = "index.html";
				}

			}
		})
	}

	function send() {
		var content = $('#write-content').val();
		$.post('/api/letter/send', {
			content: content
		}, function(data) {
			var data = JSON.parse(data),
				status = data.status;
			if (status == '200') {
				window.location.replace('user.html');
			} else if (status == '700') {
				console.log('系统出错');
			}
		})
	}

	function getName() {
		$.get('/api/mate/name/get', function(data) {
			var data = JSON.parse(data),
				status = data.status;
			if (status == '200') {
				$('#cut-off').html('断绝关系');
				$('#btn-captcha').removeClass('btn-cap-freeze').removeAttr('disabled');
				$('#sole').html(data.data.mate_name)
			}
			if (status == '450') {
				$('#cut-off').html('没有关系');
				$('#cut-off').addClass('btn-cap-freeze').attr('disabled', 'true');
			} else console.log('无对象')
		})
	}

	function cutOff() {
		var r = confirm("山无棱天地合，确认与君决？");
		if (r == true) {
			$.post('/api/mate/disconnect', function(data) {
				var data = JSON.parse(data),
					status = data.status;
				if (status == '200') {
					window.location.replace('begin.html');
				} else {
					console.log(error);
				}

			})
		}

	}

	function logOut() {
		var r = confirm("确认要退出？");
		if (r == true) {
			$.post('/api/user/logout', function(data) {
				var data = JSON.parse(data),
					status = data.status;
				if (status == '200') {
					window.location.replace('index.html');
				} else {
					console.log(status);
				}
			})
		}
	}
	$('#btn-send').click(send);
	$('#write-content').keyup(function() {
		if ($("#write-content").val() == '')
			$('#btn-send').addClass('btn-cap-freeze').attr('disabled', 'true');
		else $('#btn-send').removeClass('btn-cap-freeze').removeAttr('disabled');
	})
	$("#cut-off").click(cutOff);
	$('#log-out').click(logOut)
})