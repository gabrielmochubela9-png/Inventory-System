<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Inventory System</title>
<style>
:root{color-scheme:dark;--bg:#070605;--surface:#100E0A;--ink:#F5F0E8;--muted:#A89F8A;--line:#3A311C;--accent:#C9A84C;--on:#0A0A0A;--ok:#7bd88f;--bad:#ff7a6b;--warn:#f2b705}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(50rem 26rem at 90% -5%,rgba(201,168,76,.13),transparent 60%),var(--bg);color:var(--ink);font:400 1rem/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
.w{max-width:64rem;margin:0 auto;padding:1.25rem 1.1rem 3rem}
h1{font-size:clamp(1.6rem,5vw,2.3rem);margin:0 0 .3rem;letter-spacing:-.02em;line-height:1.1}
h2{font-size:1.1rem;margin:0 0 .8rem}
p.lead{color:var(--muted);margin:0 0 1rem;max-width:44rem}
.tabs{display:flex;gap:.3rem;border-bottom:1px solid var(--line);margin-bottom:1.1rem;overflow-x:auto}
.tabs button{font:inherit;font-weight:500;color:var(--muted);background:transparent;border:0;border-bottom:3px solid transparent;padding:.6rem .95rem;cursor:pointer;white-space:nowrap}
.tabs button:hover{color:var(--ink)}
.tabs button[aria-selected=true]{color:var(--ink);border-bottom-color:var(--accent)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem;margin-bottom:1rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(9.5rem,1fr));gap:.75rem;margin-bottom:1rem}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.8rem 1rem}
.stat b{display:block;font-size:1.6rem;line-height:1.1}.stat span{color:var(--muted);font-size:.85rem}
form.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.7rem;align-items:end}
label{display:flex;flex-direction:column;gap:.25rem;font-size:.85rem;color:var(--muted)}
input,select,textarea{font:inherit;color:var(--ink);background:#0b0907;border:1.5px solid var(--line);border-radius:6px;padding:.5rem .6rem;width:100%;min-width:0}
input:focus,select:focus,textarea:focus{border-color:var(--accent);outline:none}
.btn{font:inherit;font-size:.92rem;font-weight:500;cursor:pointer;color:var(--ink);background:transparent;border:1.5px solid var(--line);border-radius:6px;padding:.5rem .95rem}
.btn:hover{border-color:var(--accent)}
.btn.go{background:var(--accent);border-color:var(--accent);color:var(--on)}
.btn.sm{padding:.2rem .6rem;font-size:.82rem}
.btn.del:hover{border-color:var(--bad);color:var(--bad)}
.row{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin-bottom:.8rem}
.row .sp{flex:1}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{text-align:left;padding:.55rem .8rem;border-bottom:1px solid var(--line);vertical-align:middle}
th{color:var(--muted);font-weight:500;font-size:.82rem;white-space:nowrap}
tr:last-child td{border-bottom:0}
td.r,th.r{text-align:right}
.pill{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:.05rem .65rem;font-size:.8rem;color:var(--muted);white-space:nowrap}
.pill.ok{color:var(--ok);border-color:rgba(123,216,143,.45)}.pill.bad{color:var(--bad);border-color:rgba(255,122,107,.5)}.pill.warn{color:var(--warn);border-color:rgba(242,183,5,.5)}
.empty{color:var(--muted);padding:1.2rem;text-align:center}
.note{color:var(--muted);font-size:.85rem;margin:.6rem 0 0}
.err{color:var(--bad);font-size:.88rem;min-height:1.3rem;margin:.4rem 0 0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.bar{height:8px;border-radius:99px;background:#241f12;overflow:hidden;min-width:5rem}.bar i{display:block;height:100%;background:var(--accent)}
</style></head><body>
<div class="w">
<h1>Inventory System</h1>
<p class="lead">Track stock levels, receive and issue items, get low-stock alerts, and see what your stock is worth. Data stays in this browser.</p>
<div class="tabs" id="tabs"></div>
<div id="main"></div>
<div class="sr" id="live" role="status" aria-live="polite"></div>
</div>
<script>
var $=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
function esc(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
var mem={};
function load(k,def){try{var v=localStorage.getItem(k);if(v)return JSON.parse(v)}catch(e){}return mem[k]?JSON.parse(mem[k]):def}
function save(k,v){var s=JSON.stringify(v);mem[k]=s;try{localStorage.setItem(k,s)}catch(e){}}
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,6)}
function today(d){var x=new Date();x.setDate(x.getDate()+(d||0));return x.toISOString().slice(0,10)}
function say(t){var l=$('#live');if(l){l.textContent='';setTimeout(function(){l.textContent=t},30)}}
function tabs(names,render){var t=$('#tabs'),cur=0;t.setAttribute('role','tablist');
 function draw(){t.innerHTML=names.map(function(n,i){return'<button role="tab" aria-selected="'+(i===cur)+'" data-i="'+i+'">'+n+'</button>'}).join('');
  $$('button',t).forEach(function(b){b.onclick=function(){cur=+b.dataset.i;draw()}});render(cur)}
 draw();return{go:function(i){cur=i;draw()},redraw:function(){render(cur)}}}
function dl(name,text,type){var b=new Blob([text],{type:type||'text/csv'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(a.href)},5000)}
function csv(rows){return rows.map(function(r){return r.map(function(c){c=String(c==null?'':c);return/[",\n]/.test(c)?'"'+c.replace(/"/g,'""')+'"':c}).join(',')}).join('\n')}
</script>
<script>
var AUTH_KEY="stock";
(function(){
var K='auth_'+AUTH_KEY,SK='sess_'+AUTH_KEY,me=null,lock=0,lockUntil=0;
var enc=new TextEncoder();
function b64(u){var s='';u=new Uint8Array(u);for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s)}
function unb64(s){var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
async function hash(pw,salt){
 var key=await crypto.subtle.importKey('raw',enc.encode(pw),'PBKDF2',false,['deriveBits']);
 return b64(await crypto.subtle.deriveBits({name:'PBKDF2',salt:salt,iterations:100000,hash:'SHA-256'},key,256))}
function users(){return load(K,[])}
function saveUsers(u){save(K,u)}
function sess(){try{return sessionStorage.getItem(SK)}catch(e){return mem[SK]||null}}
function setSess(v){try{if(v)sessionStorage.setItem(SK,v);else sessionStorage.removeItem(SK)}catch(e){mem[SK]=v||null}}
async function mk(name,pw,role){var salt=crypto.getRandomValues(new Uint8Array(16));return{name:name,key:name.toLowerCase(),salt:b64(salt),hash:await hash(pw,salt),role:role,made:today()}}
async function check(u,pw){return await hash(pw,unb64(u.salt))===u.hash}
var css=document.createElement('style');
css.textContent='#authov{position:fixed;inset:0;z-index:1000;display:flex;align-items:center;justify-content:center;padding:1rem;background:radial-gradient(50rem 26rem at 90% -5%,rgba(201,168,76,.15),transparent 60%),#070605;overflow:auto}'+
'.authbox{width:100%;max-width:25rem;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1.4rem;box-shadow:0 20px 60px rgba(0,0,0,.6)}.authbox h2{font-size:1.35rem;margin:0 0 .2rem}.authbox p{margin:0 0 1rem;color:var(--muted);font-size:.9rem}.authbox form{display:grid;gap:.75rem}.authbox .tabs{margin-bottom:1rem}'+
'#authbar{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;justify-content:flex-end;padding:.5rem 1.1rem;border-bottom:1px solid var(--line);background:#0b0907;font-size:.88rem;color:var(--muted)}#authbar b{color:var(--ink)}#authbar .sp{flex:1}'+
'.role-staff .del{display:none!important}#authmod{position:fixed;inset:0;z-index:900;background:rgba(0,0,0,.7);display:flex;align-items:flex-start;justify-content:center;padding:1rem;overflow:auto}#authmod .authbox{max-width:40rem;margin-top:2rem}'+
'@media print{#authbar,#authov,#authmod{display:none!important}}';
document.head.appendChild(css);
function app(on){var w=$('.w');if(w){w.inert=!on;w.setAttribute('aria-hidden',on?'false':'true')}}
function gate(){
 var us=users(),ov=document.createElement('div');ov.id='authov';app(false);
 var mode=us.length?'in':'up';
 function draw(){
  ov.innerHTML='<div class="authbox" role="dialog" aria-modal="true" aria-labelledby="ah"><h2 id="ah">'+esc(document.title)+'</h2><p>'+(mode==='in'?'Sign in to continue.':(us.length?'Create a staff account.':'Create the first account. It will be the administrator.'))+'</p>'+
  (us.length?'<div class="tabs" role="tablist"><button role="tab" aria-selected="'+(mode==='in')+'" data-m="in">Sign in</button><button role="tab" aria-selected="'+(mode==='up')+'" data-m="up">Create account</button></div>':'')+
  '<form id="af"><label>Username<input name="u" autocomplete="username" required minlength="3" maxlength="24" pattern="[A-Za-z0-9._\\-]+" title="Letters, numbers, dot, dash and underscore"></label><label>Password<input name="p" type="password" autocomplete="'+(mode==='in'?'current-password':'new-password')+'" required minlength="6"></label>'+
  (mode==='up'?'<label>Confirm password<input name="c" type="password" autocomplete="new-password" required minlength="6"></label>':'')+
  '<button class="btn go">'+(mode==='in'?'Sign in':'Create account')+'</button></form><p class="err" id="ae" role="alert" style="margin:.6rem 0 0"></p>'+
  '<div style="margin-top:.6rem;padding-top:.8rem;border-top:1px solid var(--line)"><button class="btn" id="demo" style="width:100%">Try the demo account</button><p class="note" style="margin:.6rem 0 0">Accounts and data are stored in this browser only. Nothing is sent to a server.</p></div></div>';
  $$('[data-m]',ov).forEach(function(b){b.onclick=function(){mode=b.dataset.m;draw()}});
  var f=$('#af');f.elements.u.focus();
  f.onsubmit=async function(e){e.preventDefault();var E=f.elements,n=E.u.value.trim(),p=E.p.value,er=$('#ae');er.textContent='';
   if(!window.crypto||!crypto.subtle){er.textContent='This browser cannot hash passwords securely. Use a current browser over HTTPS.';return}
   var all=users(),k=n.toLowerCase();
   if(mode==='in'){
    if(Date.now()<lockUntil){er.textContent='Too many attempts. Wait '+Math.ceil((lockUntil-Date.now())/1000)+' seconds.';return}
    var u=all.find(function(x){return x.key===k});
    if(!u||!(await check(u,p))){lock++;if(lock>=5){lockUntil=Date.now()+30000;lock=0}er.textContent='Wrong username or password.';return}
    lock=0;enter(u)}
   else{
    if(all.some(function(x){return x.key===k})){er.textContent='That username is taken.';return}
    if(p!==E.c.value){er.textContent='The passwords do not match.';return}
    var real=all.filter(function(x){return!x.demo}).length;
    var nu=await mk(n,p,real===0?'admin':'staff');all.push(nu);saveUsers(all);enter(nu)}};
  $('#demo').onclick=async function(){var all=users(),u=all.find(function(x){return x.key==='demo'});
   if(!u){u=await mk('demo','demo1234','admin');u.demo=true;all.push(u);saveUsers(all)}enter(u)}}
 function enter(u){me=u;setSess(u.key);ov.remove();app(true);bar();say('Signed in as '+u.name)}
 document.body.appendChild(ov);draw()}
function bar(){
 var b=$('#authbar');if(!b){b=document.createElement('div');b.id='authbar';document.body.insertBefore(b,document.body.firstChild)}
 document.body.classList.toggle('role-staff',me.role!=='admin');
 b.innerHTML='<span>Signed in as <b>'+esc(me.name)+'</b> <span class="pill">'+(me.role==='admin'?'Administrator':'Staff')+'</span></span><span class="sp"></span><button class="btn sm" id="bpw">Change password</button>'+(me.role==='admin'?'<button class="btn sm" id="bus">Manage users</button>':'')+'<button class="btn sm" id="bout">Log out</button>';
 $('#bout').onclick=function(){setSess(null);me=null;b.remove();document.body.classList.remove('role-staff');gate()};
 $('#bpw').onclick=function(){modal('pw')};var bu=$('#bus');if(bu)bu.onclick=function(){modal('users')}}
function modal(kind){
 var m=document.createElement('div');m.id='authmod';
 function close(){m.remove();var b=$('#authbar');if(b){var x=$(kind==='pw'?'#bpw':'#bus');if(x)x.focus()}}
 function draw(){
  if(kind==='pw'){m.innerHTML='<div class="authbox" role="dialog" aria-modal="true" aria-labelledby="mh"><h2 id="mh">Change password</h2><p>Signed in as '+esc(me.name)+'.</p><form id="mf"><label>Current password<input name="o" type="password" autocomplete="current-password" required></label><label>New password<input name="n" type="password" autocomplete="new-password" required minlength="6"></label><div class="row" style="margin:0"><button class="btn go">Save password</button><button type="button" class="btn" id="mc">Cancel</button></div></form><p class="err" id="me" role="alert" style="margin:.6rem 0 0"></p></div>';
   $('#mc').onclick=close;var f=$('#mf');f.elements.o.focus();
   f.onsubmit=async function(e){e.preventDefault();var all=users(),u=all.find(function(x){return x.key===me.key});
    if(!(await check(u,f.elements.o.value))){$('#me').textContent='Current password is wrong.';return}
    var salt=crypto.getRandomValues(new Uint8Array(16));u.salt=b64(salt);u.hash=await hash(f.elements.n.value,salt);saveUsers(all);me=u;say('Password changed');close()}}
  else{var all=users();
   m.innerHTML='<div class="authbox" role="dialog" aria-modal="true" aria-labelledby="mh"><h2 id="mh">Manage users</h2><p>Administrators can add staff, change roles and remove accounts. Staff cannot delete records.</p><div class="tw"><table><thead><tr><th>User</th><th>Role</th><th></th></tr></thead><tbody>'+all.map(function(u){var self=u.key===me.key;return'<tr><td>'+esc(u.name)+(self?' (you)':'')+'</td><td><select data-r="'+u.key+'" aria-label="Role for '+esc(u.name)+'"'+(self?' disabled':'')+'><option value="admin"'+(u.role==='admin'?' selected':'')+'>Administrator</option><option value="staff"'+(u.role==='staff'?' selected':'')+'>Staff</option></select></td><td class="r">'+(self?'':'<button class="btn sm del2" data-x="'+u.key+'" aria-label="Remove '+esc(u.name)+'">Remove</button>')+'</td></tr>'}).join('')+'</tbody></table></div>'+
   '<h2 style="margin-top:1.2rem;font-size:1rem">Add a user</h2><form class="g" id="mf"><label>Username<input name="u" required minlength="3" maxlength="24" pattern="[A-Za-z0-9._\\-]+"></label><label>Password<input name="p" type="password" required minlength="6" autocomplete="new-password"></label><label>Role<select name="r"><option value="staff">Staff</option><option value="admin">Administrator</option></select></label><button class="btn go">Add user</button></form><p class="err" id="me" role="alert"></p><div class="row" style="margin:0"><button class="btn" id="mc">Close</button></div></div>';
   $('#mc').onclick=close;
   $$('[data-r]',m).forEach(function(s){s.onchange=function(){var a=users();a.find(function(x){return x.key===s.dataset.r}).role=s.value;saveUsers(a);say('Role updated')}});
   $$('[data-x]',m).forEach(function(b){b.onclick=function(){if(confirm('Remove this user?')){saveUsers(users().filter(function(x){return x.key!==b.dataset.x}));draw()}}});
   var f=$('#mf');f.onsubmit=async function(e){e.preventDefault();var E=f.elements,n=E.u.value.trim(),a=users();
    if(a.some(function(x){return x.key===n.toLowerCase()})){$('#me').textContent='That username is taken.';return}
    a.push(await mk(n,E.p.value,E.r.value));saveUsers(a);say('User added');draw()}}}
 document.body.appendChild(m);draw();
 m.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
 m.addEventListener('click',function(e){if(e.target===m)close()})}
// boot: restore session or gate
var s=sess(),u=s&&users().find(function(x){return x.key===s});
if(u){me=u;bar()}else gate();
})();
</script>
<script>
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
var T;
function render(i){var m=$('#main');[dash,stock,move,hist][i](m)}
T=tabs(['Dashboard','Stock','Receive and issue','History'],render);
function dash(m){var val=D.items.reduce(function(s,i){return s+i.qty*i.cost},0),ret=D.items.reduce(function(s,i){return s+i.qty*i.price},0),low=D.items.filter(function(i){return st(i)!=='ok'});
 m.innerHTML='<div class="stats"><div class="stat"><b>'+D.items.length+'</b><span>Products</span></div><div class="stat"><b>'+D.items.reduce(function(s,i){return s+i.qty},0)+'</b><span>Units in stock</span></div><div class="stat"><b>'+R(val)+'</b><span>Stock value (cost)</span></div><div class="stat"><b>'+R(ret-val)+'</b><span>Potential profit</span></div><div class="stat"><b style="color:'+(low.length?'var(--warn)':'var(--ok)')+'">'+low.length+'</b><span>Need reordering</span></div></div><h2>Reorder list</h2>'+
 (low.length?'<div class="tw"><table><thead><tr><th>Product</th><th>SKU</th><th class="r">In stock</th><th class="r">Reorder at</th><th class="r">Suggested order</th></tr></thead><tbody>'+low.map(function(i){return'<tr><td>'+esc(i.name)+'</td><td>'+esc(i.sku)+'</td><td class="r">'+pill(i)+' '+i.qty+'</td><td class="r">'+i.min+'</td><td class="r">'+(i.min*2-i.qty)+'</td></tr>'}).join('')+'</tbody></table></div><p class="note">Suggested order brings stock up to twice the reorder level.</p>':'<div class="card empty">Everything is above its reorder level.</div>')}
function stock(m){var q=(stock.q||'').toLowerCase(),list=D.items.filter(function(i){return(i.name+i.sku+i.cat).toLowerCase().indexOf(q)>-1});
 m.innerHTML='<div class="card"><h2>Add a product</h2><form class="g" id="f"><label>Name<input name="name" required></label><label>SKU<input name="sku" required></label><label>Category<input name="cat" list="cats"></label><label>Opening stock<input name="qty" type="number" min="0" value="0"></label><label>Reorder level<input name="min" type="number" min="0" value="5"></label><label>Cost price (R)<input name="cost" type="number" min="0" step="any" value="0"></label><label>Selling price (R)<input name="price" type="number" min="0" step="any" value="0"></label><button class="btn go">Add product</button></form><datalist id="cats">'+Array.from(new Set(D.items.map(function(i){return i.cat}))).map(function(c){return'<option value="'+esc(c)+'">'}).join('')+'</datalist><p class="err" id="e"></p></div>'+
 '<div class="row"><label class="sp"><span class="sr">Search products</span><input id="q" placeholder="Search name, SKU or category" value="'+esc(stock.q||'')+'"></label><button class="btn" id="x">Export CSV</button></div><div class="tw"><table><thead><tr><th>Product</th><th>SKU</th><th>Category</th><th class="r">Qty</th><th class="r">Cost</th><th class="r">Price</th><th>Status</th><th></th></tr></thead><tbody>'+
 (list.length?list.map(function(i){return'<tr><td>'+esc(i.name)+'</td><td>'+esc(i.sku)+'</td><td>'+esc(i.cat)+'</td><td class="r">'+i.qty+'</td><td class="r">'+R(i.cost)+'</td><td class="r">'+R(i.price)+'</td><td>'+pill(i)+'</td><td class="r"><button class="btn sm del" data-d="'+i.id+'" aria-label="Delete '+esc(i.name)+'">Delete</button></td></tr>'}).join(''):'<tr><td colspan="8" class="empty">No products match.</td></tr>')+'</tbody></table></div>';
 $('#f').onsubmit=function(e){e.preventDefault();var f=e.target,E=f.elements,sku=E.sku.value.trim().toUpperCase();
  if(D.items.some(function(i){return i.sku===sku})){$('#e').textContent='That SKU is already in use. Choose a different one.';return}
  var q=Math.max(0,Math.floor(+E.qty.value||0));D.items.push({id:uid(),sku:sku,name:E.name.value.trim(),cat:E.cat.value.trim()||'General',qty:q,min:Math.max(0,+E.min.value||0),cost:Math.max(0,+E.cost.value||0),price:Math.max(0,+E.price.value||0)});S();say('Product added');stock(m)};
 $('#q').oninput=function(e){stock.q=e.target.value;var p=e.target.selectionStart;stock(m);var n=$('#q');n.focus();n.setSelectionRange(p,p)};
 $('#x').onclick=function(){dl('inventory.csv',csv([['SKU','Name','Category','Qty','Reorder level','Cost','Price','Status']].concat(D.items.map(function(i){return[i.sku,i.name,i.cat,i.qty,i.min,i.cost,i.price,st(i)]}))))};
 $$('[data-d]',m).forEach(function(b){b.onclick=function(){if(confirm('Delete this product and its history?')){D.items=D.items.filter(function(i){return i.id!==b.dataset.d});D.log=D.log.filter(function(l){return l.item!==b.dataset.d});S();stock(m)}}})}
function move(m){m.innerHTML='<div class="card"><h2>Record a stock movement</h2><form class="g" id="f"><label>Product<select name="prod" required>'+(D.items.length?D.items.map(function(i){return'<option value="'+i.id+'">'+esc(i.name)+' ('+i.qty+' in stock)</option>'}).join(''):'<option value="">Add a product first</option>')+'</select></label><label>Movement<select name="type"><option value="in">Receive stock</option><option value="out">Issue or sell stock</option></select></label><label>Quantity<input name="qty" type="number" min="1" step="1" value="1" required></label><label>Note<input name="note" placeholder="Supplier, order number, reason"></label><button class="btn go">Record movement</button></form><p class="err" id="e"></p></div>';
 $('#f').onsubmit=function(e){e.preventDefault();var E=e.target.elements,p=it(E.prod.value);if(!p){$('#e').textContent='Add a product first.';return}
  var q=Math.floor(+E.qty.value);if(!(q>0)){$('#e').textContent='Enter a quantity of 1 or more.';return}
  if(E.type.value==='out'&&q>p.qty){$('#e').textContent='Only '+p.qty+' of '+p.name+' in stock. You cannot issue '+q+'.';return}
  p.qty+=E.type.value==='in'?q:-q;D.log.push({id:uid(),item:p.id,type:E.type.value,qty:q,date:today(),note:E.note.value.trim()});S();
  say((E.type.value==='in'?'Received ':'Issued ')+q+' of '+p.name);move(m);var s=st(p);$('#e').style.color=s==='ok'?'var(--ok)':'var(--warn)';$('#e').textContent=(E.type.value==='in'?'Received ':'Issued ')+q+' x '+p.name+'. Now '+p.qty+' in stock'+(s==='ok'?'.':s==='low'?'. This is at or below the reorder level.':'. Out of stock.')}}
function hist(m){m.innerHTML='<div class="tw"><table><thead><tr><th>Date</th><th>Product</th><th>Movement</th><th class="r">Qty</th><th>Note</th></tr></thead><tbody>'+(D.log.length?D.log.slice().reverse().map(function(l){var p=it(l.item);return'<tr><td>'+l.date+'</td><td>'+esc(p?p.name:'Deleted product')+'</td><td><span class="pill '+(l.type==='in'?'ok':'warn')+'">'+(l.type==='in'?'Received':'Issued')+'</span></td><td class="r">'+l.qty+'</td><td>'+esc(l.note)+'</td></tr>'}).join(''):'<tr><td colspan="5" class="empty">No movements yet. Record one in Receive and issue.</td></tr>')+'</tbody></table></div>'}
</script>
</body></html>
