import{_ as o,H as i,p as t,J as e,h as r,l as a,x as s,K as n,N as d,O as c,Q as p,s as l,g as h,c as u}from"./e.4add7a3d.js";import"./c.9abaa356.js";import"./c.e68bb6ba.js";import"./c.7c3326e3.js";import"./c.1d4ba97d.js";import"./c.55fb6af2.js";import"./c.58f47855.js";let m=o([u("hacs-custom-repositories-dialog")],(function(o,i){return{F:class extends i{constructor(...i){super(...i),o(this)}},d:[{kind:"field",decorators:[t()],key:"_inputRepository",value:void 0},{kind:"field",decorators:[t()],key:"_error",value:void 0},{kind:"field",decorators:[e("#add-input")],key:"_addInput",value:void 0},{kind:"field",decorators:[e("#category")],key:"_addCategory",value:void 0},{kind:"method",key:"shouldUpdate",value:function(o){return o.has("narrow")||o.has("active")||o.has("_error")||o.has("repositories")}},{kind:"method",key:"render",value:function(){var o;if(!this.active)return r``;const i=null===(o=this.repositories)||void 0===o?void 0:o.filter(o=>o.custom);return r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${a("dialog_custom_repositories.title")}
      >
        <div class="content">
          <div class="list">
            ${this._error?r`<div class="error">${this._error.message}</div>`:""}
            ${null==i?void 0:i.map(o=>r`<paper-icon-item>
                ${"integration"===o.category?r`
                      <img
                        src="https://brands.home-assistant.io/_/${o.domain}/icon.png"
                        referrerpolicy="no-referrer"
                        @error=${this._onImageError}
                        @load=${this._onImageLoad}
                      />
                    `:r`<ha-svg-icon .path=${s} slot="item-icon"></ha-svg-icon>`}
                <paper-item-body
                  @click=${()=>this._showReopsitoryInfo(String(o.id))}
                  three-line
                  >${o.name}
                  <div secondary>${o.description}</div>
                  <div secondary>Category: ${o.category}</div></paper-item-body
                ><hacs-icon-button
                  class="delete"
                  .icon=${n}
                  @click=${()=>this._removeRepository(o.id)}
                ></hacs-icon-button>
              </paper-icon-item>`)}
          </div>
        </div>
        <input
          id="add-input"
          class="add-input"
          slot="secondaryaction"
          placeholder="${a("dialog_custom_repositories.url_placeholder")}"
          .value=${this._inputRepository||""}
          @input=${this._inputValueChanged}
          ?narrow=${this.narrow}
        />

        <div class="add" slot="primaryaction" ?narrow=${this.narrow}>
          <paper-dropdown-menu
            ?narrow=${this.narrow}
            class="category"
            label="${a("dialog_custom_repositories.category")}"
          >
            <paper-listbox id="category" slot="dropdown-content" selected="-1">
              ${this.hacs.configuration.categories.map(o=>r`
                  <paper-item class="categoryitem" .category=${o}>
                    ${a("common."+o)}
                  </paper-item>
                `)}
            </paper-listbox>
          </paper-dropdown-menu>
          <mwc-button
            ?narrow=${this.narrow}
            slot="primaryaction"
            raised
            @click=${this._addRepository}
            >${a("common.add")}</mwc-button
          >
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.hass.connection.subscribeEvents(o=>this._error=o.data,"hacs/error")}},{kind:"method",key:"_inputValueChanged",value:function(){var o;this._inputRepository=null===(o=this._addInput)||void 0===o?void 0:o.value}},{kind:"method",key:"_addRepository",value:async function(){var o,i;this._error=void 0;const t=this._inputRepository,e=null===(o=this._addCategory)||void 0===o||null===(i=o.selectedItem)||void 0===i?void 0:i.category;e?t?(await d(this.hass,t,e),this.repositories=await c(this.hass)):this._error={message:a("dialog_custom_repositories.no_repository")}:this._error={message:a("dialog_custom_repositories.no_category")}}},{kind:"method",key:"_removeRepository",value:async function(o){this._error=void 0,await p(this.hass,o),this.repositories=await c(this.hass)}},{kind:"method",key:"_onImageLoad",value:function(o){o.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(o){o.target.outerHTML='<ha-icon\n      icon="mdi:github-circle"\n      slot="item-icon"\n    ></ha-icon>'}},{kind:"method",key:"_showReopsitoryInfo",value:async function(o){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:o},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[l,h`
        .content {
          width: 1024px;
          display: contents;
        }
        .list {
          position: relative;
          margin-top: 16px;
          max-height: 870px;
          overflow: auto;
        }
        ha-icon-button,
        ha-icon {
          color: var(--secondary-text-color);
        }
        ha-icon {
          --mdc-icon-size: 36px;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
          position: absolute;
        }
        .delete,
        paper-item-body {
          cursor: pointer;
        }
        .error {
          line-height: 0px;
          margin: 12px;
          color: var(--hacs-error-color, var(--google-red-500));
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add {
          display: flex;
          width: 100%;
          align-items: center;
        }

        .add-input {
          width: 100%;
          height: 40px;
          border: 0;
          padding: 0;
          text-align: left;
          padding-right: 71px;
          font-size: initial;
          color: var(--sidebar-text-color);
          font-family: var(--paper-font-body1_-_font-family);
        }
        input:focus {
          outline-offset: 0;
          outline: 0;
        }
        input {
          background-color: var(--sidebar-background-color);
        }
        paper-dropdown-menu {
          width: 100%;
          left: -50px;
          top: -8px;
        }
        mwc-button {
          margin-right: 10px;
        }

        input[narrow],
        .add[narrow],
        paper-dropdown-menu[narrow],
        mwc-button[narrow] {
          margin: 0;
          padding: 0;
          left: 0;
          top: 0;
          width: 100%;
          max-width: 100%;
        }
        .add[narrow] {
          display: contents;
        }
      `]}}]}}),i);export{m as HacsCustomRepositoriesDialog};
