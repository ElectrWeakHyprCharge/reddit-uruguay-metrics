'use strict';


let pointInfo = document.getElementById('point-info');
let legend = document.getElementById('legend')
let sourceColors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c'];
let seriesNames = {
  'Subscribers': 'Subscriptores',
  'Submissions': 'Posts',
  'Comments': 'Comentarios'
}


function inlineBox(color) {
  return '<div class="inline-box" style="background-color:' + color + ';"></div>'
}


let graph = new Dygraph(
  document.getElementById("graph"),
  "data.csv",
  {
    visibility: [true, false, false],
    xlabel: "Tiempo",
    ylabel: "Subscriptores",

    connectSeparatedPoints: true,
    pointSize: 1,
    highlightCircleSize: 4,
    hideOverlayOnMouseOut: false,
    xValueParser: x => Date.parse(x),

    //highlightSeriesOpts: { strokeWidth: 3 },
    //showRangeSelector: true,
    //showRoller: true,
    //rollPeriod: 1,

    labelsDiv: legend,
    legend: 'always',
    legendFormatter: function (data) { // Custom format for the tooltip
      if (data.xHTML === undefined) return '';
      let text = 'Fecha: ' + data.xHTML + '<br>';
      let row = this.getRowForX(data.x);

      let yvalues = data.series
        .map((s, col) => [s.labelHTML, this.getValue(row, col + 1)])
        .filter(x => x[1] !== null)

      text += yvalues.map(x => seriesNames[x[0]] + ': ' + x[1]).join(' - ');

      let source = sources[row];
      let boxes = source.id.map(id => inlineBox(sourceColors[id])).join(', ')
      text += '<br>Fuente (' + boxes + '): <code>' + source.text.join(', ') + '</code>';

      return text;
    },

    axes: {
      x: {
        ticker: Dygraph.dateTicker, // generates tick marks
        axisLabelFormatter: function (d, granularity, opts, dygraph) {
          // custom display format for the tick marks
          return d.toLocaleDateString();
        },
        valueFormatter: Dygraph.dateString_, // custom display format for the tooltip
        pixelsPerLabel: 100,
      }
    },

    series: {
      'Subscribers': {
        color: '#000000',
        strokeWidth: 0,
        drawPoints: true,
        fillGraph: true,
      },
      'Submissions': {
        color: '#1e59aa',
        drawPoints: false,
        stepPlot: true,
        fillGraph: true,
      },
      'Comments': {
        color: '#17843b',
        drawPoints: false,
        stepPlot: true,
        fillGraph: true,
      }
    },
    drawHighlightPointCallback: function (g, seriesName, canvasContext, cx, cy, seriesColor, pointSize, row) {
      let fill = sources[row].id.map(color => sourceColors[color]);

      for (let i = 0; i < fill.length; i++) {
        canvasContext.beginPath();
        canvasContext.fillStyle = fill[i];
        canvasContext.strokeStyle = fill[i];
        let from = i / fill.length * 2 * Math.PI - Math.PI / 2;
        let to = (i + 1) / fill.length * 2 * Math.PI - Math.PI / 2;
        canvasContext.arc(cx, cy, pointSize, from, to, false);
        canvasContext.fill();
        canvasContext.stroke();
      }
    },
    pointClickCallback: function (e, point) {
      pointInfo.innerHTML = legend.innerHTML
      /*
        + seriesNames[point.name] + ": " + point.yval + '<br>'
        + new Date(point.xval).toLocaleString() + '<br>'
        + "Fuente: " + sources[point.idx].text.join(', ');*/
    }
  }
)


function showSubscriberGrowth() {
  graph.setVisibility([true, false, false]);
  graph.updateOptions({
    ylabel: "Subscriptores",
  })
}

function showActivity() {
  graph.setVisibility([false, true, true]);
  graph.updateOptions({
    ylabel: "Posts / Comentarios por día"
  })
}
