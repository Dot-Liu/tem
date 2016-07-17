$(function() {
	isLogin();
	getName();
	LitsShow(0);

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

	function LitsShow(num) {
		var list = $('#letter-list');
		$.post('/api/letter/list', {
			last_letter_id: '0',
			have_read: num
		}, function(data) {
			var data = JSON.parse(data),
				status = data.status,
				letterNum = data.data.length;
			if (status == '200') {
				var tmpl = $('#letter-tmpl').html();
				var doTtmpl = doT.template(tmpl);
				$('#letter-list').html(doTtmpl(data));
				if (num == '0') {
					$('#noread-num').html(letterNum);
				}
				$('#letter-num').html(letterNum);
			} else {}
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
	$('#letter-tmpl').html();

	function letterShow(num) {
		var letter = $(this).data('id')
		event.stopPropagation();
		$.post('/api/letter/detail/get', {
			letter_id: letter
		}, function(data) {
			var data = JSON.parse(data);
			$('#write-content').html(data.data.content);
		})
	}
	$("#letter-list").on('click', '.letter', letterShow);
	$('#letter-status-read').on('click', function() {
		$('#letter-status-read').addClass("letter-status-active");
		$('#letter-status-noread').removeClass("letter-status-active")
		LitsShow(1);
	});
	$('#letter-status-noread').on('click', function() {
		$('#letter-status-noread').addClass("letter-status-active");
		$('#letter-status-read').removeClass("letter-status-active")
		LitsShow(0);
	});
	$("#cut-off").click(cutOff);
	$('#log-out').click(logOut);
})