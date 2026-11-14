(function(){
'use strict';
var doc=document, root=doc.documentElement;
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
var $=function(s,c){return (c||doc).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||doc).querySelectorAll(s))};

/* theme */
var themeNow=null;
$('#theme').addEventListener('click',function(){
  var cur=themeNow||root.dataset.theme;
  var dark=cur?cur==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;
  var next=dark?'light':'dark'; themeNow=next;
  if(doc.startViewTransition&&!reduce.matches&&doc.visibilityState==='visible'){var vt=doc.startViewTransition(function(){root.dataset.theme=themeNow});if(vt){[vt.ready,vt.finished,vt.updateCallbackDone].forEach(function(p){if(p)p.catch(function(){})})}}else{root.dataset.theme=next}
  try{localStorage.setItem('ck-theme',next)}catch(e){}
  syncTC(next);
});
var mqDark=window.matchMedia('(prefers-color-scheme: dark)');
function syncTC(t){
  t=typeof t==='string'?t:root.dataset.theme;
  var dark=t?t==='dark':mqDark.matches;
  var m=$('#tc'); if(m)m.setAttribute('content',dark?'#101c33':'#bfdcf7');
}
syncTC(); if(mqDark.addEventListener)mqDark.addEventListener('change',function(){syncTC()});

/* split headline into letters */
$$('[data-split]').forEach(function(el){
  var txt=el.textContent, k=0; el.setAttribute('aria-label',txt); el.textContent='';
  txt.split('').forEach(function(c){var s=doc.createElement('span');s.className='ch';s.setAttribute('aria-hidden','true');s.style.setProperty('--k',k++);s.textContent=c===' '?' ':c;el.appendChild(s)});
});

/* reveal on scroll (staggered) with fallbacks */
var targets=$$('.reveal,.split');
var anyShown=false;
function show(el){
  anyShown=true; el.classList.add('in');
  if(el.classList.contains('split'))return;
  var d=parseFloat(el.style.getPropertyValue('--d'))||0;
  setTimeout(function(){el.classList.remove('reveal','in');el.style.removeProperty('--d')},d+900);
}
if(!('IntersectionObserver' in window)){targets.forEach(show)}
else{
  var io=new IntersectionObserver(function(es){
    var n=0;
    es.forEach(function(en){
      if(!en.isIntersecting)return;
      en.target.style.setProperty('--d',Math.min(n++,6)*60+'ms');
      show(en.target); io.unobserve(en.target);
    });
  },{rootMargin:'0px 0px -8% 0px',threshold:.08});
  targets.forEach(function(t){io.observe(t)});
  /* safety net: if nothing ever fires, don't leave content hidden */
  setTimeout(function(){ if(!anyShown) targets.forEach(show); },2500);
}

/* scroll: progress bar, parallax clouds, nav state */
var bar=$('#bar'), clouds=$$('.cl'), nav=$('#nav'), ticking=false;
function onScroll(){
  if(ticking)return; ticking=true;
  requestAnimationFrame(function(){
    var y=window.scrollY||0, h=root.scrollHeight-window.innerHeight;
    bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
    if(!reduce.matches) clouds.forEach(function(c){c.style.transform='translate3d(0,'+(-y*parseFloat(c.dataset.p)).toFixed(1)+'px,0)'});
    nav.classList.toggle('is-scrolled',y>window.innerHeight*.55);
    nav.classList.toggle('is-stuck',y>12);
    ticking=false;
  });
}
window.addEventListener('scroll',onScroll,{passive:true}); onScroll();

/* scroll-spy + sliding indicator */
var links=$$('#links a'), ind=$('#ind'), linksWrap=$('#links');
var spyMap={}; links.forEach(function(a){spyMap[a.getAttribute('href').slice(1)]=a});
var current=null;
function moveInd(a){
  if(!a||a.offsetParent===null){ind.classList.remove('is-on');return}
  var fresh=!ind.classList.contains('is-on');
  if(fresh)ind.classList.add('no-t');
  ind.style.width=a.offsetWidth+'px';
  ind.style.transform='translateX('+a.offsetLeft+'px)';
  ind.classList.add('is-on');
  if(fresh){void ind.offsetWidth;ind.classList.remove('no-t')}
}
function setCurrent(id){
  current=id;
  links.forEach(function(a){a.removeAttribute('aria-current')});
  var a=spyMap[id]; if(a)a.setAttribute('aria-current','location');
  moveInd(a);
}
if('IntersectionObserver' in window){
  var spy=new IntersectionObserver(function(es){
    es.forEach(function(en){ if(en.isIntersecting) setCurrent(en.target.id); });
  },{rootMargin:'-45% 0px -50% 0px'});
  $$('[data-spy]').forEach(function(s){spy.observe(s)});
  var hero=$('#top'); new IntersectionObserver(function(es){ if(es[0].isIntersecting){current=null;links.forEach(function(a){a.removeAttribute('aria-current')});ind.classList.remove('is-on')} },{rootMargin:'-45% 0px -50% 0px'}).observe(hero);
}
window.addEventListener('resize',function(){moveInd(spyMap[current])});
if(doc.fonts&&doc.fonts.ready)doc.fonts.ready.then(function(){moveInd(spyMap[current])});

/* feature screenshots: thumbs swap frames */
$$('[data-frames]').forEach(function(box){
  var shots=$$('.shot',box), th=$$('.thumb',box);
  th.forEach(function(b){b.addEventListener('click',function(){
    var i=+b.dataset.frame;
    shots.forEach(function(s,j){s.classList.toggle('is-on',j===i)});
    th.forEach(function(t,j){t.classList.toggle('is-on',j===i);t.setAttribute('aria-pressed',j===i?'true':'false')});
  })});
});

/* 3D tilt */
if(window.matchMedia('(hover: hover) and (pointer: fine)').matches){
  $$('[data-tilt]').forEach(function(t){
    var tx=0,ty=0,cx=0,cy=0,raf=0,br=t.querySelector('.browser');
    function loop(){
      cx+=(tx-cx)*.12; cy+=(ty-cy)*.12;
      br.style.setProperty('--ry',cx.toFixed(2)+'deg'); br.style.setProperty('--rx',cy.toFixed(2)+'deg');
      if(Math.abs(tx-cx)>.02||Math.abs(ty-cy)>.02)raf=requestAnimationFrame(loop); else raf=0;
    }
    t.addEventListener('pointermove',function(e){
      if(reduce.matches)return;
      var r=t.getBoundingClientRect(), px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
      tx=(px-.5)*9; ty=-(py-.5)*7;
      t.style.setProperty('--gx',(px*100)+'%'); t.style.setProperty('--gy',(py*100)+'%'); t.classList.add('is-hot');
      if(!raf)raf=requestAnimationFrame(loop);
    });
    t.addEventListener('pointerleave',function(){tx=0;ty=0;t.classList.remove('is-hot');if(!raf)raf=requestAnimationFrame(loop)});
  });
}

/* filter with FLIP */
var grid=$('#grid'), tiles=$$('.tile',grid), fbtns=$$('.fbtn');
var curCat='all', expanded=false, moreWrap=$('#morewrap'), moreBtn=$('#more');
function syncCollapse(){
  var c=curCat==='all'&&!expanded;
  grid.classList.toggle('is-collapsed',c);
  moreWrap.hidden=curCat!=='all';
  $('#moren').textContent=expanded?'Show fewer':'Show all '+tiles.length;
  $('#morea').textContent=expanded?'\u2191':'\u2193';
  moreBtn.setAttribute('aria-expanded',expanded?'true':'false');
}
fbtns.forEach(function(b){
  var n=b.dataset.f==='all'?tiles.length:tiles.filter(function(t){return t.dataset.cat===b.dataset.f}).length;
  var sm=doc.createElement('small'); sm.textContent=n; b.appendChild(sm);
});
syncCollapse();
moreBtn.addEventListener('click',function(){
  if(expanded){
    expanded=false; syncCollapse();
    var sh=$('#shelf'); if(sh.getBoundingClientRect().top<0) sh.scrollIntoView({block:'start',behavior:reduce.matches?'auto':'smooth'});
    return;
  }
  var was=tiles.filter(vis);
  expanded=true; syncCollapse();
  if(reduce.matches||!tiles[0].animate)return;
  var n=0;
  tiles.forEach(function(t){
    if(was.indexOf(t)>-1||!vis(t))return;
    t.animate([{opacity:0,transform:'translateY(18px) scale(.97)'},{opacity:1,transform:'none'}],{duration:620,delay:Math.min(n++,12)*35,easing:'cubic-bezier(.2,.8,.2,1)',fill:'backwards'});
  });
});

/* featured switcher: one stage, three builds */
(function(){
  var tabs=$$('.ftab'), panels=$$('[data-fp]');
  if(!tabs.length)return;
  function pick(i,focus){
    tabs.forEach(function(t,j){t.setAttribute('aria-selected',j===i?'true':'false');t.tabIndex=j===i?0:-1});
    panels.forEach(function(p,j){p.hidden=j!==i});
    if(focus)tabs[i].focus();
    var p=panels[i];
    if(!reduce.matches&&p.animate){
      p.querySelector('.feat__media').animate([{opacity:0,transform:'translateY(16px) scale(.985)'},{opacity:1,transform:'none'}],{duration:620,easing:'cubic-bezier(.2,.8,.2,1)'});
      p.querySelector('.feat__copy').animate([{opacity:0,transform:'translateY(10px)'},{opacity:1,transform:'none'}],{duration:620,delay:70,easing:'cubic-bezier(.2,.8,.2,1)',fill:'backwards'});
    }
  }
  panels.forEach(function(p,j){p.setAttribute('role','tabpanel');p.hidden=j!==0});
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){pick(i)});
    t.addEventListener('keydown',function(e){
      var k=e.key, n=tabs.length;
      if(k==='ArrowRight'){e.preventDefault();pick((i+1)%n,true)}
      else if(k==='ArrowLeft'){e.preventDefault();pick((i+n-1)%n,true)}
    });
  });
})();

setTimeout(function(){root.classList.add('intro-done')},2600);

/* build board caption */
(function(){
  var cap=$('#boardcap'), items=$$('.bt');
  if(!cap||!items.length)return;
  var live=items.filter(function(a){return a.classList.contains('is-live')}).length;
  var key=$('.board__k');
  if(key){key.lastChild.textContent=live+' live'}
  function idle(){cap.textContent=items.length+' builds, '+live+' of them live. Pick one to read how it was made.'}
  function show(a){
    cap.textContent='';
    if(a.classList.contains('is-live')){var d=doc.createElement('i'); d.className='dot dot--still'; cap.appendChild(d)}
    var b=doc.createElement('b'); b.textContent=a.querySelector('.bt__n').textContent;
    cap.appendChild(b); cap.appendChild(doc.createTextNode('  '+a.dataset.cap));
  }
  items.forEach(function(a){
    a.addEventListener('pointerenter',function(){show(a)});
    a.addEventListener('focus',function(){show(a)});
    a.addEventListener('pointerleave',idle);
    a.addEventListener('blur',idle);
  });
  idle();
})();

function vis(el){return !el.hidden&&el.offsetParent!==null}
function filter(cat){
  var first=new Map(); tiles.forEach(function(t){if(vis(t))first.set(t,t.getBoundingClientRect())});
  tiles.forEach(function(t){t.hidden=!(cat==='all'||t.dataset.cat===cat)});
  curCat=cat; syncCollapse();
  if(reduce.matches||!tiles[0].animate)return;
  var n=0;
  tiles.forEach(function(t){
    if(!vis(t))return;
    var f=first.get(t), l=t.getBoundingClientRect();
    if(f){
      var dx=f.left-l.left, dy=f.top-l.top;
      if(Math.abs(dx)>1||Math.abs(dy)>1) t.animate([{transform:'translate('+dx+'px,'+dy+'px)'},{transform:'none'}],{duration:620,easing:'cubic-bezier(.2,.8,.2,1)'});
    }else{
      t.animate([{opacity:0,transform:'translateY(18px) scale(.97)'},{opacity:1,transform:'none'}],{duration:620,delay:Math.min(n++,8)*45,easing:'cubic-bezier(.2,.8,.2,1)',fill:'backwards'});
    }
  });
}
fbtns.forEach(function(b){b.addEventListener('click',function(){
  fbtns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
  filter(b.dataset.f);
})});

/* email assembled in JS (same approach as the live site) */
var addr='';
$$('[data-user][data-domain]').forEach(function(a){
  addr=a.dataset.user+'@'+a.dataset.domain;
  a.href='mailto:'+addr;
  if(a.hasAttribute('data-show'))a.textContent=addr;
});
var cp=$('[data-copy]'), msg=$('#copied'), cpT=0, mailA=$('.mail a');
cp.addEventListener('click',function(){
  function done(ok){
    clearTimeout(cpT);
    msg.textContent='';
    /* re-set on the next tick so repeat copies are announced again */
    setTimeout(function(){msg.textContent=ok?'Copied '+addr:'Copy failed. The address is shown here: '+addr},30);
    if(ok)cp.setAttribute('data-state','copied');
    else if(mailA&&window.getSelection){try{var r=doc.createRange();r.selectNodeContents(mailA);var sel=window.getSelection();sel.removeAllRanges();sel.addRange(r)}catch(e){}}
    cpT=setTimeout(function(){msg.textContent='';cp.removeAttribute('data-state')},2600);
  }
  if(!addr){done(false);return}
  function legacy(){try{var t=doc.createElement('textarea');t.value=addr;t.setAttribute('readonly','');t.style.cssText='position:fixed;top:0;left:0;opacity:0';doc.body.appendChild(t);t.select();t.setSelectionRange(0,addr.length);var ok=doc.execCommand('copy');doc.body.removeChild(t);done(ok)}catch(e){done(false)}}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(addr).then(function(){done(true)},legacy)}
  else legacy();
});

/* magnetic button */
if(window.matchMedia('(hover: hover) and (pointer: fine)').matches){
  $$('[data-mag]').forEach(function(m){
    var b=m.firstElementChild,x=0,y=0,cx=0,cy=0,raf=0;
    function loop(){cx+=(x-cx)*.15;cy+=(y-cy)*.15;b.style.transform='translate3d('+cx.toFixed(1)+'px,'+cy.toFixed(1)+'px,0)';if(Math.abs(x-cx)>.1||Math.abs(y-cy)>.1)raf=requestAnimationFrame(loop);else raf=0}
    window.addEventListener('pointermove',function(e){
      if(reduce.matches)return;
      var r=m.getBoundingClientRect(), mx=r.left+r.width/2, my=r.top+r.height/2, dx=e.clientX-mx, dy=e.clientY-my;
      var d=Math.hypot(dx,dy);
      if(d<170){x=dx*.35;y=dy*.35}else{x=0;y=0}
      if(!raf)raf=requestAnimationFrame(loop);
    },{passive:true});
  });
}

/* Berkeley clock */
var clock=$('#clock');
function tick(){try{clock.textContent=new Intl.DateTimeFormat('en-US',{hour:'numeric',minute:'2-digit',timeZone:'America/Los_Angeles'}).format(new Date())}catch(e){}}
tick(); setInterval(tick,30000);
})();
