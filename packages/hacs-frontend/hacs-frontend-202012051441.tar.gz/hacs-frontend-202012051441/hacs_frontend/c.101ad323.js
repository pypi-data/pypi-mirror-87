import{_ as s,H as e,p as t,w as i,a3 as a,h as o,l as r,d as n,V as l,W as c,s as d,g as h,c as p}from"./e.a5d24e53.js";import{m as u}from"./c.b5444a23.js";import"./c.5cc91132.js";import"./c.cca5aeb9.js";import"./c.895f1128.js";import{u as m}from"./c.1532d764.js";let _=s([p("hacs-update-dialog")],(function(s,e){return{F:class extends e{constructor(...e){super(...e),s(this)}},d:[{kind:"field",decorators:[t()],key:"repository",value:void 0},{kind:"field",decorators:[t()],key:"_updating",value:()=>!1},{kind:"field",decorators:[t()],key:"_error",value:void 0},{kind:"field",decorators:[t()],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>i((s,e)=>null==s?void 0:s.find(s=>s.id===e))},{kind:"method",key:"firstUpdated",value:async function(){const s=this._getRepository(this.repositories,this.repository);"commit"!==s.version_or_commit&&(this._releaseNotes=await a(this.hass,s.id),this._releaseNotes=this._releaseNotes.filter(e=>e.tag>s.installed_version)),this.hass.connection.subscribeEvents(s=>this._error=s.data,"hacs/error")}},{kind:"method",key:"render",value:function(){if(!this.active)return o``;const s=this._getRepository(this.repositories,this.repository);return o`
      <hacs-dialog
        .active=${this.active}
        .title=${r("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${n({content:!0,narrow:this.narrow})}>
          ${s.name}
          <p>
            <b>${r("dialog_update.installed_version")}:</b>
            ${s.installed_version}
          </p>
          <p>
            <b>${r("dialog_update.available_version")}:</b>
            ${s.available_version}
          </p>
          ${this._releaseNotes.length>0?this._releaseNotes.map(s=>o`<details>
                  <summary>${s.name}</summary>
                  ${u.html(s.body)}
                </details>`):""}
          ${s.can_install?"":o`<p class="error">
                ${r("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",s.homeassistant)}
              </p>`}
          ${"integration"===s.category?o`<p>${r("dialog_install.restart")}</p>`:""}
          ${this._error?o`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!s.can_install}
          @click=${this._updateRepository}
          >${this._updating?o`<ha-circular-progress active></ha-circular-progress>`:r("common.update")}</mwc-button
        >
        <div class="secondary" slot="secondaryaction">
          <hacs-link .url=${this._getChanglogURL()}
            ><mwc-button>${r("dialog_update.changelog")}</mwc-button></hacs-link
          >
          <hacs-link .url="https://github.com/${s.full_name}"
            ><mwc-button>${r("common.repository")}</mwc-button></hacs-link
          >
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const s=this._getRepository(this.repositories,this.repository);"commit"!==s.version_or_commit?await l(this.hass,s.id,s.available_version):await c(this.hass,s.id),"plugin"===s.category&&"storage"===this.hacs.status.lovelace_mode&&await m(this.hass,s),this._updating=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===s.category&&this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"reload"},bubbles:!0,composed:!0}))}},{kind:"method",key:"_getChanglogURL",value:function(){const s=this._getRepository(this.repositories,this.repository);return"commit"===s.version_or_commit?`https://github.com/${s.full_name}/compare/${s.installed_version}...${s.available_version}`:`https://github.com/${s.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[d,h`
        .content {
          padding: 32px 8px;
        }
        .error {
          color: var(--hacs-error-color, var(--google-red-500));
        }
        details {
          padding: 12px 0;
        }
        summary {
          padding: 4px;
          cursor: pointer;
        }
        .secondary {
          display: flex;
        }
      `]}}]}}),e);export{_ as HacsUpdateDialog};
