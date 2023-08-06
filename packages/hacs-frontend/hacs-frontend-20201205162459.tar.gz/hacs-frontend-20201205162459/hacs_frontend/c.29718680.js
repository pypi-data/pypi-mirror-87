import{_ as t,L as a,p as e,a0 as i,g as s,c as r,H as o,t as n,h as d,n as c}from"./e.1b8d9b76.js";import"./c.9c6740fb.js";import"./c.abfb169a.js";t([r("ha-bar")],(function(t,a){return{F:class extends a{constructor(...a){super(...a),t(this)}},d:[{kind:"field",decorators:[e({type:Number})],key:"min",value:()=>0},{kind:"field",decorators:[e({type:Number})],key:"max",value:()=>100},{kind:"field",decorators:[e({type:Number})],key:"value",value:void 0},{kind:"method",key:"render",value:function(){const t=(t=>Math.round(10*t)/10)(((t,a,e)=>100*(t-a)/(e-a))((a=this.value,e=this.min,s=this.max,isNaN(a)||isNaN(e)||isNaN(s)?0:a>s?s:a<e?e:a),this.min,this.max));var a,e,s;return i`
      <svg>
        <g>
          <rect/>
          <rect width="${t}%"/>
        </g>
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return s`
      rect {
        height: 100%;
      }
      rect:first-child {
        width: 100%;
        fill: var(--ha-bar-background-color, var(--secondary-background-color));
      }
      rect:last-child {
        fill: var(--ha-bar-primary-color, var(--primary-color));
        rx: var(--ha-bar-border-radius, 4px);
      }
      svg {
        border-radius: var(--ha-bar-border-radius, 4px);
        height: 12px;
        width: 100%;
      }
    `}}]}}),a);let h=t([r("hacs-navigate-dialog")],(function(t,a){return{F:class extends a{constructor(...a){super(...a),t(this)}},d:[{kind:"field",decorators:[e()],key:"path",value:void 0},{kind:"field",decorators:[n()],key:"_progress",value:()=>0},{kind:"method",key:"firstUpdated",value:async function(){this._updateProgress()}},{kind:"method",key:"render",value:function(){return this.active?d`
      <hacs-dialog
        @closed=${this.closeDialog}
        .active=${this.active}
        .hass=${this.hass}
        title="Navigating away from HACS"
        >
        <div class="content">
          This takes you away from HACS and to another page, what you see on that page is not a part
          of HACS.
          </br></br>
          Redirect will happen automatically in 10 seconds, if you do not want to wait
          click the "GO NOW" button.
        </div>
        <ha-bar .value=${this._progress}></ha-bar>
        <mwc-button slot="primaryaction" @click=${this._navigate}>
          Go now
        </mwc-button>
      </hacs-dialog>
    `:d``}},{kind:"method",key:"closeDialog",value:function(){this.active=!1}},{kind:"method",key:"_updateProgress",value:function(){setTimeout(()=>{this.active&&(this._progress+=10,100===this._progress?this._navigate():this._updateProgress())},1e3)}},{kind:"method",key:"_navigate",value:function(){this.active&&c(this,this.path)}},{kind:"get",static:!0,key:"styles",value:function(){return[s`
        hacs-dialog {
          --hacs-dialog-max-width: 460px;
        }
      `]}}]}}),o);export{h as HacsNavigateDialog};
