import{_ as i,H as t,p as s,w as o,T as e,O as a,h as r,d as n,l as h,a4 as c,a5 as d,a6 as l,a7 as p,a8 as u,s as _,g as y,c as m}from"./e.4add7a3d.js";import{m as f}from"./c.e6096e9b.js";import"./c.02702101.js";import"./c.9abaa356.js";import"./c.e68bb6ba.js";import"./c.eeecae56.js";let g=i([m("hacs-repository-info-dialog")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[s()],key:"repository",value:void 0},{kind:"field",decorators:[s()],key:"_repository",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((i,t)=>null==i?void 0:i.find(i=>i.id===t))},{kind:"field",key:"_getAuthors",value:()=>o(i=>{const t=[];if(!i.authors)return t;if(i.authors.forEach(i=>t.push(i.replace("@",""))),0===t.length){const s=i.full_name.split("/")[0];if(["custom-cards","custom-components","home-assistant-community-themes"].includes(s))return t;t.push(s)}return t})},{kind:"method",key:"shouldUpdate",value:function(i){return i.forEach((i,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===t&&(this._repository=this._getRepository(this.repositories,this.repository))}),i.has("sidebarDocked")||i.has("narrow")||i.has("active")||i.has("_repository")}},{kind:"method",key:"firstUpdated",value:async function(){this._repository=this._getRepository(this.repositories,this.repository),this._repository.updated_info||(await e(this.hass,this._repository.id),this.repositories=await a(this.hass))}},{kind:"method",key:"render",value:function(){if(!this.active)return r``;const i=this._getAuthors(this._repository);return r`
      <hacs-dialog
        .noActions=${this._repository.installed}
        .active=${this.active}
        .title=${this._repository.name||""}
        .hass=${this.hass}
        ><div class=${n({content:!0,narrow:this.narrow})}>
          <div class="chips">
            ${this._repository.installed?r`<hacs-chip
                  title="${h("dialog_info.version_installed")}"
                  .icon=${c}
                  .value=${this._repository.installed_version}
                ></hacs-chip>`:""}
            ${i?i.map(i=>r`<hacs-chip
                    title="${h("dialog_info.author")}"
                    .url="https://github.com/${i}"
                    .icon=${d}
                    .value="@${i}"
                  ></hacs-chip>`):""}
            ${this._repository.downloads?r` <hacs-chip
                  title="${h("dialog_info.downloads")}"
                  .icon=${l}
                  .value=${this._repository.downloads}
                ></hacs-chip>`:""}
            <hacs-chip
              title="${h("dialog_info.stars")}"
              .icon=${p}
              .value=${this._repository.stars}
            ></hacs-chip>
            <hacs-chip
              title="${h("dialog_info.open_issues")}"
              .icon=${u}
              .value=${this._repository.issues}
              .url="https://github.com/${this._repository.full_name}/issues"
            ></hacs-chip>
          </div>
          ${this._repository.updated_info?f.html(this._repository.additional_info||h("dialog_info.no_info"),this._repository):h("dialog_info.loading")}
        </div>
        ${!this._repository.installed&&this._repository.updated_info?r`
              <mwc-button slot="primaryaction" @click=${this._installRepository}
                >${h("dialog_info.install")}</mwc-button
              ><hacs-link
                slot="secondaryaction"
                .url="https://github.com/${this._repository.full_name}"
                ><mwc-button>${h("dialog_info.open_repo")}</mwc-button></hacs-link
              >
            `:""}
      </hacs-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[_,y`
        .content {
          width: 100%;
          overflow: auto;
          max-height: 870px;
        }
        .narrow {
          max-height: 480px;
          min-width: unset !important;
          width: 100% !important;
        }
        img {
          max-width: 100%;
        }
        .chips {
          display: flex;
          padding-bottom: 8px;
        }
        hacs-chip {
          margin: 0 4px;
        }
        div.chips hacs-link {
          margin: -24px 4px;
        }
        hacs-link mwc-button {
          margin-top: -18px;
        }
      `]}},{kind:"method",key:"_installRepository",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"install",repository:this._repository.id},bubbles:!0,composed:!0}))}}]}}),t);export{g as HacsRepositoryDialog};
