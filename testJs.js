var ret = '{"稅後純益成長率": {"201901": -6.83,"201803": -40.17,"201804": NaN,"201802": -20.19},"自由現金流量(百萬)": {"201901": -6013.78,"201804": -5179.4,"201803": 2881.58,"201802": -5360.96}}';
ret = ret.replace(/\bNaN\b/g, "null")
var parsedObj = JSON.parse(ret);
for(var k in parsedObj) {
    console.log(k);
    for(var kd in parsedObj[k]){
        console.log(kd.toString() + ': ' + String(parsedObj[k][kd]));
    }
 }