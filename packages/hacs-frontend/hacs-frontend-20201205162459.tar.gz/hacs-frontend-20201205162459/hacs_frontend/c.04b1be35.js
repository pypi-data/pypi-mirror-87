import{_ as e,H as t,p as i,w as o,h as s,c as r}from"./e.1b8d9b76.js";import{m as a}from"./c.c4c0026c.js";import"./c.b9a5584e.js";import"./c.9c6740fb.js";import"./c.abfb169a.js";let d=e([r("hacs-generic-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[i()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"header",value:void 0},{kind:"field",decorators:[i()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((e,t)=>null==e?void 0:e.find(e=>e.id===t))},{kind:"method",key:"render",value:function(){if(!this.active)return s``;const e=this._getRepository(this.repositories,this.repository);return s`
      <hacs-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?a.html(this.content||"",e):a.html(this.content||""):this.content||""}
      </hacs-dialog>
    `}}]}}),t);export{d as HacsGenericDialog};
