// this function executes our search via an AJAX call
function runSearch() {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    // $('#uploadresults').hide();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './search_product.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

//this function executes the search via an AJAX call to give suggestions via .autocomplete()
function autoFill() {
	$( "#search_term" ).autocomplete({
		source: function( request, response ) {
			var maxRows = 5;
			var productName = request.term;
			var paramStr = "maxRows=" + maxRows + "&productName=" + productName;
			$.ajax({
				url: './search_product.cgi',
				dataType: 'json',
				data: paramStr,
				contentType: 'application/json; charset=utf-8',
				success: function( data ) {
					response( $.map( data.matches, function( item ) {
						return {
							label: item.product,
							value: item.product
						}
					}));
				}
			});
		},
		minLength: 2,
		open: function() {
			$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
		},
		close: function() {
			$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
		}
	});
}

// this processes a passed JSON structure representing gene matches and draws it
//  to the result table
function processJSON( data ) {
    // set the span that lists the match count
    $('#match_count').text( data.match_count );
    
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
    
        // create a row and append it to the body of the table
        $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
        
        // add the organism column
        $('<td/>', { "text" : item.organism } ).appendTo('#' + this_row_id);

        // add the locus column
        $('<td/>', { "text" : item.locus } ).appendTo('#' + this_row_id);
        
        // add the product column
        $('<td/>', { "text" : item.product } ).appendTo('#' + this_row_id);

        // add the residues column
        $('<td/>', { "text" : item.residues } ).appendTo('#' + this_row_id);

    });
    
    // now show the result section that was previously hidden
    $('#results').show();
}

// // this function uploads & processes the requested file via an AJAX call
// function uploadFile() {
//     // hide and clear the previous results, if any
//     $('#results').hide();
//     $('tbody').empty();
//     $('#uploadresults').hide();
// }

// run our javascript once the page is ready
$(document).ready( function() {
    // define what should happen when a user clicks submit on our search form
    $('#submit').click( function() {
        runSearch();
        return false;  // prevents 'normal' form submission
    });
    $(function(){
		autoFill();
	});
    // $('#filesubmit').click( function() {
    //     // uploadFile();
    //     alert('Please wait while your file is processed.');
    //     return false;  // prevents 'normal' form submission
    // });
});
