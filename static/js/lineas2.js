d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/employment.csv", function(err, data){

  function unpack(data, key) {
  return data.map(function(d) { return d[key]; });
}

data.forEach(function(d) {
  d.date = d.index;
  d.italy = parseFloat(d.Italy);
  d.germany = parseFloat(d['Germany (until 1990 former territory of the FRG)'])
  d.ireland = parseFloat(d.Ireland);
  d.europe = parseFloat(d['European Union - 27 countries (from 2020)'])
});


  var frames = []
  var x = unpack(data, 'date')
  var y = unpack(data, 'italy')
  var x2 = unpack(data, 'date')
  var y2 = unpack(data, 'germany')
  var x3 = unpack(data, 'date')
  var y3 = unpack(data, 'ireland')
  var x4 = unpack(data, 'date')
  var y4 = unpack(data, 'europe')

 
  for (var i = 0; i < x.length; i++) {
    frames[i] = {data: [{x: [], y: []}, {x: [], y: []},{x: [], y: []},{x: [], y: []}]}
    frames[i].data[3].x = x4.slice(0, i+1);
    frames[i].data[3].y = y4.slice(0, i+1);
    frames[i].data[2].x = x3.slice(0, i+1);
    frames[i].data[2].y = y3.slice(0, i+1);
    frames[i].data[1].x = x2.slice(0, i+1);
    frames[i].data[1].y = y2.slice(0, i+1);
    frames[i].data[0].x = x.slice(0, i+1);
    frames[i].data[0].y = y.slice(0, i+1);
  }

  var italy = {
    type: "scatter",
    name: 'Italy',
    x: frames[1].data[0].x,
    y: frames[1].data[0].y,
    line: {color: '#e78ac3'}
  }

  var germany = {
    type: "scatter",
    name: 'Germany',
    x: frames[1].data[1].x,
    y: frames[1].data[1].y,
    line: {color: '#fc8e62'}
  }

  var ireland = {
    type: "scatter",
    name: 'Ireland',
    x: frames[1].data[2].x,
    y: frames[1].data[2].y,
    line: {color: '#66c2a5'}
  }

  var s_europe = {
    type: "scatter",
    name: 'Europe',
    x: frames[1].data[3].x,
    y: frames[1].data[3].y,
    line: {color: '#8d9bcb'}
  }

  var data = [italy, germany,ireland, s_europe];
  console.log(data)

  var layout = {
    title: 'Evolución de la Población Ocupada',
    xaxis: {
      title:'Fecha',
      range: [frames[x.length-1].data[0].x[0], frames[x.length-1].data[0].x[x.length-1]],
      showgrid: false
    },   
    yaxis: {
      title:'% Población ocupada',
    },
      legend:{
        y:0.75,
        font: {
            size:12
        }
    },
    annotations:[{
      x: "2020",
      y:83,
      xref:"x",
      yref: "y",
      text: "COVID-19"
  }],
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
  Plotly.newPlot('linea2', data, layout, config).then(function() {
    Plotly.addFrames('linea2', frames);
  });
})