var serverhost = 'http://127.0.0.1:8000';

	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {
		  var url;
      if(request.type == "wiki"){
        url = serverhost + '/wiki/get_wiki_summary/?topic='+ encodeURIComponent(request.topic);
        fetch(url)
        .then(response => response.json())
        .then(response => sendResponse({farewell: response}))
        .catch(error => console.log(error))

      }else if(request.type == "page"){
        chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
          url = serverhost + '/wiki/get_page_summary/?topic='+ tabs[0].url;
          fetch(url)
          .then(response => response.json())
          .then(response => sendResponse({farewell: response}))
          .catch(error => console.log(error))
        });
      }	
			return true;  // Will respond asynchronously.
	});

	