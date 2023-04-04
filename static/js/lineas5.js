d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/debts.csv", function(err, data){

  function unpack(data, key) {
  return data.map(function(d) { return d[key]; });
}

var europe = []
for (var i=0; i<data.length; i++) {
  keys = Object.keys(data[i])
  var contador = 0
  var intermediate_europe = 0
  for (key of keys) {
    if ((!['index'].includes(key)) & (data[i][key]!="")){
      intermediate_europe += (parseFloat(data[i][key]))
      contador +=1
    }
}
europe.push(intermediate_europe/contador)
}

data.forEach(function(d) {
  d.date = d.index;
  d.italy = parseFloat(d.Italy);
  d.germany = parseFloat(d['Germany (until 1990 former territory of the FRG)'])
  d.ireland = parseFloat(d.Ireland);
});


  var frames = []
  var x = unpack(data, 'date')
  var y = unpack(data, 'italy')
  var x2 = unpack(data, 'date')
  var y2 = unpack(data, 'germany')
  var x3 = unpack(data, 'date')
  var y3 = unpack(data, 'ireland')
//   var x4 = unpack(data, 'date')
//   var y4 = europe

 
  for (var i = 0; i < europe.length; i++) {
    frames[i] = {data: [{x: [], y: []}, {x: [], y: []},{x: [], y: []},{x: [], y: []}]}
    // frames[i].data[3].x = x4.slice(0, i+1);
    // frames[i].data[3].y = y4.slice(0, i+1);
    frames[i].data[2].x = x3.slice(0, i+1);
    frames[i].data[2].y = y3.slice(0, i+1);
    frames[i].data[1].x = x2.slice(0, i+1);
    frames[i].data[1].y = y2.slice(0, i+1);
    frames[i].data[0].x = x.slice(0, i+1);
    frames[i].data[0].y = y.slice(0, i+1);
  }

  var italy = {
    type: "scatter",
    mode: "lines",
    name: 'Italy',
    x: frames[1].data[0].x,
    y: frames[1].data[0].y,
    line: {color: '#e78ac3'}
  }

  var germany = {
    type: "scatter",
    mode: "lines",
    name: 'Germany',
    x: frames[1].data[1].x,
    y: frames[1].data[1].y,
    line: {color: '#fc8e62'}
  }

  var ireland = {
    type: "scatter",
    mode: "lines",
    name: 'Ireland',
    x: frames[1].data[2].x,
    y: frames[1].data[2].y,
    line: {color: '#66c2a5'}
  }

//   var s_europe = {
//     type: "scatter",
//     mode: "lines",
//     name: 'Europe',
//     x: frames[1].data[3].x,
//     y: frames[1].data[3].y,
//     line: {color: '#8d9bcb'}
//   }

  var data = [italy, germany,ireland];
  console.log(data)

  var layout = {
    title: 'Multiple Trace Filled-Area Animation',
    xaxis: {
      range: [frames[europe.length-1].data[0].x[0], frames[europe.length-1].data[0].x[europe.length-1]],
      showgrid: false
    },
    yaxis: {
        range: [-410,100],
        showgrid: false
      },
    legend: {
      orientation: 'h',
      x: 0.5,
      y: 1.2,
      xanchor: 'center'
    },
    updatemenus: [{
      x: 0.5,
      y: 0,
      yanchor: "top",
      xanchor: "center",
      showactive: false,
      direction: "left",
      type: "buttons",
      pad: {"t": 87, "r": 10},
      buttons: [{
        method: "animate",
        args: [null, {
          fromcurrent: true,
          transition: {
            duration: 500,
          },
          frame: {
            duration: 500,
            redraw: false
          }
        }],
        label: "Play"
      }, {
        method: "animate",
        args: [
          [null],
          {
            mode: "immediate",
            transition: {
              duration: 100
            },
            frame: {
              duration: 1000,
              redraw: true
            }
          }
        ],
        label: "Pause"
      }]
    }]
  };

  var config = {responsive: true}
  Plotly.newPlot('linea5', data, layout, config).then(function() {
    Plotly.addFrames('linea5', frames);
  });
})