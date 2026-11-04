// ---------- P11: "rich clients need more than ads" reel ----------
// ---------- SUBTITLES ----------
const FULL=[[5.90,11.75],[13.00,18.00],[25.56,30.00],[33.90,40.00],[42.70,47.04]];
const isFull=t=>FULL.some(([a,b])=>t>=a&&t<b);
const SUB_Y=t=>isFull(t)?0.87:t<6.4?0.58:t<25.56?0.585:t<40?0.66:t<47.04?0.62:0.72;
const CARDS=[
 [0.00,1.40,[['b',[['думаете,',0.00]]],['s',[['добавили',0.50],['в',1.00],['таргет',1.14]]]]],
 [1.40,2.50,[['r',[['rolex,',1.40],['яхты',1.92]]],['s',[['и',2.40]]]]],
 [2.50,3.56,[['r',[['rolls-royce',2.50]]],['s',[['и',2.96],['всё,',3.22]]]]],
 [3.56,4.94,[['s',[['получили',3.56]]],['b',[['богатых',4.00],['клиентов?',4.36]]]]],
 [4.94,6.34,[['b',[['ага,',4.94],['конечно',5.48]]]]],
 [6.34,7.86,[['b',[['интересоваться',6.34]]],['s',[['дорогими',6.98],['вещами',7.38]]]]],
 [7.86,9.56,[['s',[['и',7.86],['быть',8.14],['готовым',8.32],['за',8.86],['них']]],['r',[['платить',9.06]]]]],
 [9.56,11.96,[['s',[['это',9.56],['две',10.00],['совершенно',10.18]]],['b',[['разные',10.64],['истории',11.14]]]]],
 [11.96,13.42,[['b',[['представьте,',11.96]]],['s',[['у',12.62],['вас',12.90],['салон',13.06]]]]],
 [13.42,15.00,[['s',[['дорогой',13.42]]],['b',[['мебели',13.76]]],['s',[['качественные',14.20]]]]],
 [15.00,16.90,[['b',[['материалы',15.00]]],['s',[['отличная',15.72],['фурнитура',16.22]]]]],
 [16.90,18.12,[['s',[['идеальная',16.90]]],['r',[['сборка',17.48]]]]],
 [18.12,19.74,[['s',[['а',18.12],['в',18.58],['instagram',18.60]]],['b',[['фотографии',19.10]]],['s',[['на',19.66],['телефон',19.74]]]]],
 [19.74,21.72,[['b',[['сайт',20.30]]],['r',[['2000-х',20.66]]],['s',[['годов',21.20]]]]],
 [21.72,23.20,[['b',[['непонятные',21.72]]],['s',[['предложения',22.34],['и',23.00]]]]],
 [23.20,25.34,[['b',[['сообщения,',23.20]]],['s',[['на',23.80],['которые',23.92],['отвечают',24.12],['через',24.60]]],['r',[['сутки',24.78]]]]],
 [25.34,26.82,[['s',[['и',25.34],['вот',25.66]]],['b',[['вопрос',25.78]]],['s',[['почему',26.34]]]]],
 [26.82,28.26,[['s',[['клиент',26.82],['должен']]],['b',[['доверить',27.62]]],['s',[['вам',28.12]]]]],
 [28.26,30.00,[['s',[['несколько',28.26]]],['r',[['тысяч',28.68],['долларов?',29.12]]]]],
 [30.00,31.70,[['s',[['хотите',30.00],['привлекать',30.34],['клиентов',30.78],['с',31.18]]],['b',[['высоким',31.32],['чеком?',31.70]]]]],
 [31.70,34.08,[['s',[['тогда',32.08],['работайте',32.56]]],['b',[['не',33.00],['только',33.18]]],['s',[['над',33.40],['рекламой',33.60]]]]],
 [34.08,35.58,[['s',[['нужны',34.08],['сильная',34.56]]],['b',[['упаковка',34.96]]]]],
 [35.58,36.72,[['s',[['качественный',35.58]]],['b',[['контент',36.14]]]]],
 [36.72,38.12,[['s',[['понятное',36.72]]],['b',[['позиционирование',37.34]]]]],
 [38.12,39.82,[['s',[['и',38.12],['нормальная',38.26]]],['b',[['обработка',38.78]]],['s',[['заявок',39.32]]]]],
 [39.82,41.34,[['s',[['потому',39.82],['что',40.18]]],['b',[['реклама',40.42]]],['s',[['лишь',41.08]]]]],
 [41.34,43.38,[['b',[['приводит',41.34]]],['s',[['человека',41.90],['к',42.14],['вашему',42.40],['предложению',42.68]]]]],
 [43.38,45.08,[['s',[['а',43.38],['вот',43.72]]],['r',[['убедить',43.86]]],['s',[['его',44.32],['купить',44.50]]]]],
 [45.08,46.84,[['s',[['задача',45.08],['всей',45.64],['остальной',45.80]]],['b',[['системы',46.26]]]]],
 [46.84,48.98,[['s',[['поэтому,',46.84],['прежде',47.34],['чем',47.88],['увеличивать',48.04]]],['b',[['бюджет',48.98]]]]],
 [48.98,50.94,[['r',[['убедитесь,',49.40]]],['s',[['что',50.14],['ваш',50.38],['бизнес',50.60]]]]],
 [50.94,52.38,[['b',[['готов',50.94]]],['s',[['к',51.34],['этим',51.62],['клиентам',51.76]]]]],
 [52.38,54.10,[['s',[['а',52.38],['если',52.78],['не',52.96],['знаете,',53.10],['с',53.36],['чего']]],['b',[['начать',53.62]]]]],
 [54.10,55.30,[['b',[['напишите',54.10]]],['s',[['мне',54.60],['в',54.74]]],['r',[['direct',54.86]]]]],
 [55.30,56.78,[['b',[['разберём',55.30]]],['s',[['вашу',55.90],['ситуацию',56.12]]]]],
 [56.78,59.10,[['s',[['и',56.60],['обсудим,',56.78],['как',57.24],['привлечь',57.52]]],['b',[['больше',57.96],['клиентов',58.12]]]]],
];
const cardEls=[];
(function(){const R=$('subs');
 for(const c of CARDS){const ce=el('div','card',R);const words=[];
  for(const L of c[2]){if(typeof L!=='object')continue;const le=el('div','line l'+L[0],ce);let last=c[0];
   for(const [txt,at] of L[1]){const w=el('span','w',le);w.textContent=L[0]==='s'?txt.toLowerCase():txt.toUpperCase();const a=at===undefined?last+.1:at;last=a;words.push([w,a])}}
  cardEls.push({c,ce,words})}})();
function renderSubs(t){const y=SUB_Y(t)*1280;
 for(const k of cardEls){const on=t>=k.c[0]&&t<k.c[1];k.ce.style.display=on?'flex':'none';if(!on)continue;k.ce.style.top=y+'px';
  for(const [w,at] of k.words)applyPop(w,t,at,'',.15,.55)}}

// ================= FACE OVERLAYS =================
const OV={};
(function(){const S=mkOv('ov');OV.S=S;
 // A 0–5.9: targeting interests (head top ≈ 340px)
 OV.tg=el('div','abs',S,Object.assign({left:'60px',top:'40px',width:'600px',height:'150px',borderRadius:'26px'},skyGlass));
 OV.tg.innerHTML=`<div style="position:absolute;left:24px;top:18px;font:800 17px/1 Mont,${EMO};color:#fff">🎯 Таргетинг · интересы</div>`;
 OV.ti=['⌚ Rolex','🛥 Яхты','🚗 Rolls-Royce'].map((x,i)=>{const c=el('div','abs',OV.tg,{left:[20,192,350][i]+'px',top:'60px',height:'60px',padding:'0 18px',borderRadius:'30px',background:'rgba(255,178,30,.22)',border:`1px solid ${ACC}`,color:'#fff',font:`800 21px/58px Mont,${EMO}`,whiteSpace:'nowrap',boxSizing:'border-box'});c.textContent=x;return c});
 OV.rich=skyChip(S,206,`= 💎 Богатые клиенты?`);
 OV.richX=el('div','abs',OV.rich,{left:'14px',right:'14px',top:'27px',height:'6px',borderRadius:'3px',background:RED,transformOrigin:'0 50%',transform:'scaleX(0)'});
 OV.eye=el('div','abs',S,{left:'560px',top:'190px',font:`70px/1 ${EMO}`});OV.eye.textContent='🙄';
 // C1 11.75–13: salon chip (head top ≈ 230)
 OV.sal=skyChip(S,50,`🛋 Салон дорогой мебели`);
 // C2 18–25.56: 4 problem cards at the bottom
 OV.pc=[];const PC=[['📱','Фото на телефон',19.10],['🌐','Сайт из 2000-х',20.30],['❓','Непонятный оффер',21.72],['💬','Ответ через сутки',23.20]];
 PC.forEach(([ico,tt,at],i)=>{const x=40+(i%2)*326,y=846+Math.floor(i/2)*196;const c=el('div','frost abs',S,{left:x+'px',top:y+'px',width:'314px',height:'180px',borderRadius:'22px',overflow:'hidden'});
  let vis='';
  if(i===0)vis=`<div style="position:absolute;left:16px;top:56px;width:282px;height:104px;border-radius:12px;background:linear-gradient(135deg,#a58f78,#6d5a4a);filter:blur(6px)"></div><div style="position:absolute;left:30px;top:70px;width:120px;height:70px;border-radius:8px;background:#c9b49a;filter:blur(5px)"></div>`;
  if(i===1)vis=`<div style="position:absolute;left:16px;top:56px;width:282px;height:104px;border-radius:4px;background:linear-gradient(180deg,#0000aa,#5555ff 30%,#c0c0c0 30%);border:2px outset #ddd;box-sizing:border-box"><div style="position:absolute;left:8px;top:4px;font:700 14px/1 'Times New Roman',serif;color:#ff0;font-style:italic">Добро пожаловать!!!</div><div style="position:absolute;left:8px;top:40px;font:400 13px/1.3 'Times New Roman',serif;color:#00e;text-decoration:underline">Главная | Каталог | Гостевая</div><div style="position:absolute;right:8px;bottom:6px;font:400 11px/1 'Times New Roman',serif;color:#000">Посетителей: 000127</div></div>`;
  if(i===2)vis=`<div style="position:absolute;left:16px;top:58px;width:282px;font:800 19px/1.3 Mont;color:#fff">Звоните!!! Цены договорные. Скидки есть???</div>`;
  if(i===3)vis=`<div style="position:absolute;left:16px;top:60px;padding:10px 14px;border-radius:16px 16px 16px 4px;background:rgba(255,255,255,.14);color:#e9eaee;font:700 15px/1 Mont">Добрый день, сколько стоит?</div><div class="clk" style="position:absolute;right:16px;bottom:16px;font:800 30px/1 Mont;color:#ff8b8b"></div>`;
  c.innerHTML=`<div style="position:absolute;left:16px;top:16px;font:800 18px/1 Mont,${EMO};color:#fff;white-space:nowrap">${ico} ${tt}</div>${vis}`;
  const x_=xBadge(c,262,10);OV.pc.push({c,at,x:x_,clk:c.querySelector('.clk')})});
 // E 30–33.9: high ticket (head top ≈ 420)
 OV.hi=skyChip(S,90,`💎 Клиенты с высоким чеком`);
 OV.nr=el('div','abs',S,Object.assign({left:'110px',top:'176px',width:'500px',height:'150px',borderRadius:'26px'},skyGlass));
 OV.nr.innerHTML=`<div style="position:absolute;left:24px;top:22px;font:800 18px/1 Mont;color:#fff">Работать не только над рекламой</div>
  <div style="position:absolute;left:24px;top:66px;display:flex;gap:10px;font:800 20px/56px Mont,${EMO};color:#fff"><div style="height:56px;padding:0 18px;border-radius:28px;background:rgba(255,255,255,.14)">📣 Реклама</div><div style="color:${ACC};font-size:34px">+</div><div id="nrq" style="height:56px;padding:0 18px;border-radius:28px;background:rgba(255,178,30,.25);border:1px solid ${ACC}">ещё 4 вещи</div></div>`;
 // F 40–42.7: ads → person → offer (head top ≈ 270)
 OV.fl=[['📣 Реклама',40.42],['👤',41.34],['🎁 Предложение',42.68]].map(([x,at],i)=>{const c=el('div','abs',S,Object.assign({left:[40,300,420][i]+'px',top:'60px',height:'70px',padding:'0 22px',borderRadius:'35px',color:'#fff',font:`800 22px/70px Mont,${EMO}`,whiteSpace:'nowrap'},skyGlass));c.textContent=x;return{c,at}});
 OV.fa=[0,1].map(i=>{const a=el('div','abs',S,{left:[240,370][i]+'px',top:'72px',font:'600 44px/1 Osw',color:ACC});a.textContent='→';return a});
 // G1 47–52.3: checklist before scaling budget (head top ≈ 470)
 OV.ck=el('div','abs',S,Object.assign({left:'70px',top:'50px',width:'580px',height:'360px',borderRadius:'28px'},skyGlass));
 OV.ck.innerHTML=`<div style="position:absolute;left:24px;top:22px;font:800 19px/1 Mont;color:#fff">Прежде чем увеличить бюджет</div>
  <div id="bud" style="position:absolute;right:20px;top:14px;height:40px;padding:0 14px;border-radius:20px;background:rgba(255,255,255,.14);font:800 16px/40px Mont,${EMO};color:#fff">📈 Бюджет <span id="lock">🔒</span></div>`;
 OV.ci=['Упаковка','Контент','Позиционирование','Обработка заявок'].map((x,i)=>{const r=el('div','abs',OV.ck,{left:'20px',top:(70+i*56)+'px',width:'540px',height:'46px',borderRadius:'14px',background:'rgba(255,255,255,.1)'});
  r.innerHTML=`<div class="cb" style="position:absolute;left:10px;top:7px;width:32px;height:32px;border-radius:9px;border:2px solid rgba(255,255,255,.5);box-sizing:border-box;color:#111;font:800 18px/28px Mont;text-align:center"></div><div style="position:absolute;left:56px;top:0;font:700 18px/46px Mont;color:#fff">${x}</div>`;return r.querySelector('.cb')});
 OV.rd=el('div','abs',OV.ck,{left:'20px',top:'296px',width:'540px',height:'48px',borderRadius:'14px',background:'rgba(46,204,113,.3)',border:'1px solid rgba(46,204,113,.8)',boxSizing:'border-box',color:'#fff',font:'800 19px/46px Mont',textAlign:'center'});OV.rd.textContent='✓ Бизнес готов к этим клиентам';
 // G2/G3 52.3–end
 OV.st=skyChip(S,60,`🤔 Не знаете, с чего начать?`);
 OV.dm=el('div','frost abs',S,{left:'70px',top:'50px',width:'580px',height:'370px',borderRadius:'30px'});
 OV.dm.innerHTML=`<div style="position:absolute;left:22px;top:20px;width:52px;height:52px;border-radius:50%;padding:3px;background:conic-gradient(#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5,#feda75);box-sizing:border-box"><img src="assets/vadim.jpg" style="width:46px;height:46px;border-radius:50%;object-fit:cover;border:3px solid #141519;box-sizing:border-box"></div>
  <div style="position:absolute;left:88px;top:24px;font:800 19px/1 Mont;color:#fff">zaslavskuy</div><div style="position:absolute;left:88px;top:50px;font:600 14px/1 Mont;color:#9a9ba3">Direct</div>
  <div id="dmb" style="position:absolute;right:22px;top:96px;max-width:420px;padding:14px 18px;border-radius:22px 22px 6px 22px;background:linear-gradient(135deg,#7b3fe4,#d62976);color:#fff;font:700 18px/1.35 Mont"></div>
  <div id="dmr" style="position:absolute;left:22px;top:170px;max-width:440px;padding:14px 18px;border-radius:22px 22px 22px 6px;background:rgba(255,255,255,.14);color:#fff;font:700 18px/1.35 Mont,${EMO}">Разберём вашу ситуацию и обсудим, как привлечь больше клиентов 🚀</div>
  <div style="position:absolute;left:22px;right:22px;bottom:20px;height:52px;border-radius:26px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18)"><div id="dmi" style="position:absolute;left:20px;top:0;font:600 17px/52px Mont;color:#e9eaee;white-space:pre"></div>
   <div id="dms" style="position:absolute;right:6px;top:6px;width:40px;height:40px;border-radius:50%;background:#3797f0;color:#fff;font:800 20px/40px Mont;text-align:center">➤</div></div>`;
})();
function renderOV(t){OV.S.style.display=isFull(t)?'none':'block';if(isFull(t))return;
 const show=(e,a,b,tr,from=.6,i=0)=>{const on=t>=a&&t<b;e.style.display=on?'block':'none';if(!on)return false;applyPop(e,t,a,tr||'',.28,from);floatOut(e,t,eInOut(lin(t,b-.3,b)),i);return true};
 // A
 if(show(OV.tg,0.50,5.90,'',.7)){OV.ti.forEach((c,i)=>applyPop(c,t,[1.40,1.92,2.60][i],'',.24,.4))}
 show(OV.rich,3.56,5.90,'translateX(-50%)',.6,1);OV.richX.style.transform=`scaleX(${eOut(lin(t,5.48,5.66))})`;
 show(OV.eye,4.94,5.90,'rotate(-8deg)',.3,2);
 show(OV.sal,12.62,13.00,'translateX(-50%)',.6);if(t>=11.75&&t<12.62)OV.sal.style.display='none';
 // C2
 OV.pc.forEach(({c,at,x,clk},i)=>{if(!show(c,at,25.56,'',.7,i))return;applyPop(x,t,at+.35,'',.2,.3);
  if(clk){const h=Math.round(24*eOut(lin(t,23.92,24.80)));clk.textContent=t>=23.92?h+' ч':''}});
 // E
 show(OV.hi,31.32,33.90,'translateX(-50%)',.6);show(OV.nr,33.00,33.90,'',.75,1);
 // F
 OV.fl.forEach(({c,at},i)=>show(c,at,42.70,'',.5,i));OV.fa.forEach((a,i)=>show(a,[41.10,42.40][i],42.70,'',.4,i));
 // G1
 if(show(OV.ck,47.34,52.30,'',.8)){OV.ci.forEach((cb,i)=>{const at=49.40+i*.34,ok=t>=at;cb.style.background=ok?ACC:'transparent';cb.style.borderColor=ok?ACC:'rgba(255,255,255,.5)';cb.textContent=ok?'✓':'';if(ok)cb.style.transform=`scale(${.6+.4*eBack(lin(t,at,at+.2))})`});
  applyPop(OV.rd,t,51.76,'',.24,.6);$('lock').textContent=t>=51.90?'🔓':'🔒';$('bud').style.background=t>=51.90?'rgba(46,204,113,.35)':'rgba(255,255,255,.14)';if(t>=51.9&&t<52.1)$('bud').style.transform=`scale(${1+.15*Math.sin(lin(t,51.9,52.1)*Math.PI)})`}
 show(OV.st,52.38,54.10,'translateX(-50%)',.6);
 if(show(OV.dm,54.10,59.10,'',.85)){const msg='Хочу разбор своей ситуации';$('dmi').textContent=t<55.10?typed(msg,t,54.40,55.00)+(Math.floor(t*6)%2?'|':''):'Сообщение…';
  const sent=t>=55.20;$('dmb').style.display=sent?'block':'none';$('dmb').textContent=msg;if(sent){const q=lin(t,55.20,55.45);$('dmb').style.opacity=clamp(q*2);$('dmb').style.transform=`translateY(${(1-eBack(q))*30}px)`}
  $('dms').style.transform=t>=55.08&&t<55.22?'scale(.85)':'none';const rq=lin(t,56.60,56.90);$('dmr').style.display=t>=56.60?'block':'none';$('dmr').style.opacity=clamp(rq*2);$('dmr').style.transform=`translateY(${(1-eBack(rq))*30}px)`}
}

// ================= FULL SCENES =================
// F1 5.90–11.75: interested ≠ ready to pay
const F1={p:[]};
(function(){const S=mkScene('f1','v3bg');F1.S=S;
 F1.h=head(S,`Интересуются ≠ ${A_('платят')}`,100);
 const c=glassBox(S,40,210,640,560);F1.c=c;
 const gold=[9,26,38];
 for(let i=0;i<48;i++){const x=36+(i%8)*72,y=34+Math.floor(i/8)*84;const p=el('div','abs',c,{left:x+'px',top:y+'px',width:'60px',height:'70px'});
  p.innerHTML=`<svg width="60" height="70" viewBox="0 0 60 70"><circle cx="30" cy="20" r="13" fill="currentColor"/><path d="M6 68 C6 46 18 38 30 38 C42 38 54 46 54 68 Z" fill="currentColor"/></svg>`;p.style.color='#2c2d33';F1.p.push({p,gold:gold.includes(i)})}
 F1.l1=el('div','abs',S,{left:'50%',top:'800px',height:'60px',padding:'0 24px',borderRadius:'30px',background:'rgba(255,255,255,.1)',border:'1px solid rgba(255,255,255,.3)',color:'#fff',font:`800 21px/60px Mont,${EMO}`,whiteSpace:'nowrap'});F1.l1.innerHTML='👀 Интересуются люксом: <b>48</b>';
 F1.l2=el('div','abs',S,{left:'50%',top:'878px',height:'60px',padding:'0 24px',borderRadius:'30px',background:'rgba(255,178,30,.18)',border:`1px solid ${ACC}`,color:'#fff',font:`800 21px/60px Mont,${EMO}`,whiteSpace:'nowrap'});F1.l2.innerHTML=`💳 Готовы платить: <b style="color:${ACC}">3</b>`;
})();
function renderF1(t){if(!vis(F1.S,t,5.90,11.75))return;
 applyPop(F1.h,t,6.00,'',.26,.6);applyPop(F1.c,t,6.10,'',.28,.85);
 F1.p.forEach(({p,gold},i)=>{const lit=t>=6.34+(i%8)*.05+Math.floor(i/8)*.05;const g=gold&&t>=8.32;const dim=t>=8.32&&!gold;
  p.style.color=g?ACC:lit?(dim?'#3a3b42':'#e9eaee'):'#2c2d33';p.style.filter=g?`drop-shadow(0 0 10px ${ACC})`:'none';if(g)p.style.transform=`scale(${1+.15*eBack(lin(t,8.32,8.6))})`});
 applyPop(F1.l1,t,7.38,'translateX(-50%)',.24,.6);applyPop(F1.l2,t,9.06,'translateX(-50%)',.24,.6);
 if(t>=10.64){F1.h.innerHTML=`Две ${A_('разные истории')}`;applyPop(F1.h,t,10.64,'',.24,.7)}else F1.h.innerHTML=`Интересуются ≠ ${A_('платят')}`;
}
// F2 13.00–18.00: premium product
const F2={};
(function(){const S=mkScene('f2','v3bg');F2.S=S;
 F2.h=head(S,`Продукт — ${A_('премиум')}`,100);
 const c=glassBox(S,60,210,600,330);F2.c=c;
 c.innerHTML=`<svg width="520" height="230" viewBox="0 0 520 230" style="position:absolute;left:40px;top:40px">
  <defs><linearGradient id="sofa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9c2a3"/><stop offset="1" stop-color="#a88c6b"/></linearGradient></defs>
  <ellipse cx="260" cy="214" rx="230" ry="10" fill="rgba(0,0,0,.4)"/>
  <rect x="60" y="40" width="400" height="100" rx="30" fill="url(#sofa)"/><rect x="20" y="90" width="80" height="110" rx="30" fill="#c4a984"/><rect x="420" y="90" width="80" height="110" rx="30" fill="#c4a984"/>
  <rect x="80" y="120" width="360" height="70" rx="18" fill="#e3cfb3"/><line x1="260" y1="124" x2="260" y2="186" stroke="#b89e7c" stroke-width="3"/>
  <rect x="80" y="196" width="10" height="16" rx="3" fill="${ACC}"/><rect x="430" y="196" width="10" height="16" rx="3" fill="${ACC}"/></svg>
  <div style="position:absolute;right:24px;top:20px;font:800 22px/1 Mont;color:${ACC};letter-spacing:3px">★★★★★</div>`;
 F2.it=[['Качественные материалы',14.20],['Отличная фурнитура',15.72],['Идеальная сборка',16.90]].map(([x,at],i)=>{const r=glassBox(S,60,566+i*100,600,84);
  r.innerHTML=`<div style="position:absolute;left:20px;top:20px;width:44px;height:44px;border-radius:50%;background:${ACC};color:#111;font:800 24px/44px Mont;text-align:center">✓</div><div style="position:absolute;left:84px;top:0;font:800 23px/84px Mont;color:#fff">${x}</div>`;return{r,at}});
})();
function renderF2(t){if(!vis(F2.S,t,13.00,18.00))return;
 applyPop(F2.h,t,13.10,'',.26,.6);applyPop(F2.c,t,13.42,'',.3,.8);
 F2.it.forEach(({r,at})=>{const q=lin(t,at,at+.36);r.style.opacity=t<at?0:clamp(q*2);r.style.transform=`translateX(${(1-eBack(q))*-400}px)`});
 const g=eOut(lin(t,17.48,17.75));F2.c.style.boxShadow=`0 24px 60px rgba(0,0,0,.5),0 0 ${60*g}px rgba(255,178,30,${.4*g})`;
}
// F3 25.56–30.00: why trust you with $5 000
const F3={};
(function(){const S=mkScene('f3','v3bg');F3.S=S;
 F3.h=head(S,`Почему вам<br>${A_('доверят')}?`,96);
 F3.m=glassBox(S,60,290,600,230,{background:'rgba(28,29,34,.97)',border:`1.5px solid ${ACC}`});
 F3.m.innerHTML=`<div style="position:absolute;left:28px;top:28px;font:700 17px/1 Mont;color:#8e8f97">Чек клиента</div>
  <div id="f3n" style="position:absolute;left:24px;top:62px;font:600 110px/1 Osw;background:linear-gradient(180deg,#FFD36A,#FFB21E 55%,#FF8A1A);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(255,170,40,.45))"></div>
  <div style="position:absolute;right:28px;top:66px;font:90px/1 ${EMO}">💳</div>`;
 F3.tr=glassBox(S,60,546,600,300);
 F3.tr.innerHTML=`<div style="position:absolute;left:28px;top:26px;font:800 20px/1 Mont;color:#fff">Доверие клиента</div><div id="f3p" style="position:absolute;right:28px;top:20px;font:800 30px/1 Mont;color:#fff"></div>
  <div style="position:absolute;left:28px;top:72px;width:544px;height:26px;border-radius:13px;background:#24252b;overflow:hidden"><div id="f3b" style="height:26px;border-radius:13px;width:0"></div></div>
  ${['📱 Фото на телефон','🌐 Сайт из 2000-х','❓ Непонятное предложение','💬 Ответ через сутки'].map((x,i)=>`<div class="f3r" style="position:absolute;left:28px;top:${120+i*42}px;font:700 17px/1 Mont,${EMO};color:#c9cad2"><span style="color:${RED};margin-right:8px">✕</span>${x}</div>`).join('')}`;
 F3.rows=[...F3.tr.querySelectorAll('.f3r')];
})();
function renderF3(t){if(!vis(F3.S,t,25.56,30.00))return;
 applyPop(F3.h,t,25.70,'',.26,.6);applyPop(F3.tr,t,26.34,'',.28,.8);
 F3.rows.forEach((r,i)=>applyPop(r,t,26.60+i*.18,'',.2,.7));
 const v=mix(85,18,eInOut(lin(t,26.80,28.00)));$('f3b').style.width=v+'%';$('f3b').style.background=v>50?ACC:RED;$('f3p').textContent=t>=26.6?Math.round(v)+'%':'';$('f3p').style.color=v>50?'#fff':'#ff8b8b';
 applyPop(F3.m,t,28.26,'',.28,.8);$('f3n').textContent=t>=28.26?'$'+fmtInt(Math.round(5000*eOut(lin(t,28.30,29.20))/100)*100):'';
}
// F4 33.90–40.00: what's needed besides ads
const F4={};
(function(){const S=mkScene('f4','v3bg');F4.S=S;
 F4.h=head(S,`Кроме рекламы ${A_('нужны')}`,100);
 F4.it=[['📦','Сильная упаковка','бренд, визуал, сайт',34.96],['🎬','Качественный контент','съёмка, тексты, кейсы',36.14],['🎯','Понятное позиционирование','за что платят именно вам',37.34],['⚡','Обработка заявок','ответ за минуты, а не сутки',38.78]].map(([ico,tt,sub,at],i)=>{
  const r=glassBox(S,50,214+i*170,620,150);
  r.innerHTML=`<div style="position:absolute;left:22px;top:23px;width:104px;height:104px;border-radius:28px;background:#17181c;border:1px solid rgba(255,178,30,.4);display:flex;align-items:center;justify-content:center;font:52px/1 ${EMO}">${ico}</div>
   <div style="position:absolute;left:150px;top:40px;font:800 25px/1 Mont;color:#fff">${tt}</div><div style="position:absolute;left:150px;top:80px;font:600 16px/1 Mont;color:#9a9ba3">${sub}</div>
   <div class="ok" style="position:absolute;right:22px;top:49px;width:52px;height:52px;border-radius:50%;background:${ACC};color:#111;font:800 28px/52px Mont;text-align:center">✓</div>`;
  return{r,at,ok:r.querySelector('.ok')}});
})();
function renderF4(t){if(!vis(F4.S,t,33.90,40.00,'slide'))return;
 applyPop(F4.h,t,34.08,'',.26,.6);
 F4.it.forEach(({r,at,ok},i)=>{const q=lin(t,at,at+.36);r.style.opacity=t<at?0:clamp(q*2);r.style.transform=`translateX(${(1-eBack(q))*(i%2?-420:420)}px)`;applyPop(ok,t,at+.3,'',.2,.3);
  r.style.borderColor=t>=at+.3?'rgba(255,178,30,.5)':'rgba(255,255,255,.08)'});
}
// F5 42.70–47.04: ads bring, the system sells
const F5={};
(function(){const S=mkScene('f5','v3bg');F5.S=S;
 F5.h=head(S,`Убедить купить —<br>${A_('задача системы')}`,90);
 const steps=[['📣','Реклама'],['📦','Упаковка'],['🎬','Контент'],['🎯','Позиционирование'],['⚡','Обработка заявки'],['💳','Покупка']];
 F5.st=steps.map(([ico,tt],i)=>{const y=270+i*112;const r=el('div','abs',S,{left:'170px',top:y+'px',width:'470px',height:'92px',borderRadius:'24px',boxSizing:'border-box',background:i===5?'rgba(46,204,113,.16)':'rgba(28,29,34,.96)',border:i===0?`1.5px solid ${ACC}`:i===5?'1.5px solid #2ecc71':'1px solid rgba(255,255,255,.1)',boxShadow:'0 16px 40px rgba(0,0,0,.45)'});
  r.innerHTML=`<div style="position:absolute;left:16px;top:14px;width:64px;height:64px;border-radius:18px;background:#17181c;display:flex;align-items:center;justify-content:center;font:34px/1 ${EMO}">${ico}</div><div style="position:absolute;left:98px;top:0;font:800 23px/92px Mont;color:#fff">${tt}</div>`;return{r,y}});
 F5.rail=el('div','abs',S,{left:'120px',top:'316px',width:'6px',height:'0',borderRadius:'3px',background:ACC,boxShadow:`0 0 14px ${ACC}`});
 F5.dot=el('div','abs',S,{left:'104px',width:'38px',height:'38px',borderRadius:'50%',background:'#fff',boxShadow:`0 0 0 6px rgba(255,178,30,.45),0 0 26px ${ACC}`,font:`22px/38px ${EMO}`,textAlign:'center'});F5.dot.textContent='👤';
 F5.b1=el('div','abs',S,{left:'20px',top:'292px',width:'80px',textAlign:'right',font:'800 14px/1.2 Mont',color:ACC});F5.b1.innerHTML='реклама<br>приводит';
 F5.b2=el('div','abs',S,{left:'20px',top:'560px',width:'80px',textAlign:'right',font:'800 14px/1.2 Mont',color:'#c9cad2'});F5.b2.innerHTML='система<br>убеждает';
})();
function renderF5(t){if(!vis(F5.S,t,42.70,47.04))return;
 applyPop(F5.h,t,42.80,'',.26,.6);
 F5.st.forEach(({r},i)=>applyPop(r,t,[42.80,43.86,44.10,44.34,44.58,46.26][i],'',.24,.7));
 applyPop(F5.b1,t,42.90,'',.2,.6);applyPop(F5.b2,t,45.08,'',.2,.6);
 const p=eInOut(lin(t,43.86,46.26));const y0=316,y1=316+5*112;F5.rail.style.height=(p*(y1-y0))+'px';
 F5.dot.style.display=t>=43.0?'block':'none';F5.dot.style.top=(mix(y0,y1,p)-19)+'px';
 const g=eOut(lin(t,46.26,46.5));F5.st[5].r.style.boxShadow=`0 16px 40px rgba(0,0,0,.45),0 0 ${50*g}px rgba(46,204,113,${.5*g})`;
}

window.renderAt=function(t){pending.length=0;document.querySelectorAll('img').forEach(im=>{if(im.src)pending.push(im.decode().catch(()=>{}))});
 renderSubs(t);renderOV(t);renderF1(t);renderF2(t);renderF3(t);renderF4(t);renderF5(t);return Promise.all(pending)};
window.renderAt(0);
</script></body></html>
