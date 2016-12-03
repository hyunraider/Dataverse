/*
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
			
			$("#imageBox").append("<img src='" + response["pictures"][0] + "'/>");
			
			reload();
		},
		error: function(error){
			console.log(error);
		} 
	});
});
*/
var $grid = $("#masonry").masonry({
            
});

$("#insertbox").click(function(e){
    e.preventDefault();
    var keyword = $('#queryword').val();
    var insert = $('#insertstuff').val();
    var cat = $('#category').val();
    $.ajax({
        url:'/insert',
        data: {
            keyword: keyword,
            insert: insert,
            cat: cat
        },
        type: 'POST',
        success: function(response){
            console.log("insert success!");
        
        },
        error: function(error){
            console.log(error);
        }
    });


});

$("#querybox").click(function(e){
    e.preventDefault();
    $("#masonry").empty();
    var keyword = $('#queryword').val();
    $.ajax({
        url:'/query',
        data: {
            keyword: keyword
        },
        type: 'POST',
        success: function(response){
            console.log("success!!");

            var myJSON = JSON.parse(response);

            if (myJSON.includes("NULL")){
                console.log("DOESNT EXIST");
                
                $.ajax({
                    url:'/autoinsert',
                    data: {
                        keyword: keyword
                    },
                    type: 'POST',
                    success: function(response){
                        console.log("Success in Autoinsert");
                    },
                    error: function(error){
                        console.log(error);
                    }
                });

            }else{
                for (x in myJSON){
                    var list = myJSON[x]
                    console.log(list);
                    var $newblock = $(document.createElement('div'));
                    $newblock.addClass("col-sm-4");
                    $newblock.css({"width":"250px", "display":"inline-block" ,"border": "2px black solid", "background-color":"red"});
                    $newblock.append("<h4>" + list[0] + "</h4>");
                    console.log(response);
                    console.log(myJSON.summary);
                    $newblock.append("<p style='font-size:10px'>" + list[2] + "</p>");
                    setTimeout($grid.append($newblock).masonry('appended', $newblock, true), 2000);
                }
            $("#masonry").masonry(); 
            }
        },
        error: function(error){
            console.log(error);
        }
    });
})

