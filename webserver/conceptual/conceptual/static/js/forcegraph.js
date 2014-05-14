function init_graph(links, element, zoomLevel) {
  var nodes = {};
  var heaviestNode;
  var nodesCount = 0;

  // Compute the distinct nodes from the links.
  links.forEach(function(link) {
    link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, index: nodes.length - 1, count: 0});

    link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, index: nodes.length - 1, count: 0});

    if (!link.source.count) {
      nodesCount++;
    }
    if (!link.target.count) {
      nodesCount++;
    }

    link.source.count++;
    link.target.count++;

    if (heaviestNode in nodes) {
      if (nodes[link.source].count > nodes[heaviestNode].count) {
        heaviestNode = link.source;
      }

      if (nodes[link.target].count > nodes[heaviestNode]) {
        heaviestNode = link.target;
      }
    } else {
      heaviestNode = link.source;
    }

  });

  var width = 1020,
      height = 800,
      meanRadius = 16,
      linksPerNode = links.length / nodesCount;
      linkDistance = 250 * linksPerNode;

  var force = d3.layout.force()
      .nodes(d3.values(nodes))
      .links(links.filter(function(x) { return x.source.count >= zoomLevel && x.target.count >= zoomLevel;}))
      .size([width, height])
      .linkDistance(linkDistance)
      .charge(-1000)
      .on("tick", tick)
      .start();



  var svg = d3.select(element).append("svg")
      .attr("width", width)
      .attr("height", height);


  force.nodes(force.nodes().filter(function(x) { return x.count >= zoomLevel; }));

  // Per-type markers, as they don't inherit styles.
  svg.append("defs").selectAll("marker")
      .data(force.nodes())
    .enter().append("marker")
      .attr("id", function(d) { return d.index; })
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", function(d) { var r = getRadius(d); return r + 20; })
      .attr("refY", 0)
      .attr("markerWidth", 5)
      .attr("markerHeight", 5)
      .attr("orient", "auto")
    .append("path")
      .attr("d", "M0,-5L10,0L0,5");

  var path = svg.append("g").selectAll("path")
      .data(force.links())
    .enter().append("path")
      .attr("class", function(d) { return "link " + 'source-' + d.source.index + ' target-' + d.target.index; })
      .attr("marker-end", function(d) { return "url(#" + d.target.index + ")"; });

  var circle = svg.append("g").selectAll("circle")
      .data(force.nodes())
    .enter().append("circle")
      .attr("r", getRadius)
      .call(force.drag)
      .on('mouseover', mouseOver)
      .on('mouseout', mouseOut);

  var linkText = svg.append("g").selectAll("path")
      .data(force.links())
    .enter().append("text")
      .attr("x", 8)
      .attr("y", "1em")
      .attr("class", function(d) { return "link-text hidden " + 'source-' + d.source.index + ' target-' + d.target.index;})
      .text(function(d) { return d.type; });

  var text = svg.append("g").selectAll("text")
      .data(force.nodes())
    .enter().append("text")
      .attr("x", 8)
      .attr("y", "1em")
      .text(function(d) { return d.name; });


  function getRadius(node) {
    return meanRadius + (node.count - linksPerNode) * 2;
  }

  // Use elliptical arc path segments to doubly-encode directionality.
  function tick() {
    path.attr("d", linkArc);
    circle.attr("transform", transform);
    text.attr("transform", transform);
    linkText.attr('transform', linkTransform);
  }

  function mouseOver(d) {
    svg.selectAll('.link.source-' + d.index)
       .classed('highlight', true);
    svg.selectAll('.link-text.source-' + d.index)
       .classed('hidden', false);


    svg.selectAll('.link.target-' + d.index)
       .classed('highlight', true);
   svg.selectAll('.link-text.target-' + d.index)
       .classed('hidden', false);

  }

  function mouseOut(d) {
    svg.selectAll('.link.source-' + d.index)
       .classed('highlight', false);
    svg.selectAll('.link-text.source-' + d.index)
       .classed('hidden', true);


    svg.selectAll('.link.target-' + d.index)
       .classed('highlight', false);
    svg.selectAll('.link-text.target-' + d.index)
       .classed('hidden', true);

  }

  function linkArc(d) {
    var dx = (d.target.x) - (d.source.x),
        dy = (d.target.y) - (d.source.y),
        dr = Math.sqrt(dx * dx + dy * dy);
    return "M" + d.source.x + "," + d.source.y + "l" + dx + ',' + dy;
  }

  function linkTransform(d) {
    var dx = (d.target.x) - (d.source.x),
      dy = (d.target.y) - (d.source.y);
    return "translate(" + (d.source.x + (dx / 2)) + "," + (d.source.y + (dy / 2)) + ")";
  }

  function transform(d) {
    return "translate(" + d.x + "," + d.y + ")";
  }

  return heaviestNode;
}
