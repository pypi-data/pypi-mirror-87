import{_ as e,H as t,p as i,v as o,w as a,h as r,l as s,d,x as n,y as l,s as c,g as p,c as h}from"./e.4add7a3d.js";import"./c.9abaa356.js";import"./c.e68bb6ba.js";import"./c.7c3326e3.js";import"./c.1d4ba97d.js";import"./c.55fb6af2.js";import"./c.58f47855.js";import{f as u,h as f}from"./c.e4f3ae9f.js";import"./c.eeecae56.js";let v=e([h("hacs-add-repository-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[i({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[i({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[i()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[i()],key:"_sortBy",value:()=>"stars"},{kind:"field",decorators:[i()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return e.forEach((e,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))}),e.has("narrow")||e.has("filters")||e.has("active")||e.has("_searchInput")||e.has("_load")||e.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(e,t)=>null==e?void 0:e.filter(e=>{var i,o;return!e.installed&&(null===(i=this.hacs.sections)||void 0===i||null===(o=i.find(e=>e.id===this.section).categories)||void 0===o?void 0:o.includes(e.category))&&!e.installed&&(null==t?void 0:t.includes(e.category))})}},{kind:"method",key:"firstUpdated",value:async function(){var e;if(this.addEventListener("filter-change",e=>this._updateFilters(e)),0===(null===(e=this.filters)||void 0===e?void 0:e.length)){var t;const e=null===(t=o(this.route))||void 0===t?void 0:t.categories;null==e||e.filter(e=>{var t;return null===(t=this.hacs.configuration)||void 0===t?void 0:t.categories.includes(e)}).forEach(e=>{this.filters.push({id:e,value:e,checked:!0})}),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(e){const t=this.filters.find(t=>t.id===e.detail.id);this.filters.find(e=>e.id===t.id).checked=!t.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>a(u)},{kind:"method",key:"render",value:function(){var e;if(!this.active)return r``;this._searchInput=window.localStorage.getItem("hacs-search")||"";let t=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(e=this.hacs.configuration)||void 0===e?void 0:e.categories),this._searchInput);return 0!==this.filters.length&&(t=t.filter(e=>{var t;return null===(t=this.filters.find(t=>t.id===e.category))||void 0===t?void 0:t.checked})),r`
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
        <div class=${d({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${d({list:!0,narrow:this.narrow})}>
            ${t.sort((e,t)=>"name"===this._sortBy?e.name.toLocaleLowerCase()<t.name.toLocaleLowerCase()?-1:1:e[this._sortBy]>t[this._sortBy]?-1:1).slice(0,this._load).map(e=>r`<paper-icon-item
                  class=${d({narrow:this.narrow})}
                  @click=${()=>this._openInformation(e)}
                >
                  ${"integration"===e.category?r`
                        <img
                          src="https://brands.home-assistant.io/_/${e.domain}/icon.png"
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${n} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body two-line
                    >${e.name}
                    <div class="category-chip">
                      <hacs-chip
                        .icon=${f}
                        .value=${s("common."+e.category)}
                      ></hacs-chip>
                    </div>
                    <div secondary>${e.description}</div>
                  </paper-item-body>
                </paper-icon-item>`)}
            ${0===t.length?r`<p>${s("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(e){const t=e.target.scrollTop;t>=this._top?this._load+=1:this._load-=1,this._top=t}},{kind:"method",key:"_inputValueChanged",value:function(e){this._searchInput=e.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(e){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:e.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target&&(e.target.outerHTML=`<ha-svg-icon .path=${n} slot="item-icon"></ha-svg-icon>`)}},{kind:"get",static:!0,key:"styles",value:function(){return[l,c,p`
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
      `]}}]}}),t);export{v as HacsAddRepositoryDialog};
