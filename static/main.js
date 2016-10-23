$("#querybox").click(function(e){
	e.preventDefault();
	console.log("querying");
	var keyword = $('#queryword').val();
	
	$.ajax({
		url:'/query',
		data: {
			keyword: keyword
		},
		type: 'POST',
		success: function(response){
			console.log(typeof(response));
			console.log(response);
			reload();
		},
		error: function(error){
			console.log(error);
		} 
	});
});
