// var parseTime = d3.timeParse("%Y");

d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/employment.csv", function(error, data){

  if (error) throw error;
    
  // format the data
  // data.forEach(function(d) {
  //     d.date = d.index;
  //     d.europe = parseFloat(d['European Union - 28 countries (2013-2020)'])/28;
  //     d.italy = parseFloat(d.Italy);
  //     d.germany = parseFloat(d['Germany (until 1990 former territory of the FRG)'])
  //     d.ireland = parseFloat(d.Ireland);
  // });


  console.log(data)
  // data.sort(function(a,b){
  //     return new Date(b.date) - new Date(a.date);
  // });
  
const pos = data.length-1
var paises = Object.keys(data[pos])
var paises_dict = []
var paises2_dict = []

for(var i=0; i<paises.length; i++){
  if (!['Ireland', 'Germany (until 1990 former territory of the FRG)', 'Italy', 'European Union - 28 countries (2013-2020)','European Union - 27 countries (from 2020)', 'index','Euro area - 19 countries  (from 2015)'].includes(paises[i])){
    paises_dict.push({'pais':paises[i], 'value':parseFloat(data[pos][paises[i]])})
  }else{
    if (['Ireland', 'Germany (until 1990 former territory of the FRG)', 'Italy'].includes(paises[i])){
     if (paises[i]=='Germany (until 1990 former territory of the FRG)'){
        paises2_dict.push({'pais':'Germany', 'value':parseFloat(data[pos][paises[i]])})
      }else{
        paises2_dict.push({'pais':paises[i], 'value':parseFloat(data[pos][paises[i]])})
      }
      
    }
  }
}

resto_europa = data[pos]['European Union - 27 countries (from 2020)']
paises_dict = paises_dict.sort(function(a,b) {
  return b.value - a.value
});

paises2_dict.push({'pais':'Resto de Europa', 'value':resto_europa})
paises_dict = paises_dict.slice(0,10)
paises_dict = paises_dict.concat(paises2_dict)

paises_dict = paises_dict.sort(function(a,b) {
  return b.value - a.value
});

var vals = []
var labs = []

for (var i=0; i<paises_dict.length; i++){
  vals.push(paises_dict[i].value)
  labs.push(paises_dict[i].pais)
}


          
var trace = {
      x: labs,
      y: vals,
      name: 'Población Ocupada',
      type: 'bar',
      marker:
      {
          color: [
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#fc8e62",
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#66c2a5",
            "#8d9bcb",
            "#e78ac3"
          ]
      }
    };
    
  
    var data = [trace];
    var layout = {barmode: 'stack',title: 'Población ocupada por país',
    xaxis: {
      tickangle: 25,
      tickfont: {
        size: 10,
        color: 'rgb(107, 107, 107)'
      }},
    
    yaxis: {
      title: {
        text: 'Cantidad',
    
      }
    }
                      };
    var config = {responsive: true}
      Plotly.newPlot('barra1', data, layout,config);
});