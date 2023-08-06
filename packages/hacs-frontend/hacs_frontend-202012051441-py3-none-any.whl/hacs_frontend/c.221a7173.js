import{_ as t,H as e,p as i,v as o,w as a,h as r,l as s,d as n,x as d,y as l,s as c,g as p,c as h}from"./e.a5d24e53.js";import"./c.cca5aeb9.js";import"./c.895f1128.js";import"./c.6bc22f20.js";import"./c.aab2d74a.js";import"./c.f9483f07.js";import"./c.2a90b9a5.js";import{f as u,h as f}from"./c.b3443e2e.js";import"./c.c20a72e7.js";let v=t([h("hacs-add-repository-dialog")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[i({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[i({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[i()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[i()],key:"_sortBy",value:()=>"stars"},{kind:"field",decorators:[i()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(t){return t.forEach((t,e)=>{"hass"===e&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))}),t.has("narrow")||t.has("filters")||t.has("active")||t.has("_searchInput")||t.has("_load")||t.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(t,e)=>null==t?void 0:t.filter(t=>{var i,o;return!t.installed&&(null===(i=this.hacs.sections)||void 0===i||null===(o=i.find(t=>t.id===this.section).categories)||void 0===o?void 0:o.includes(t.category))&&!t.installed&&(null==e?void 0:e.includes(t.category))})}},{kind:"method",key:"firstUpdated",value:async function(){var t;if(this.addEventListener("filter-change",t=>this._updateFilters(t)),0===(null===(t=this.filters)||void 0===t?void 0:t.length)){var e;const t=null===(e=o(this.route))||void 0===e?void 0:e.categories;null==t||t.filter(t=>{var e;return null===(e=this.hacs.configuration)||void 0===e?void 0:e.categories.includes(t)}).forEach(t=>{this.filters.push({id:t,value:t,checked:!0})}),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(t){const e=this.filters.find(e=>e.id===t.detail.id);this.filters.find(t=>t.id===e.id).checked=!e.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>a(u)},{kind:"method",key:"render",value:function(){var t;if(!this.active)return r``;this._searchInput=window.localStorage.getItem("hacs-search")||"";let e=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(t=this.hacs.configuration)||void 0===t?void 0:t.categories),this._searchInput);return 0!==this.filters.length&&(e=e.filter(t=>{var e;return null===(e=this.filters.find(e=>e.id===t.category))||void 0===e?void 0:e.checked})),r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${s("dialog_add_repo.title")}
        hideActions
      >
        <div class="searchandfilter">
          <search-input
            no-label-float
            .label=${s("search.placeholder")}
            .filter=${this._searchInput||""}
            @value-changed=${this._inputValueChanged}
            ?narrow=${this.narrow}
          ></search-input>
          <div class="filter" ?narrow=${this.narrow}>
            <paper-dropdown-menu
              label="${s("dialog_add_repo.sort_by")}"
              ?narrow=${this.narrow}
            >
              <paper-listbox slot="dropdown-content" selected="0">
                <paper-item @tap=${()=>this._sortBy="stars"}
                  >${s("store.stars")}</paper-item
                >
                <paper-item @tap=${()=>this._sortBy="name"}
                  >${s("store.name")}</paper-item
                >
                <paper-item @tap=${()=>this._sortBy="last_updated"}
                  >${s("store.last_updated")}</paper-item
                >
              </paper-listbox>
            </paper-dropdown-menu>
          </div>
        </div>
        ${this.filters.length>1?r`<div class="filters">
              <hacs-filter .filters="${this.filters}"></hacs-filter>
            </div>`:""}
        <div class=${n({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${n({list:!0,narrow:this.narrow})}>
            ${e.sort((t,e)=>"name"===this._sortBy?t.name.toLocaleLowerCase()<e.name.toLocaleLowerCase()?-1:1:t[this._sortBy]>e[this._sortBy]?-1:1).slice(0,this._load).map(t=>r`<paper-icon-item
                  class=${n({narrow:this.narrow})}
                  @click=${()=>this._openInformation(t)}
                >
                  ${"integration"===t.category?r`
                        <img
                          src="https://brands.home-assistant.io/_/${t.domain}/icon.png"
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${d} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body two-line
                    >${t.name}
                    <div class="category-chip">
                      <hacs-chip
                        .icon=${f}
                        .value=${s("common."+t.category)}
                      ></hacs-chip>
                    </div>
                    <div secondary>${t.description}</div>
                  </paper-item-body>
                </paper-icon-item>`)}
            ${0===e.length?r`<p>${s("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(t){const e=t.target.scrollTop;e>=this._top?this._load+=1:this._load-=1,this._top=e}},{kind:"method",key:"_inputValueChanged",value:function(t){this._searchInput=t.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(t){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:t.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(t){t.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(t){t.target&&(t.target.outerHTML=`<ha-svg-icon .path=${d} slot="item-icon"></ha-svg-icon>`)}},{kind:"get",static:!0,key:"styles",value:function(){return[l,c,p`
        .content {
          width: 100%;
          overflow: auto;
          max-height: 70vh;
        }

        .filter {
          margin-top: -12px;
          display: flex;
          width: 200px;
          float: right;
        }

        .narrow {
          max-height: 480px;
          min-width: unset !important;
          width: 100% !important;
        }
        .list {
          margin-top: 16px;
          width: 1024px;
          max-width: 100%;
        }
        .category-chip {
          position: absolute;
          top: 8px;
          right: 8px;
        }
        ha-icon {
          --mdc-icon-size: 36px;
        }
        search-input {
          float: left;
          width: 60%;
        }
        search-input[narrow],
        div.filter[narrow],
        paper-dropdown-menu[narrow] {
          width: 100%;
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

        paper-icon-item:focus {
          background-color: var(--divider-color);
        }

        paper-icon-item {
          cursor: pointer;
          padding: 2px 0;
        }

        paper-dropdown-menu {
          margin: 0 12px 4px 0;
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-icon-item.narrow {
          border-bottom: 1px solid var(--divider-color);
          padding: 8px 0;
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add {
          border-top: 1px solid var(--divider-color);
          margin-top: 32px;
        }
        .filters {
          width: 100%;
          display: flex;
        }
        .add-actions {
          justify-content: space-between;
        }
        .add,
        .add-actions {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: 65px;
          background-color: var(--sidebar-background-color);
          border-bottom: 1px solid var(--divider-color);
          padding: 0 16px;
          box-sizing: border-box;
        }
        .add-input {
          width: calc(100% - 80px);
          height: 40px;
          border: 0;
          padding: 0 16px;
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

        hacs-filter {
          width: 100%;
        }
        div[secondary] {
          width: 88%;
        }
      `]}}]}}),e);export{v as HacsAddRepositoryDialog};
