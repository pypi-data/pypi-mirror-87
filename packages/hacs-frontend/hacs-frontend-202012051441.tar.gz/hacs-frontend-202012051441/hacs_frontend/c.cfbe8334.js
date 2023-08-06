import{_ as o,H as t,h as e,l as c,c as a}from"./e.a5d24e53.js";import"./c.cca5aeb9.js";import"./c.895f1128.js";let i=o([a("hacs-reload-dialog")],(function(o,t){return{F:class extends t{constructor(...t){super(...t),o(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?e`
      <hacs-dialog .active=${this.active} .hass=${this.hass} title="Reload">
        <div class="content">
          ${c("dialog.reload.description")}
          </br>
          ${c("dialog.reload.confirm")}
        </div>
        <mwc-button slot="secondaryaction" @click=${this._close}>
          ${c("common.cancel")}
        </mwc-button>
        <mwc-button slot="primaryaction" @click=${this._reload}>
          ${c("common.reload")}
        </mwc-button>
      </hacs-dialog>
    `:e``}},{kind:"method",key:"_reload",value:function(){window.top.location.reload(!0)}},{kind:"method",key:"_close",value:function(){this.active=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0}))}}]}}),t);export{i as HacsReloadDialog};
