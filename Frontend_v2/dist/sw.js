if(!self.define){let e,s={};const i=(i,l)=>(i=new URL(i+".js",l).href,s[i]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=s,document.head.appendChild(e)}else e=i,importScripts(i),s()})).then((()=>{let e=s[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(l,r)=>{const n=e||("document"in self?document.currentScript.src:"")||location.href;if(s[n])return;let t={};const u=e=>i(e,n),o={module:{uri:n},exports:t,require:u};s[n]=Promise.all(l.map((e=>o[e]||u(e)))).then((e=>(r(...e),t)))}}define(["./workbox-3625d7b0"],(function(e){"use strict";self.skipWaiting(),e.clientsClaim(),e.precacheAndRoute([{url:"assets/BlogView-22aa8f57.css",revision:null},{url:"assets/BlogView-9c83a5d0.js",revision:null},{url:"assets/counter-5cebc8db.js",revision:null},{url:"assets/index-1e837380.js",revision:null},{url:"assets/index-20c75656.css",revision:null},{url:"assets/LoginView-b5c19a1c.js",revision:null},{url:"assets/LoginView-e4fce82a.css",revision:null},{url:"assets/profileView-383cd112.css",revision:null},{url:"assets/profileView-f6e87237.js",revision:null},{url:"assets/RegisterView-bc9384a3.js",revision:null},{url:"assets/RegisterView-e3b0c442.css",revision:null},{url:"assets/relativeTime-73612df9.js",revision:null},{url:"assets/Summary-35a65309.css",revision:null},{url:"assets/Summary-a0c30745.js",revision:null},{url:"assets/validate-7539bfb6.js",revision:null},{url:"index.html",revision:"38e31d56d2e3025e7c95d44adfa27f88"},{url:"registerSW.js",revision:"1872c500de691dce40960bb85481de07"},{url:"icons/image.png",revision:"9535cde49086e4410663be061ee56e8b"},{url:"manifest.webmanifest",revision:"ce72045d7e2e3daa3dacd1170ee0c5c9"}],{}),e.cleanupOutdatedCaches(),e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html")))}));