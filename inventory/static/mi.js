mi = {


    changeCardCount: function(id, type, count) {
    	$.ajax({
    		type: "GET",
    		url:"/card/change_count/",
    		dataType: 'json',
    		data: {id: id, type: type, count: count},
    		success: function (data, status, xhr) {
    			if (data.type.indexOf("alt") == -1) {
    				$card = $("#" + data.id);
    			}
    			else {
    				$card = $("#alt_" + data.id)
    			}
				$card.children(".card_count").text(data.count);
				$card.children(".card_foil_count").text(data.foil_count);
    		}
    	});
    }



}