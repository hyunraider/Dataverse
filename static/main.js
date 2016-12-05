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
$(document).ready(function(){
  gutter:10
});


var $grid = $("#masonry").masonry({
});

$("#insertbox").click(function(e){
    e.preventDefault();
    var keyword = $('#queryword').val();
    var insert = $('#insertstuff').val();
    var cat = $('#category').val();
    var summary = $('#inputText').val();
    var imageURL = $('#inputURL').val();

    $.ajax({
        url:'/insert',
        data: {
            keyword: keyword,
            insert: insert,
            cat: cat,
            summary: summary,
            imageURL: imageURL
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
                        $('#card-name').text("Keyword Doesn't Exist!");
                        $('#card-summary').text("But we just added it to the Database! Refresh and enter that Term again!");
                    },
                    error: function(error){
                        console.log(error);
                    }
                });

            }else{
                var myStuff = myJSON[0];
                
                $('#card-name').text(myStuff.title);
                $('#card-summary').text(myStuff.summary);
                $('.card-image img').attr("src", myStuff.images);

                var index = 0;
                for (x in myJSON){
                    index++;
                    if (index==1) continue;
                    var list = myJSON[x]
                    console.log(list);
                    var $newblock = $(document.createElement('div'));
                    $newblock.addClass("col-sm-4");
                    $newblock.css({"width":"250px", "display":"inline-block" ,"border": "1px #d3d3d3 solid", "background-color":"white"});
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

