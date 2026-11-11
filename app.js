'use strict';
(() => {
 const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
 const toggle=$('.menu-toggle'),nav=$('#main-nav'),links=$$('#main-nav a');
 function setMenu(open){toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('is-open',open);document.body.classList.toggle('menu-open',open);}
 toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';setMenu(open);if(open)links[0].focus();});
 const mobile=window.matchMedia('(max-width: 620px)');mobile.addEventListener('change',()=>{if(!mobile.matches)setMenu(false);});
 const cards=$$('[data-project]'),filters=$$('[data-filter]'),count=$('#project-count');
 filters.forEach(button=>button.addEventListener('click',()=>{const selected=button.dataset.filter;let visible=0;cards.forEach(card=>{card.hidden=selected!=='all'&&card.dataset.project!==selected;if(!card.hidden)visible++;});filters.forEach(f=>{const active=f===button;f.classList.toggle('active',active);f.setAttribute('aria-pressed',String(active));});count.textContent=`${visible} ${selected==='all'?'pieces of work':selected==='development'?'projects':selected}`;}));
 const dialog=$('#image-dialog'),image=$('#dialog-image'),caption=$('#dialog-caption');let current=0,items=[];
 function showImage(index){current=(index+items.length)%items.length;const item=items[current];image.src=item.dataset.image;image.alt=item.dataset.caption;caption.textContent=`${item.dataset.caption} · ${current+1} / ${items.length}`;}
 $$('[data-image]').forEach(button=>button.addEventListener('click',()=>{items=$$('[data-image]').filter(item=>!item.closest('[data-project]')?.hidden);showImage(items.indexOf(button));dialog.showModal();}));
 dialog.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
 dialog.querySelector('.gallery-prev').addEventListener('click',()=>showImage(current-1));dialog.querySelector('.gallery-next').addEventListener('click',()=>showImage(current+1));
 dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
 document.addEventListener('keydown',event=>{if(toggle.getAttribute('aria-expanded')==='true'){if(event.key==='Escape'){setMenu(false);toggle.focus();}if(event.key==='Tab'){const items=[...links,toggle],index=items.indexOf(document.activeElement);event.preventDefault();items[(index+(event.shiftKey?-1:1)+items.length)%items.length].focus();}}if(dialog.open){if(event.key==='ArrowRight'){event.preventDefault();showImage(current+1);}if(event.key==='ArrowLeft'){event.preventDefault();showImage(current-1);}}});
 $('#year').textContent=String(new Date().getFullYear());
})();
