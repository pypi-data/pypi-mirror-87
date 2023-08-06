import{P as t,o as e,q as i,r as n,_ as o,L as s,p as r,t as a,h as c,u as h,g as l,c as d}from"./e.a5d24e53.js";function u(t){const e=t.language||"en";return t.translationMetadata.translations[e]&&t.translationMetadata.translations[e].isRTL||!1}function p(t){return u(t)?"rtl":"ltr"}class y{constructor(t){y[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return y.types[t]&&y.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=y.types[e]=y.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=y.types[this.type];return t?Object.keys(t).map((function(t){return v[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}y[" "]=function(){},y.types={};var v=y.types;t({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new y({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new y({type:this.type,key:t}).value}}),t({_template:e`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:i.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&n(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,n(this.root).appendChild(this._img))}});const m=window;"customIconsets"in m||(m.customIconsets={});const _=m.customIconsets;const f={version:"0",parts:[]};class g{constructor(t="keyval-store",e="keyval"){this.storeName=e,this._dbp=new Promise((i,n)=>{const o=indexedDB.open(t,1);o.onerror=()=>n(o.error),o.onsuccess=()=>i(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(e)}})}_withIDBStore(t,e){return this._dbp.then(i=>new Promise((n,o)=>{const s=i.transaction(this.storeName,t);s.oncomplete=()=>n(),s.onabort=s.onerror=()=>o(s.error),e(s.objectStore(this.storeName))}))}}let k;function w(){return k||(k=new g),k}function b(t,e,i=w()){return i._withIDBStore("readwrite",i=>{i.put(e,t)})}const I=new g("hass-icon-db","mdi-icon-store"),S=["mdi","hass","hassio","hademo"];let x=[];const B={},$={};(function(t,e=w()){let i;return e._withIDBStore("readonly",e=>{i=e.get(t)}).then(()=>i.result)})("_version",I).then(t=>{t?t!==f.version&&function(t=w()){return t._withIDBStore("readwrite",t=>{t.clear()})}(I).then(()=>b("_version",f.version,I)):b("_version",f.version,I)});const N=((t,e,i=!1)=>{let n;return function(...o){const s=this,r=i&&!n;clearTimeout(n),n=setTimeout(()=>{n=null,i||t.apply(s,o)},e),r&&t.apply(s,o)}})(()=>(async t=>{const e=Object.keys(t),i=await Promise.all(Object.values(t));I._withIDBStore("readwrite",n=>{i.forEach((i,o)=>{Object.entries(i).forEach(([t,e])=>{n.put(e,t)}),delete t[e[o]]})})})($),2e3),C={};o([d("ha-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[r()],key:"icon",value:void 0},{kind:"field",decorators:[a()],key:"_path",value:void 0},{kind:"field",decorators:[a()],key:"_viewBox",value:void 0},{kind:"field",decorators:[a()],key:"_legacy",value:()=>!1},{kind:"method",key:"updated",value:function(t){t.has("icon")&&(this._path=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?c`<iron-icon .icon=${this.icon}></iron-icon>`:c`<ha-svg-icon
      .path=${this._path}
      .viewBox=${this._viewBox}
    ></ha-svg-icon>`:c``}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const[t,e]=this.icon.split(":",2);let i,n=e;if(!t||!n)return;if(!S.includes(t)){if(t in _){const e=_[t];return void(e&&this._setCustomPath(e(n)))}return void(this._legacy=!0)}if(this._legacy=!1,n in B){const e=B[n];let i;e.newName?(i=`Icon ${t}:${n} was renamed to ${t}:${e.newName}, please change your config, it will be removed in version ${e.removeIn}.`,n=e.newName):i=`Icon ${t}:${n} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${e.removeIn}.`,console.warn(i),h(this,"write_log",{level:"warning",message:i})}if(n in C)return void(this._path=C[n]);try{i=await(t=>new Promise((e,i)=>{if(x.push([t,e,i]),x.length>1)return;const n=[];I._withIDBStore("readonly",t=>{for(const[e,i]of x)n.push([i,t.get(e)]);x=[]}).then(()=>{for(const[t,e]of n)t(e.result)}).catch(()=>{for(const[,,t]of x)t();x=[]})}))(n)}catch(t){i=void 0}if(i)return this._path=i,void(C[n]=i);const o=(t=>{let e;for(const i of f.parts){if(void 0!==i.start&&t<i.start)break;e=i}return e.file})(n);if(o in $)return void this._setPath($[o],n);const s=fetch(`/static/mdi/${o}.json`).then(t=>t.json());$[o]=s,this._setPath(s,n),N()}},{kind:"method",key:"_setCustomPath",value:async function(t){const e=await t;this._path=e.path,this._viewBox=e.viewBox}},{kind:"method",key:"_setPath",value:async function(t,e){const i=await t;this._path=i[e],C[e]=i[e]}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        fill: currentcolor;
      }
    `}}]}}),s),o([d("ha-icon-button")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[r({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[r({type:String})],key:"icon",value:()=>""},{kind:"field",decorators:[r({type:String})],key:"label",value:()=>""},{kind:"method",key:"createRenderRoot",value:function(){return this.attachShadow({mode:"open",delegatesFocus:!0})}},{kind:"method",key:"render",value:function(){return c`
      <mwc-icon-button .label=${this.label} .disabled=${this.disabled}>
        <ha-icon .icon=${this.icon}></ha-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),s),o([d("hacs-icon-button")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[r({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[r({type:String})],key:"icon",value:()=>""},{kind:"method",key:"createRenderRoot",value:function(){return this.attachShadow({mode:"open",delegatesFocus:!0})}},{kind:"method",key:"render",value:function(){return c`
      <mwc-icon-button .disabled=${this.disabled}>
        <ha-svg-icon .path=${this.icon}></ha-svg-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-svg-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),s);export{y as I,u as a,p as c};
