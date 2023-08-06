import{_ as t,L as e,p as n,h as r,n as i,g as o,c as s}from"./e.4add7a3d.js";t([s("hacs-link")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[n({type:Boolean})],key:"newtab",value:()=>!1},{kind:"field",decorators:[n({type:Boolean})],key:"parent",value:()=>!1},{kind:"field",decorators:[n()],key:"title",value:void 0},{kind:"field",decorators:[n()],key:"url",value:void 0},{kind:"method",key:"render",value:function(){return r`<span title=${this.title||this.url} @click=${this._open}><slot></slot></span>`}},{kind:"method",key:"_open",value:function(){var t;if(this.url.startsWith("/"))return void i(this,this.url,!0);const e=null===(t=this.url)||void 0===t?void 0:t.includes("http");let n="",r="_blank";e&&(n="noreferrer=true"),e||this.newtab||(r="_top"),e||this.parent||(r="_parent"),window.open(this.url,r,n)}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      span {
        cursor: pointer;
        color: var(--hcv-text-color-link);
        text-decoration: var(--hcv-text-decoration-link);
      }
    `}}]}}),e);
