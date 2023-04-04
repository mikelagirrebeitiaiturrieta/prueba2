d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/employment.csv", function(err, data){  
    
    var x1 = [];
    for (var i=0; i<data.length; i++) {
        var paises = Object.keys(data[i])
        for (var pais of paises) {
            if ((!['European Union - 28 countries (2013-2020)','European Union - 27 countries (from 2020)', 'index','Euro area - 19 countries  (from 2015)'].includes(pais))&(data[i][pais]!="")){
                x1.push(parseFloat(data[i][pais]))
            }
            }
        }
    
    console.log(x1)
    var trace1 = {
      x: x1,
      histnorm: "count", 
      autobinx: false, 
      marker: {
        color: "#23007A", 
        line: {
        color:  "#23007A", 
        width: 2
        }
    },  
       opacity: 0.75, 
       type: "histogram", 
       xbins: {
        end: 100, 
        size: 2, 
        start: 40
      }
    };
    var data = [trace1];
    var layout = {
        bargap: 0, 
        bargroupgap: 0.2, 
        barmode: "overlay", 
        title: "Distribución del % de población ocupada en Europa", 
        xaxis: {title: "% Población Ocupada"}, 
        yaxis: {title: "Frecuencia"}
      };
    var config = {responsive: true};
    Plotly.newPlot('hist2', data, layout, config);
})