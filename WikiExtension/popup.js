$(function(){

    $('#keywordsubmit').click(function(){
    $('#loading-image').show();
		var search_topic = $('#keyword').val();	
		if (search_topic){
      chrome.runtime.sendMessage({topic: search_topic, type: "wiki"}, function(response) {
						result = response.farewell;
            $('#loading-image').hide();
            $( '#summaryTitle' ).show();
            $( '#summaryCategories' ).hide();
            $("#summaryResult").text(result.summary);
					});
		}
  });

    $('#pageSubmit').click(function(){
      $('#loading-image').show();
      chrome.runtime.sendMessage({topic: "", type: "page"}, function(response) {
        result = response.farewell;
        $('#loading-image').hide();
        $( '#summaryTitle' ).show();
        $( '#summaryCategories' ).text("categories: " + result.topics);
        $("#summaryResult").text(result.summary)
      });
    });

});