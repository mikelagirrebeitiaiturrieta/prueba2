// var parseTime = d3.timeParse("%Y");

d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/gdp.csv", function(error, data){

  if (error) throw error;
    
  // format the data
  data.forEach(function(d) {
      d.date = d.index;
      d.europe = parseFloat(d['European Union - 27 countries (from 2020)'])/27*(10**6);
      d.italy = parseFloat(d.Italy)*(10**6);
      d.germany = parseFloat(d['Germany (until 1990 former territory of the FRG)'])*(10**6);
      d.ireland = parseFloat(d.Ireland)*(10**6);
  });


  data.sort(function(a,b){
      return new Date(b.date) - new Date(a.date);
  });
  
data = data.slice(0,-1);

  function unpack(data, key) {
      return data.map(function(row) { return row[key]; });
    };


  console.log(d3.min(unpack(data,"date")))

  var serie_europe = {
      x: unpack(data,"date"),
      y: unpack(data,"europe"),
      type: 'scatter',
      name: "Europe",
      line: {color: '#8d9bcb'}
    };
  
  var serie_italy = {
    x: unpack(data,"date"),
    y: unpack(data,"italy"),
    type: 'scatter',
    name: "Italy",
    line: {color: '#e78ac3'}
  };
  
  var serie_germany = {
    x: unpack(data,"date"),
    y: unpack(data,"germany"),
    type: 'scatter',
    name: "Germany",
    line: {color: '#fc8e62'}
  };

  var serie_ireland = {
    x: unpack(data,"date"),
    y: unpack(data,"ireland"),
    type: 'scatter',
    name: "Ireland",
    line: {color: '#66c2a5'}
  };

    
  var datos = [serie_europe, serie_italy, serie_germany, serie_ireland];

    var layout = {
        title: "Evolución del Producto Interior Bruto",
        xaxis:{
            title: "Años",
            rangeselector:{buttons:[
                {
                    count: 3,
                    label: '3y',
                    step: 'year',
                    stepmode: 'backward'
                  },
                  {
                    count: 5,
                    label: '5y',
                    step: 'year',
                    stepmode: 'backward'
                  },
                  {step: 'all'}
            ]},
            rangeslider: {range: [d3.min(unpack(data,"date")), d3.max(unpack(data,"date"))]},
            type: 'date'
        },
        yaxis:{
          title: "Número de alumnos"
      },
      legend:{
          y:0.75,
          font: {
              size:12
          }
      },
    }
    
    var config = {responsive: true}
      Plotly.newPlot('linea3', datos, layout,config);
});