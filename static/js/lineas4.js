d3.queue()
.defer(d3.csv, "https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/gdp.csv")
.defer(d3.csv, "https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/population.csv")
.await(function(error, data, data2){
    if (error) {
        console.error(error);
    }
    else {
      var europe = []
      for (var i=0; i<data.length; i++) {
        keys = Object.keys(data[i])
        keys2 = Object.keys(data2[i])
        var contador = 0
        var intermediate_europe = 0
        for (key of keys) {
          if ((!['European Union - 28 countries (2013-2020)','European Union - 27 countries (from 2020)', 'index','Euro area - 19 countries  (from 2015)','European Union - 15 countries (1995-2004)', 
          'Euro area (EA11-1999, EA12-2001, EA13-2007, EA15-2008, EA16-2009, EA17-2011, EA18-2014, EA19-2015)','Euro area - 12 countries (2001-2006)','index'].includes(key)) & (data[i][key]!="") & (keys2.includes(key)) & (data2[i][key]!="")){
            intermediate_europe += (parseFloat(data[i][key])*(10**6))/parseFloat(data2[i][key])
            contador +=1
          }
          if ((data2[i][key] != "") & (key!='index')) {
            data[i][key] = (parseFloat(data[i][key])*(10**6))/parseFloat(data2[i][key])
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
    
  
    data.sort(function(a,b){
        return new Date(b.date) - new Date(a.date);
    });
    
  data = data.slice(0,-1);
  
    function unpack(data, key) {
        return data.map(function(row) { return row[key]; });
      };
  

  
    var serie_europe = {
        x: unpack(data,"date"),
        y: europe,
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
          title: "Evolución del Producto Interior Bruto per capita",
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
      Plotly.newPlot('linea4', datos, layout,config);
  }
});
 