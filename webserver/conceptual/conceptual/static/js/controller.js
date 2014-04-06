document.onload = function() {
    var baseURI = 'http://localhost:8001/api/';
    var element = '#graph';

    function receivedExtractions(extractions) {
        var links = [];
        extractions.forEach(function(extraction) {
            links.append({
                source: extraction[0],
                type: extraction[1],
                target: extraction[2]
            });
        });
        forcegraph(links, element);
    }

    function fetchExtractions(website, page) {
        var requestURI = baseURI + 'extractions?website=' + website + '&page=' + encodeURIComponent(page);
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    receivedExtractions(JSON.parse(xhr.responseText));
                }
            }
        };
        xhr.open('GET', requestURI, true);
        xhr.send();
    }
};
