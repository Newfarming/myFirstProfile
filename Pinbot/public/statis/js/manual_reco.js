// Run the script on DOM ready:
$(function(){

	$('table').visualize({type: 'bar', width: '1100px',
                            rowFilter: ':not(:last)',
							parseDirection:"y"
                             });
	$('table').visualize({type: 'area', 
                          width: '1100px',
                          rowFilter: ':not(:last)',
						  parseDirection:"y"
                           });
	$('table').visualize({type: 'line', 
                          width: '1100px',
                          rowFilter: ':not(:last)',
						  parseDirection:"y"
                            });
    $('table').visualize(
               {type: 'pie', 
                 height: '300px',
                 width: '1100px',
                rowFilter: ':not(:last)',
               
                 });                           
});