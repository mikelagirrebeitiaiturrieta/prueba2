d3.csv("https://raw.githubusercontent.com/MikelAgirrebeitia/trabajo_internacional/main/debts.csv", function(err, data){  
    
    var x1 = [];
    for (var i=0; i<data.length; i++) {
        var paises = Object.keys(data[i])
        for (var pais of paises) {
            if ((!['index'].includes(pais))&(data[i][pais]!="")){
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
        end: 500, 
        size: 20, 
        start: -500
      }
    };
    var data = [trace1];
    var layout = {
        bargap: 0, 
        bargroupgap: 0.2, 
        barmode: "overlay", 
        title: "Distribución del % de deuda en Europa", 
        xaxis: {title: "% Deuda respecto PIB"}, 
        yaxis: {title: "Frecuencia"}
      };
    var config = {responsive: true};
    Plotly.newPlot('hist1', data, layout, config);
})