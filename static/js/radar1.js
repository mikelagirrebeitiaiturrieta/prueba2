d3.queue()
.defer(d3.csv, "https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/education.csv")
.defer(d3.csv, "https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/population.csv")
.defer(d3.csv, "https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/employment.csv")
.await(function(error, data, data2, data3){
    if (error) {
        console.error(error);
    }
    else {

var len = data.length-1
var keys = Object.keys(data[len])
var italy = []
var ireland = []
var germany = []

for (var key of keys) {
    var total_pop_europe = 0
    var media_educacion = 0
    var media_empleo = 0
    var contador = 0
    var keys2 =  Object.keys(data[len])
    for  (var key2 of keys2) {
        if ((!['index','European Union - 27 countries (from 2020)','European Union - 28 countries (2013-2020)'].includes(key2))&(data2[len][key2]!='')&(data[len][key2]!='')&(data3[len][key2]!='')) {
            total_pop_europe += parseFloat(data2[len][key2])
            media_educacion += parseFloat(data[len][key2])
            media_empleo += parseFloat(data3[len][key2])
            contador += 1
        }
    }
    total_pop_europe = total_pop_europe/contador
    media_educacion = media_educacion/contador
    media_empleo = media_empleo/contador
    if (['Italy','Ireland', 'Germany (until 1990 former territory of the FRG)'].includes(key)){
        if (key=='Italy'){
            italy.push(parseFloat(data[len][key])/media_educacion)
            italy.push(parseFloat(data2[len][key])/total_pop_europe)
            italy.push(parseFloat(data3[len][key])/media_empleo)
        }else if (key=='Ireland'){
            ireland.push(parseFloat(data[len][key])/media_educacion)
            ireland.push(parseFloat(data2[len][key])/total_pop_europe)
            ireland.push(parseFloat(data3[len][key])/media_empleo)
        }else{
            germany.push(parseFloat(data[len][key])/media_educacion)
            germany.push(parseFloat(data2[len][key])/total_pop_europe)
            germany.push(parseFloat(data3[len][key])/media_empleo)
        }
    }
}

datos = [italy, ireland, germany]



data = [
    {
    type: 'scatterpolar',
    r: datos[2],
    theta: ['Educación Terciaria','Población','Tasa Ocupación'],
    fill: 'toself',
    name: 'Germany',
    marker:{color:'#fc8e62'}
    },
    {
    type: 'scatterpolar',
    r: datos[0],
    theta: ['Educación Terciaria','Población','Tasa Ocupación'],
    fill: 'toself',
    name: 'Italy',
    marker:{color:'#e78ac3'}
    },
    {
    type: 'scatterpolar',
    r: datos[1],
    theta: ['Educación Terciaria','Población','Tasa Ocupación'],
    fill: 'toself',
    name: 'Ireland',
    marker:{color:'#66c2a5'}
    }
  ]
  
  layout = {
      title:'Resumen Variables Socioeconómicas',
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 5]
      }
    }
  }
  
  var config = {responsive: true}
  Plotly.newPlot("radar1", data, layout, config)
}
});