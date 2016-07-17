$(function() {
	function check(){
		$.get('/api/mate/check',function(data){
			var data = JSON.parse(data);
			  if (data.data.is_mate) {
			  	    window.location.replace("user.html");
			  }
			  else window.location.replace("begin.html");
			 		})
	}
	function submit() {
		var loginName = $("#ilogin-name").val(),
			password = $('#ilogin-psw').val();
		if (loginName == '' || password == '') {
			errorShow($('#err-null'));
		} else $.post('/api/user/login', {
			login_name: loginName,
			password: password
		}, function(data) {
			var data = JSON.parse(data),
			status=data.status;
			if (status == '200') {
               check();
			} else if (status == '422') {
				errorShow($('#err-email'));
			} else if (status == '430') {
				errorShow($('#err-psw'));
			} else if (status == '700') {
				errorShow($('#err-server'));
			}

		})
	}
	function errorShow(obj) {
		var error = $('.error');
		error.addClass('hidden');
		error.removeClass('slow-out');
		obj.removeClass('hidden');
		obj.addClass('slow-show');
        setTimeout(function(){obj.addClass('slow-out');},3000);
	}

	$("#btn-login").on('click', submit);
	$('#ilogin-psw').keydown(function(event) {
		var keycode = event.which;
		if (keycode == '13') {
			submit();
		}
	})
	$('#ilogin-name').keydown(function(event) {
		var keycode = event.which;
		if (keycode == '13') {
			$('#ilogin-psw').focus();
		}
	})
})