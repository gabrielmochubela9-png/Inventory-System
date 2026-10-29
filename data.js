var D=load('stock_v1',null);
if(!D){D={items:[
{id:'p1',sku:'ICE-5KG',name:'Ice bags 5kg',cat:'Ice',qty:120,min:40,cost:18,price:30},
{id:'p2',sku:'ICE-10KG',name:'Ice bags 10kg',cat:'Ice',qty:18,min:25,cost:32,price:50},
{id:'p3',sku:'CUP-250',name:'Paper cups 250ml (50)',cat:'Packaging',qty:60,min:20,cost:22,price:38},
{id:'p4',sku:'CLN-5L',name:'Sanitiser 5L',cat:'Cleaning',qty:6,min:8,cost:95,price:140},
{id:'p5',sku:'TOW-12',name:'Hand towels (12)',cat:'Cleaning',qty:35,min:10,cost:40,price:65}],
log:[{id:'x1',item:'p2',type:'out',qty:12,date:today(-2),note:'Weekend event order'},{id:'x2',item:'p1',type:'in',qty:60,date:today(-4),note:'Supplier delivery'}]};save('stock_v1',D)}
function S(){save('stock_v1',D)}
function R(n){return'R'+(Math.round(n*100)/100).toLocaleString('en-ZA',{minimumFractionDigits:2,maximumFractionDigits:2})}
function it(id){return D.items.find(function(i){return i.id===id})}
function st(i){return i.qty<=0?'out':i.qty<=i.min?'low':'ok'}
function pill(i){var s=st(i);return'<span class="pill '+(s==='ok'?'ok':s==='low'?'warn':'bad')+'">'+(s==='ok'?'In stock':s==='low'?'Low':'Out of stock')+'</span>'}
