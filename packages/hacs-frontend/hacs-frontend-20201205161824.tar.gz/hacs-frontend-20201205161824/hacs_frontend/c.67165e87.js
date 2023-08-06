import{_ as o,H as t,h as a,l as e,c}from"./e.4add7a3d.js";import"./c.9abaa356.js";import"./c.e68bb6ba.js";let i=o([c("hacs-reload-dialog")],(function(o,t){return{F:class extends t{constructor(...t){super(...t),o(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?a`
      <hacs-dialog .active=${this.active} .hass=${this.hass} title="Reload">
        <div class="content">
          ${e("dialog.reload.description")}
          </br>
          ${e("dialog.reload.confirm")}
        </div>
        <mwc-button slot="secondaryaction" @click=${this._close}>
          ${e("common.cancel")}
        </mwc-button>
        <mwc-button slot="primaryaction" @click=${this._reload}>
          ${e("common.reload")}
        </mwc-button>
      </hacs-dialog>
    `:a``}},{kind:"method",key:"_reload",value:function(){window.top.location.reload(!0)}},{kind:"method",key:"_close",value:function(){this.active=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0}))}}]}}),t);export{i as HacsReloadDialog};
