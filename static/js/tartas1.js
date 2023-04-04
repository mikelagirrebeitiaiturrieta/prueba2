// var parseTime = d3.timeParse("%Y");

d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/education.csv", function(error, data){

  if (error) throw error;
    
  // format the data
  // data.forEach(function(d) {
  //     d.date = d.index;
  //     d.europe = parseFloat(d['European Union - 28 countries (2013-2020)'])/28;
  //     d.italy = parseFloat(d.Italy);
  //     d.germany = parseFloat(d['Germany (until 1990 former territory of the FRG)'])
  //     d.ireland = parseFloat(d.Ireland);
  // });


  // console.log(data)
  // data.sort(function(a,b){
  //     return new Date(b.date) - new Date(a.date);
  // });
  
const pos = data.length-1
var paises = Object.keys(data[pos])
var resto_europa = 0
for(var i=0; i<paises.length; i++){
  if (['Ireland', 'Germany (until 1990 former territory of the FRG)', 'Italy', 'European Union - 28 countries (2013-2020)','European Union - 27 countries (from 2020)', 'index'].includes(paises[i])){
    if (data[pos][paises[i]]!=''){
      resto_europa+=parseFloat(data[pos][paises[i]])
    }
  }
}


    var datos = [
      {
        values: [
          parseFloat(data[pos]['Ireland']),parseFloat(data[pos]['Germany (until 1990 former territory of the FRG)']),parseFloat(data[pos]['Italy']),resto_europa
        ],
        labels: [
          'Ireland', 'Germany', 'Italy', 'Resto de Europa'
        ],
        domain: { column: 0 },
        name: "Color",
        hoverinfo: "label+percent+name",
        hole: 0.4,
        type: "pie",
        marker: {
          colors: [
            "#66c2a5",
            "#fc8e62",
            "#e78ac3",
            "#8d9bcb"
          ],
        },
      },
    ];
    // console.log(datos)
    var layout = {
      title: "Distribución de la educación terciaria en Europa",
      
      showlegend: true,
    }    


    
    var config = {responsive: true}
      Plotly.newPlot('tarta_1', datos, layout,config);
});