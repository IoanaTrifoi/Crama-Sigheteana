(function(){
"use strict";
var PHONE="0755 674 569",EMAIL="cramasigheteana@yahoo.com";
function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}

// year
var y=$("#yr");if(y)y.textContent=new Date().getFullYear();

// mobile nav
var burger=$(".burger"),nav=$("#main-nav");
if(burger)burger.addEventListener("click",function(){var o=nav.classList.toggle("open");burger.setAttribute("aria-expanded",o)});

// reveal on scroll
var rv=$$(".section,.dish,.feat");rv.forEach(function(e){e.classList.add("reveal")});
if("IntersectionObserver" in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.08});
  rv.forEach(function(e){io.observe(e)});
}else rv.forEach(function(e){e.classList.add("in")});

// lightbox
var lb=$("#lightbox");
if(lb){
  document.addEventListener("click",function(e){
    var t=e.target;
    if(t.matches&&t.matches("[data-zoom]")){$("img",lb).src=t.src;$("img",lb).alt=t.alt;lb.hidden=false}
    else if(t===lb||t.closest&&t.closest("#lightbox button")){lb.hidden=true}
  });
  document.addEventListener("keydown",function(e){if(e.key==="Escape"){lb.hidden=true;closeCart()}});
}

// menu filter
var tabs=$("#tabs");
if(tabs){
  var dishes=$$(".dish"),blocks=$$("[data-block]");
  function applyFilter(f){
    $$(".tab",tabs).forEach(function(b){b.classList.toggle("is-on",b.dataset.filter===f)});
    dishes.forEach(function(d){d.classList.toggle("hide",!(f==="all"||d.dataset.cat===f))});
    var zil=$("#meniul-zilei-sec"),dsh=$('[data-block="dishes"]');
    if(f==="zilei"){dsh.classList.add("hide");zil.classList.remove("hide")}
    else{dsh.classList.remove("hide");zil.classList.toggle("hide",f!=="all")}
  }
  tabs.addEventListener("click",function(e){var b=e.target.closest(".tab");if(b)applyFilter(b.dataset.filter)});
  applyFilter(location.hash==="#meniul-zilei"?"zilei":"all");
}

// cart (localStorage cu fallback)
var cart={};
try{cart=JSON.parse(localStorage.getItem("crama-cart")||"{}")}catch(e){cart={}}
function save(){try{localStorage.setItem("crama-cart",JSON.stringify(cart))}catch(e){}}
var drawer=$("#cart-drawer"),bar=$("#cart-bar"),list=$("#cart-list");
function count(){return Object.keys(cart).reduce(function(s,k){return s+cart[k].q},0)}
function text(){return "Comandă Crama Sigheteană:\n"+Object.keys(cart).map(function(k){return "- "+cart[k].n+" x"+cart[k].q}).join("\n")}
function render(){
  if(!list)return;
  var n=count();$("#cart-count").textContent=n;bar.hidden=n===0;
  list.innerHTML="";
  Object.keys(cart).forEach(function(k){
    var li=document.createElement("li");
    li.innerHTML='<span></span><span class="qty"><button data-d="-1" data-k="'+k+'" aria-label="Mai puțin">−</button> <b>'+cart[k].q+'</b> <button data-d="1" data-k="'+k+'" aria-label="Mai mult">+</button></span>';
    li.firstChild.textContent=cart[k].n;list.appendChild(li);
  });
  $("#cart-mail").href="mailto:"+EMAIL+"?subject="+encodeURIComponent("Comandă")+"&body="+encodeURIComponent(text());
}
function openCart(){drawer.classList.add("open");drawer.setAttribute("aria-hidden","false")}
function closeCart(){if(drawer){drawer.classList.remove("open");drawer.setAttribute("aria-hidden","true")}}
if(drawer){
  document.addEventListener("click",function(e){
    var a=e.target.closest(".add-btn");
    if(a){var id=a.dataset.id;cart[id]=cart[id]||{n:a.dataset.name,q:0};cart[id].q++;save();render();a.textContent="✓ Adăugat";setTimeout(function(){a.textContent="+ Adaugă"},900)}
    var q=e.target.closest(".qty button");
    if(q){var k=q.dataset.k;cart[k].q+=+q.dataset.d;if(cart[k].q<=0)delete cart[k];save();render()}
  });
  $("#cart-open").addEventListener("click",openCart);
  $("#cart-close").addEventListener("click",closeCart);
  $("#cart-clear").addEventListener("click",function(){cart={};save();render();closeCart()});
  $("#cart-copy").addEventListener("click",function(){
    var t=text(),b=this;
    if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){b.textContent="Copiat ✓"});
    else{prompt("Copiază lista:",t)}
  });
  render();
}

// forms -> mailto (site static, fără server)
function bindForm(id,subject,lines){
  var f=document.getElementById(id);if(!f)return;
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var m=$(".form-msg",f),d=new FormData(f);
    if(!d.get("nume")||!d.get("telefon")||!f.elements.gdpr.checked){m.textContent="Completați numele, telefonul și bifați acordul.";return}
    var body=lines.map(function(l){return l[0]+": "+(d.get(l[1])||"-")}).join("\n");
    location.href="mailto:"+EMAIL+"?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent(body);
    m.style.color="var(--brown)";m.textContent="Se deschide aplicația de email. Dacă nu se deschide, scrieți-ne la "+EMAIL+" sau sunați la "+PHONE+".";
  });
}
bindForm("contact-form","Rezervare / mesaj de pe site",[["Nume","nume"],["Telefon","telefon"],["Data","data"],["Persoane","persoane"],["Mesaj","mesaj"]]);
bindForm("job-form","Aplicație job de pe site",[["Nume","nume"],["Telefon","telefon"],["Post","post"],["Mesaj","mesaj"]]);
})();
