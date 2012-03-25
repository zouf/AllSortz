
$(document).ready(function(){

	$('#submit').click(function() {

	//	$('#waiting').show(500);
	//	$('#demoForm').hide(0);
	//	$('#message').hide(0);

		$.ajax({
			type : 'POST',
			url : 'search/search.php',
			dataType : 'json',
			data: {
				searchDat : $('#search').val(), location: $('#location').val()
			},
			success : function(data){
				$('#waiting').hide(500);
				$('#message').html(data.msg);
			//	$('#message').removeClass().addClass((data.error === true) ? 'error' : 'success')
			//		.text(data.msg).show(500);
				if (data.error === true)
					$('#demoForm').show(500);
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				alert(errorThrown);
				$('#waiting').hide(500);
				$('#message').removeClass().addClass('error')
					.text('There was an error.').show(500);
				$('#demoForm').show(500);
			}
		});

		return false;
	});

});