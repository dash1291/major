document.onreadystatechange = function(e) {
    var baseURI = 'http://localhost:8001/api/';
    var element = '#graph';
    var links = [];
    var detailLevel = 0;
    var maxDetail;

    function copyArray(links) {
        var newArray = [];
        links.forEach(function(link) {
            newArray.push({
                source: link.source,
                type: link.type,
                target: link.target
            });
        });

        return newArray;
    }

    function receivedExtractions(extractions) {
        extractions.forEach(function(extraction) {
            links.push({
                source: extraction[0],
                type: extraction[1],
                target: extraction[2]
            });
        });
        var linksCopy = links.concat();
        console.log(links);
        maxDetail = init_graph(copyArray(links), element, detailLevel).count;
        console.log(links);
    }

    function fetchExtractions(page) {
        var requestURI = baseURI + 'extractions?page=' + encodeURIComponent(page);
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

    if (document.readyState === 'complete') {
        fetchExtractions(document.querySelector('#graph').getAttribute('data-page'));

        document.querySelector('#zoom-in').onclick = function(e) {
            if (detailLevel) {
                document.querySelector('#graph').innerHTML = '';
                init_graph(copyArray(links), element, --detailLevel);

            }
        };

        document.querySelector('#zoom-out').onclick = function(e) {
            if (maxDetail >= detailLevel) {
                document.querySelector('#graph').innerHTML = '';
                init_graph(copyArray(links), element, ++detailLevel);
            }
        };
    }
};
