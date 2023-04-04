// var parseTime = d3.timeParse("%Y");

d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/debts.csv", function(error, data){

  if (error) throw error;
    
  
const pos = data.length-1
var paises = Object.keys(data[pos])
var paises_dict = []
var paises2_dict = []
var media_europa = 0
var contador = 0

for(var i=0; i<paises.length; i++){
  if ((data[pos][paises[i]]!='')&(!['Ireland', 'Germany (until 1990 former territory of the FRG)', 'Italy','index'].includes(paises[i]))){
    console.log(data[pos][paises[i]])
    media_europa += parseFloat(data[pos][paises[i]])
    contador += 1
  }
  if (!['Ireland', 'Germany (until 1990 former territory of the FRG)', 'Italy','index'].includes(paises[i])){
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

resto_europa = media_europa/contador
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
      name: 'Deudas',
      type: 'bar',
      marker:
      {
          color: [
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#e78ac3",
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#23007A",
            "#fc8e62",
            "#8d9bcb",
            "#66c2a5",
          ]
      }
    };
    
  
    var data = [trace];
    var layout = {barmode: 'stack',title: 'Deudas en % de PIB en Europa',
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
      Plotly.newPlot('barra2', data, layout,config);
});