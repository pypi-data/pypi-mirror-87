import{ak as e,S as t,h as i,d as o,_ as a,e as r,f as s,c as n,L as d,p as c,al as l,t as p,am as h,an as u,g as m,ao as b,w as f,n as v,l as g,ap as x,T as y,aq as _,Y as k,a1 as w,a2 as $,k as S,P as R,o as P,ar as z,v as C,as as T,at as E,au as A,y as U,s as j}from"./e.4add7a3d.js";import"./c.02702101.js";import{a as O}from"./c.e68bb6ba.js";import{P as I}from"./c.7c3326e3.js";import"./c.1d4ba97d.js";import{h as F,f as B}from"./c.e4f3ae9f.js";import{i as H}from"./c.2d4d36d6.js";function L(e,t,i,o){var a,r=arguments.length,s=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(s=(r<3?a(s):r>3?a(t,i,s):a(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}window.JSCompiler_renameProperty=(e,t)=>e;const D={toAttribute(e,t){switch(t){case Boolean:return e?"":null;case Object:case Array:return null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){switch(t){case Boolean:return null!==e;case Number:return null===e?null:Number(e);case Object:case Array:return JSON.parse(e)}return e}},M=(e,t)=>t!==e&&(t==t||e==e),N={attribute:!0,type:String,converter:D,reflect:!1,hasChanged:M};class q extends HTMLElement{constructor(){super(),this._updateState=0,this._instanceProperties=void 0,this._updatePromise=new Promise(e=>this._enableUpdatingResolver=e),this._changedProperties=new Map,this._reflectingProperties=void 0,this.initialize()}static get observedAttributes(){this.finalize();const e=[];return this._classProperties.forEach((t,i)=>{const o=this._attributeNameForProperty(i,t);void 0!==o&&(this._attributeToPropertyMap.set(o,i),e.push(o))}),e}static _ensureClassProperties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties",this))){this._classProperties=new Map;const e=Object.getPrototypeOf(this)._classProperties;void 0!==e&&e.forEach((e,t)=>this._classProperties.set(t,e))}}static createProperty(e,t=N){if(this._ensureClassProperties(),this._classProperties.set(e,t),t.noAccessor||this.prototype.hasOwnProperty(e))return;const i="symbol"==typeof e?Symbol():"__"+e,o=this.getPropertyDescriptor(e,i,t);void 0!==o&&Object.defineProperty(this.prototype,e,o)}static getPropertyDescriptor(e,t,i){return{get(){return this[t]},set(i){const o=this[e];this[t]=i,this._requestUpdate(e,o)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this._classProperties&&this._classProperties.get(e)||N}static finalize(){const e=Object.getPrototypeOf(this);if(e.hasOwnProperty("finalized")||e.finalize(),this.finalized=!0,this._ensureClassProperties(),this._attributeToPropertyMap=new Map,this.hasOwnProperty(JSCompiler_renameProperty("properties",this))){const e=this.properties,t=[...Object.getOwnPropertyNames(e),..."function"==typeof Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(e):[]];for(const i of t)this.createProperty(i,e[i])}}static _attributeNameForProperty(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}static _valueHasChanged(e,t,i=M){return i(e,t)}static _propertyValueFromAttribute(e,t){const i=t.type,o=t.converter||D,a="function"==typeof o?o:o.fromAttribute;return a?a(e,i):e}static _propertyValueToAttribute(e,t){if(void 0===t.reflect)return;const i=t.type,o=t.converter;return(o&&o.toAttribute||D.toAttribute)(e,i)}initialize(){this._saveInstanceProperties(),this._requestUpdate()}_saveInstanceProperties(){this.constructor._classProperties.forEach((e,t)=>{if(this.hasOwnProperty(t)){const e=this[t];delete this[t],this._instanceProperties||(this._instanceProperties=new Map),this._instanceProperties.set(t,e)}})}_applyInstanceProperties(){this._instanceProperties.forEach((e,t)=>this[t]=e),this._instanceProperties=void 0}connectedCallback(){this.enableUpdating()}enableUpdating(){void 0!==this._enableUpdatingResolver&&(this._enableUpdatingResolver(),this._enableUpdatingResolver=void 0)}disconnectedCallback(){}attributeChangedCallback(e,t,i){t!==i&&this._attributeToProperty(e,i)}_propertyToAttribute(e,t,i=N){const o=this.constructor,a=o._attributeNameForProperty(e,i);if(void 0!==a){const e=o._propertyValueToAttribute(t,i);if(void 0===e)return;this._updateState=8|this._updateState,null==e?this.removeAttribute(a):this.setAttribute(a,e),this._updateState=-9&this._updateState}}_attributeToProperty(e,t){if(8&this._updateState)return;const i=this.constructor,o=i._attributeToPropertyMap.get(e);if(void 0!==o){const e=i.getPropertyOptions(o);this._updateState=16|this._updateState,this[o]=i._propertyValueFromAttribute(t,e),this._updateState=-17&this._updateState}}_requestUpdate(e,t){let i=!0;if(void 0!==e){const o=this.constructor,a=o.getPropertyOptions(e);o._valueHasChanged(this[e],t,a.hasChanged)?(this._changedProperties.has(e)||this._changedProperties.set(e,t),!0!==a.reflect||16&this._updateState||(void 0===this._reflectingProperties&&(this._reflectingProperties=new Map),this._reflectingProperties.set(e,a))):i=!1}!this._hasRequestedUpdate&&i&&(this._updatePromise=this._enqueueUpdate())}requestUpdate(e,t){return this._requestUpdate(e,t),this.updateComplete}async _enqueueUpdate(){this._updateState=4|this._updateState;try{await this._updatePromise}catch(e){}const e=this.performUpdate();return null!=e&&await e,!this._hasRequestedUpdate}get _hasRequestedUpdate(){return 4&this._updateState}get hasUpdated(){return 1&this._updateState}performUpdate(){this._instanceProperties&&this._applyInstanceProperties();let e=!1;const t=this._changedProperties;try{e=this.shouldUpdate(t),e?this.update(t):this._markUpdated()}catch(t){throw e=!1,this._markUpdated(),t}e&&(1&this._updateState||(this._updateState=1|this._updateState,this.firstUpdated(t)),this.updated(t))}_markUpdated(){this._changedProperties=new Map,this._updateState=-5&this._updateState}get updateComplete(){return this._getUpdateComplete()}_getUpdateComplete(){return this._updatePromise}shouldUpdate(e){return!0}update(e){void 0!==this._reflectingProperties&&this._reflectingProperties.size>0&&(this._reflectingProperties.forEach((e,t)=>this._propertyToAttribute(t,this[t],e)),this._reflectingProperties=void 0),this._markUpdated()}updated(e){}firstUpdated(e){}}q.finalized=!0;const V=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?Object.assign(Object.assign({},t),{finisher(i){i.createProperty(t.key,e)}}):{kind:"field",key:Symbol(),placement:"own",descriptor:{},initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(i){i.createProperty(t.key,e)}};function J(e){return(t,i)=>void 0!==i?((e,t,i)=>{t.constructor.createProperty(i,e)})(e,t,i):V(e,t)}const K=(e,t,i)=>{Object.defineProperty(t,i,e)},W=(e,t)=>({kind:"method",placement:"prototype",key:t.key,descriptor:e});const G="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Y=Symbol();class Q{constructor(e,t){if(t!==Y)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return void 0===this._styleSheet&&(G?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}(window.litElementVersions||(window.litElementVersions=[])).push("2.3.1");const X={};class Z extends q{static getStyles(){return this.styles}static _getUniqueStyles(){if(this.hasOwnProperty(JSCompiler_renameProperty("_styles",this)))return;const e=this.getStyles();if(void 0===e)this._styles=[];else if(Array.isArray(e)){const t=(e,i)=>e.reduceRight((e,i)=>Array.isArray(i)?t(i,e):(e.add(i),e),i),i=t(e,new Set),o=[];i.forEach(e=>o.unshift(e)),this._styles=o}else this._styles=[e]}initialize(){super.initialize(),this.constructor._getUniqueStyles(),this.renderRoot=this.createRenderRoot(),window.ShadowRoot&&this.renderRoot instanceof window.ShadowRoot&&this.adoptStyles()}createRenderRoot(){return this.attachShadow({mode:"open"})}adoptStyles(){const e=this.constructor._styles;0!==e.length&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow?G?this.renderRoot.adoptedStyleSheets=e.map(e=>e.styleSheet):this._needsShimAdoptedStyleSheets=!0:window.ShadyCSS.ScopingShim.prepareAdoptedCssText(e.map(e=>e.cssText),this.localName))}connectedCallback(){super.connectedCallback(),this.hasUpdated&&void 0!==window.ShadyCSS&&window.ShadyCSS.styleElement(this)}update(e){const t=this.render();super.update(e),t!==X&&this.constructor.render(t,this.renderRoot,{scopeName:this.localName,eventContext:this}),this._needsShimAdoptedStyleSheets&&(this._needsShimAdoptedStyleSheets=!1,this.constructor._styles.forEach(e=>{const t=document.createElement("style");t.textContent=e.cssText,this.renderRoot.appendChild(t)}))}render(){return X}}Z.finalized=!0,Z.render=e;class ee extends Z{constructor(){super(...arguments),this.mini=!1,this.exited=!1,this.disabled=!1,this.extended=!1,this.showIconAtEnd=!1,this.reducedTouchTarget=!1,this.icon="",this.label="",this.shouldRenderRipple=!1,this.rippleHandlers=new t(()=>(this.shouldRenderRipple=!0,this.ripple))}createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}render(){const e=this.mini&&!this.reducedTouchTarget,t={"mdc-fab--mini":this.mini,"mdc-fab--touch":e,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended,"icon-end":this.showIconAtEnd},a=this.label?this.label:this.icon;return i`
      <button
          class="mdc-fab ${o(t)}"
          ?disabled="${this.disabled}"
          aria-label="${a}"
          @mouseenter=${this.handleRippleMouseEnter}
          @mouseleave=${this.handleRippleMouseLeave}
          @focus=${this.handleRippleFocus}
          @blur=${this.handleRippleBlur}
          @mousedown=${this.handleRippleActivate}
          @touchstart=${this.handleRippleStartPress}
          @touchend=${this.handleRippleDeactivate}
          @touchcancel=${this.handleRippleDeactivate}>
        ${this.renderBeforeRipple()}
        ${this.renderRipple()}
        ${this.showIconAtEnd?this.renderLabel():""}
        <span class="icon-slot-container">
          <slot name="icon">
            ${this.renderIcon()}
          </slot>
        </span>
        ${this.showIconAtEnd?"":this.renderLabel()}
        ${this.renderTouchTarget()}
      </button>`}renderIcon(){return i`${this.icon?i`
          <span class="material-icons mdc-fab__icon">${this.icon}</span>`:""}`}renderTouchTarget(){const e=this.mini&&!this.reducedTouchTarget;return i`${e?i`<div class="mdc-fab__touch"></div>`:""}`}renderLabel(){const e=""!==this.label&&this.extended;return i`${e?i`<span class="mdc-fab__label">${this.label}</span>`:""}`}renderBeforeRipple(){return i``}renderRipple(){return this.shouldRenderRipple?i`<mwc-ripple class="ripple"></mwc-ripple>`:""}handleRippleActivate(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.handleRippleStartPress(e)}handleRippleStartPress(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}var te,ie;L([(te="mwc-ripple",(e,t)=>{const i={async get(){return await this.updateComplete,this.renderRoot.querySelector(te)},enumerable:!0,configurable:!0};return void 0!==t?K(i,e,t):W(i,e)})],ee.prototype,"ripple",void 0),L([J({type:Boolean})],ee.prototype,"mini",void 0),L([J({type:Boolean})],ee.prototype,"exited",void 0),L([J({type:Boolean})],ee.prototype,"disabled",void 0),L([J({type:Boolean})],ee.prototype,"extended",void 0),L([J({type:Boolean})],ee.prototype,"showIconAtEnd",void 0),L([J({type:Boolean})],ee.prototype,"reducedTouchTarget",void 0),L([J()],ee.prototype,"icon",void 0),L([J()],ee.prototype,"label",void 0),L([J({attribute:!1,hasChanged:null==ie?void 0:ie.hasChanged})],ee.prototype,"shouldRenderRipple",void 0),L([function(e){return(t,i)=>void 0!==i?((e,t,i)=>{Object.assign(t[i],e)})(e,t,i):((e,t)=>Object.assign(Object.assign({},t),{finisher(i){Object.assign(i.prototype[t.key],e)}}))(e,t)}({passive:!0})],ee.prototype,"handleRippleStartPress",null);const oe=((e,...t)=>{const i=t.reduce((t,i,o)=>t+(e=>{if(e instanceof Q)return e.cssText;if("number"==typeof e)return e;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${e}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(i)+e[o+1],e[0]);return new Q(i,Y)})`:host .mdc-fab .material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}:host{outline:none;--mdc-ripple-color: currentcolor;user-select:none;-webkit-tap-highlight-color:transparent;display:inline-flex}:host .mdc-touch-target-wrapper{display:inline}:host .mdc-elevation-overlay{position:absolute;border-radius:inherit;pointer-events:none;opacity:0;opacity:var(--mdc-elevation-overlay-opacity, 0);transition:opacity 280ms cubic-bezier(0.4, 0, 0.2, 1);background-color:#fff;background-color:var(--mdc-elevation-overlay-color, #fff)}:host .mdc-fab{position:relative;box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2),0px 6px 10px 0px rgba(0, 0, 0, 0.14),0px 1px 18px 0px rgba(0,0,0,.12);display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1);background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);color:#fff;color:var(--mdc-theme-on-secondary, #fff)}:host .mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}:host .mdc-fab:not(.mdc-fab--extended){border-radius:50%}:host .mdc-fab:not(.mdc-fab--extended) .mdc-fab__ripple{border-radius:50%}:host .mdc-fab::-moz-focus-inner{padding:0;border:0}:host .mdc-fab:hover,:host .mdc-fab:focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus{outline:none}:host .mdc-fab:hover{cursor:pointer}:host .mdc-fab>svg{width:100%}:host .mdc-fab .mdc-fab__icon{width:24px;height:24px;font-size:24px}:host .mdc-fab--mini{width:40px;height:40px}:host .mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding-left:20px;padding-right:20px;width:auto;max-width:100%;height:48px;line-height:normal}:host .mdc-fab--extended .mdc-fab__ripple{border-radius:24px}:host .mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-right:12px}[dir=rtl] :host .mdc-fab--extended .mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:calc(12px - 20px)}:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:calc(12px - 20px)}[dir=rtl] :host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-right:12px}:host .mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}:host .mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;right:0;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host .mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:""}:host .mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}:host .mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}:host .mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab{box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12))}:host .mdc-fab:hover,:host .mdc-fab:focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12))}:host .mdc-fab:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12))}:host .mdc-fab .ripple{overflow:hidden}:host .mdc-fab .mdc-fab__label{z-index:0}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab.mdc-fab--extended .ripple{border-radius:24px}:host .mdc-fab .icon-slot-container{display:inline-flex}:host .mdc-fab .mdc-fab__icon,:host .mdc-fab .icon-slot-container ::slotted([slot=icon]){width:24px;width:var(--mdc-icon-size, 24px);height:24px;height:var(--mdc-icon-size, 24px);font-size:24px;font-size:var(--mdc-icon-size, 24px);transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform;display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab.mdc-fab--extended{padding-left:20px;padding-left:var(--mdc-fab-extended-label-padding, 20px);padding-right:20px;padding-right:var(--mdc-fab-extended-label-padding, 20px)}:host .mdc-fab.mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}[dir=rtl] :host .mdc-fab.mdc-fab--extended .mdc-fab__icon,:host .mdc-fab.mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}:host .mdc-fab.mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab.mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}:host .mdc-fab.mdc-fab--extended .icon-slot-container ::slotted([slot=icon]){margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}[dir=rtl] :host .mdc-fab.mdc-fab--extended .icon-slot-container ::slotted([slot=icon]),:host .mdc-fab.mdc-fab--extended .icon-slot-container ::slotted([slot=icon])[dir=rtl]{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon,:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}:host .mdc-fab.mdc-fab--extended.icon-end .icon-slot-container ::slotted([slot=icon]){margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended.icon-end .icon-slot-container ::slotted([slot=icon]),:host .mdc-fab.mdc-fab--extended.icon-end .icon-slot-container ::slotted([slot=icon])[dir=rtl]{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}:host .mdc-fab.mdc-fab--exited .icon-slot-container ::slotted([slot=icon]){transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}`;let ae=class extends ee{};var re;ae.styles=oe,ae=L([(re="mwc-fab",e=>"function"==typeof e?((e,t)=>(window.customElements.define(e,t),t))(re,e):((e,t)=>{const{kind:i,elements:o}=t;return{kind:i,elements:o,finisher(t){window.customElements.define(e,t)}}})(re,e))],ae);const se=customElements.get("mwc-fab");a([n("ha-fab")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(e){r(s(i.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),se),a([n("ha-tab")],(function(e,o){return{F:class extends o{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[c({type:Boolean,reflect:!0})],key:"active",value:()=>!1},{kind:"field",decorators:[c({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[c()],key:"name",value:void 0},{kind:"field",decorators:[l("mwc-ripple")],key:"_ripple",value:void 0},{kind:"field",decorators:[p()],key:"_shouldRenderRipple",value:()=>!1},{kind:"method",key:"render",value:function(){return i`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${h(this.name)}
        @focus=${this.handleRippleFocus}
        @blur=${this.handleRippleBlur}
        @mousedown=${this.handleRippleActivate}
        @mouseup=${this.handleRippleDeactivate}
        @mouseenter=${this.handleRippleMouseEnter}
        @mouseleave=${this.handleRippleMouseLeave}
        @touchstart=${this.handleRippleActivate}
        @touchend=${this.handleRippleDeactivate}
        @touchcancel=${this.handleRippleDeactivate}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?i`<slot name="icon"></slot>`:""}
        ${!this.narrow||this.active?i`<span class="name">${this.name}</span>`:""}
        ${this._shouldRenderRipple?i`<mwc-ripple></mwc-ripple>`:""}
      </div>
    `}},{kind:"field",key:"_rippleHandlers",value(){return new t(()=>(this._shouldRenderRipple=!0,this._ripple))}},{kind:"method",key:"_handleKeyDown",value:function(e){13===e.keyCode&&e.target.click()}},{kind:"method",decorators:[u({passive:!0})],key:"handleRippleActivate",value:function(e){this._rippleHandlers.startPress(e)}},{kind:"method",key:"handleRippleDeactivate",value:function(){this._rippleHandlers.endPress()}},{kind:"method",key:"handleRippleMouseEnter",value:function(){this._rippleHandlers.startHover()}},{kind:"method",key:"handleRippleMouseLeave",value:function(){this._rippleHandlers.endHover()}},{kind:"method",key:"handleRippleFocus",value:function(){this._rippleHandlers.startFocus()}},{kind:"method",key:"handleRippleBlur",value:function(){this._rippleHandlers.endFocus()}},{kind:"get",static:!0,key:"styles",value:function(){return m`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        padding: 0 16px;
        width: 20%;
        min-width: 0;
      }
    `}}]}}),d),a([n("hass-tabs-subpage")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[c({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[c({type:Boolean})],key:"hassio",value:()=>!1},{kind:"field",decorators:[c({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[c()],key:"backCallback",value:void 0},{kind:"field",decorators:[c({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[c()],key:"route",value:void 0},{kind:"field",decorators:[c()],key:"tabs",value:void 0},{kind:"field",decorators:[c({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[c({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value:()=>!1},{kind:"field",decorators:[c({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[p()],key:"_activeTab",value:void 0},{kind:"field",decorators:[b(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return f((e,t,o,a,r,s)=>e.filter(e=>(!e.component||e.core||H(this.hass,e.component))&&(!e.advancedOnly||o)).map(e=>i`
            <ha-tab
              .hass=${this.hass}
              @click=${this._tabTapped}
              .path=${e.path}
              .active=${e===t}
              .narrow=${this.narrow}
              .name=${e.translationKey?this.hass.localize(e.translationKey):e.name}
            >
              ${e.iconPath?i`<ha-svg-icon
                    slot="icon"
                    .path=${e.iconPath}
                  ></ha-svg-icon>`:i`<ha-icon slot="icon" .icon=${e.icon}></ha-icon>`}
            </ha-tab>
          `))}},{kind:"method",key:"updated",value:function(e){if(r(s(a.prototype),"updated",this).call(this,e),e.has("route")&&(this._activeTab=this.tabs.find(e=>`${this.route.prefix}${this.route.path}`.includes(e.path))),e.has("hass")){const t=e.get("hass");t&&t.language===this.hass.language||(this.rtl=O(this.hass))}}},{kind:"method",key:"render",value:function(){var e;const t=this._getTabs(this.tabs,this._activeTab,null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced,this.hass.config.components,this.hass.language,this.narrow),a=t.length>1||!this.narrow;return i`
      <div class="toolbar">
        ${this.mainPage?i`
              <ha-menu-button
                .hassio=${this.hassio}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:i`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}
        ${this.narrow?i` <div class="main-title"><slot name="header"></slot></div> `:""}
        ${a?i`
              <div id="tabbar" class=${o({"bottom-bar":this.narrow})}>
                ${t}
              </div>
            `:""}
        <div id="toolbar-icon">
          <slot name="toolbar-icon"></slot>
        </div>
      </div>
      <div
        class="content ${o({tabs:a})}"
        @scroll=${this._saveScrollPos}
      >
        <slot></slot>
      </div>
      <div id="fab" class="${o({tabs:a})}">
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[u({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_tabTapped",value:function(e){v(this,e.currentTarget.path,!0)}},{kind:"method",key:"_backTapped",value:function(){this.backPath?v(this,this.backPath):this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return m`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      ha-menu-button {
        margin-right: 24px;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        background-color: var(--sidebar-background-color);
        font-weight: 400;
        color: var(--sidebar-text-color);
        border-bottom: 1px solid var(--divider-color);
        padding: 0 16px;
        box-sizing: border-box;
      }

      #tabbar {
        display: flex;
        font-size: 14px;
      }

      #tabbar.bottom-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 16px;
        box-sizing: border-box;
        background-color: var(--sidebar-background-color);
        border-top: 1px solid var(--divider-color);
        justify-content: space-between;
        z-index: 2;
        font-size: 12px;
        width: 100%;
        padding-bottom: env(safe-area-inset-bottom);
      }

      #tabbar:not(.bottom-bar) {
        flex: 1;
        justify-content: center;
      }

      :host(:not([narrow])) #toolbar-icon {
        min-width: 40px;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        flex-shrink: 0;
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        max-height: 58px;
        line-height: 20px;
      }

      .content {
        position: relative;
        width: calc(
          100% - env(safe-area-inset-left) - env(safe-area-inset-right)
        );
        margin-left: env(safe-area-inset-left);
        margin-right: env(safe-area-inset-right);
        height: calc(100% - 1px - var(--header-height));
        height: calc(
          100% - 1px - var(--header-height) - env(safe-area-inset-bottom)
        );
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([narrow]) .content.tabs {
        height: calc(100% - 128px);
        height: calc(100% - 128px - env(safe-area-inset-bottom));
      }

      #fab {
        position: fixed;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      :host([narrow]) #fab.tabs {
        bottom: calc(84px + env(safe-area-inset-bottom));
      }
      #fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
      :host([rtl]) #fab {
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
      :host([rtl][is-wide]) #fab {
        bottom: 24px;
        left: 24px;
        right: auto;
      }
    `}}]}}),d),a([n("hacs-fab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[c()],key:"icon",value:void 0},{kind:"field",decorators:[c({type:Boolean})],key:"narrow",value:void 0},{kind:"method",key:"render",value:function(){return i`
      <div class="fab" ?narrow=${this.narrow}>
        <div><ha-icon .icon=${this.icon}></ha-icon></div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[m`
        .fab {
          position: fixed;
          bottom: 16px;
          right: 16px;
          z-index: 1;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          box-sizing: border-box;
          width: 56px;
          height: 56px;
          cursor: pointer;
          user-select: none;
          -webkit-appearance: none;
          background-color: var(--hcv-color-fab);
          -webkit-box-shadow: 2px 2px 8px 1px rgba(0, 0, 0, 0.3);
          -moz-box-shadow: 2px 2px 8px 1px rgba(0, 0, 0, 0.3);
          box-shadow: 2px 2px 8px 1px rgba(0, 0, 0, 0.3);
          border-radius: 50%;
        }
        .fab[narrow] {
          margin-bottom: 65px;
        }
        ha-icon {
          margin: auto;
          color: var(--hcv-text-color-fab);
          height: 100%;
          width: 100%;
          --mdc-icon-size: 32px;
        }
      `]}}]}}),d),a([n("hacs-repository-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[c({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"status",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"removed",value:void 0},{kind:"field",decorators:[c({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[c({type:Boolean})],key:"addedToLovelace",value:void 0},{kind:"get",key:"_borderClass",value:function(){const e={};return this.addedToLovelace&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?e["status-update"]=!0:this.repository.new&&!this.repository.installed&&(e["status-new"]=!0):e["status-issue"]=!0,0!==Object.keys(e).length&&(e["status-border"]=!0),e}},{kind:"get",key:"_headerClass",value:function(){const e={};return this.addedToLovelace&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?e["update-header"]=!0:this.repository.new&&!this.repository.installed?e["new-header"]=!0:e["default-header"]=!0:e["issue-header"]=!0,e}},{kind:"get",key:"_headerTitle",value:function(){return this.addedToLovelace?"pending-restart"===this.repository.status?g("repository_card.pending_restart"):this.repository.pending_upgrade?g("repository_card.pending_update"):this.repository.new&&!this.repository.installed?g("repository_card.new_repository"):"":g("repository_card.not_loaded")}},{kind:"method",key:"render",value:function(){const e=this.repository.local_path.split("/");return i`
      <ha-card class=${o(this._borderClass)} ?narrow=${this.narrow}>
        <div class="card-content">
          <div class="group-header">
            <div class="status-header ${o(this._headerClass)}">
              ${this._headerTitle}
            </div>
            <div class="title">
              <h1 class="pointer" @click=${this._showReopsitoryInfo}>
                ${this.repository.name}
              </h1>
              ${"integration"!==this.repository.category?i` <hacs-chip
                    .icon=${F}
                    .value=${g("common."+this.repository.category)}
                  ></hacs-chip>`:""}
            </div>
          </div>
          <paper-item>
            <paper-item-body>${this.repository.description}</paper-item-body></paper-item
          >
        </div>
        <div class="card-actions">
          ${this.repository.new&&!this.repository.installed?i`<div>
                  <mwc-button @click=${this._installRepository}
                    >${g("common.install")}</mwc-button
                  >
                </div>
                <div>
                  <mwc-button @click=${this._showReopsitoryInfo}
                    >${g("repository_card.information")}</mwc-button
                  >
                </div>
                <div>
                  <hacs-link .url="https://github.com/${this.repository.full_name}"
                    ><mwc-button>${g("common.repository")}</mwc-button></hacs-link
                  >
                </div>
                <div>
                  <mwc-button @click=${this._setNotNew}
                    >${g("repository_card.dismiss")}</mwc-button
                  >
                </div>`:this.repository.pending_upgrade&&this.addedToLovelace?i`<div>
                  <mwc-button class="update-header" @click=${this._updateRepository} raised
                    >${g("common.update")}</mwc-button
                  >
                </div>
                <div>
                  <hacs-link .url="https://github.com/${this.repository.full_name}"
                    ><mwc-button>${g("common.repository")}</mwc-button></hacs-link
                  >
                </div>`:i`<div>
                <hacs-link .url="https://github.com/${this.repository.full_name}"
                  ><mwc-button>${g("common.repository")}</mwc-button></hacs-link
                >
              </div>`}
          ${this.repository.installed?i` <paper-menu-button
                horizontal-align="right"
                vertical-align="top"
                vertical-offset="40"
                close-on-activate
              >
                <hacs-icon-button
                  .icon=${x}
                  slot="dropdown-trigger"
                ></hacs-icon-button>
                <paper-listbox slot="dropdown-content">
                  <paper-item class="pointer" @tap=${this._showReopsitoryInfo}
                    >${g("repository_card.information")}</paper-item
                  >

                  <paper-item class="pointer" @tap=${this._updateReopsitoryInfo}
                    >${g("repository_card.update_information")}</paper-item
                  >

                  <paper-item @tap=${this._installRepository}
                    >${g("repository_card.reinstall")}</paper-item
                  >

                  ${"plugin"===this.repository.category?i`<hacs-link
                        .url="/hacsfiles/${e.pop()}/${this.repository.file_name}"
                        newtab
                        ><paper-item class="pointer"
                          >${g("repository_card.open_source")}</paper-item
                        ></hacs-link
                      >`:""}

                  <hacs-link .url="https://github.com/${this.repository.full_name}/issues"
                    ><paper-item class="pointer"
                      >${g("repository_card.open_issue")}</paper-item
                    ></hacs-link
                  >

                  ${"172733314"!==String(this.repository.id)?i`<hacs-link
                          .url="https://github.com/hacs/integration/issues/new?assignees=ludeeus&labels=flag&template=flag.md&title=${this.repository.full_name}"
                          ><paper-item class="pointer uninstall"
                            >${g("repository_card.report")}</paper-item
                          ></hacs-link
                        >
                        <paper-item class="pointer uninstall" @tap=${this._uninstallRepository}
                          >${g("common.uninstall")}</paper-item
                        >`:""}
                </paper-listbox>
              </paper-menu-button>`:""}
        </div>
      </ha-card>
    `}},{kind:"method",key:"_updateReopsitoryInfo",value:async function(){await y(this.hass,this.repository.id)}},{kind:"method",key:"_showReopsitoryInfo",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"repository-info",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_lovelaceUrl",value:function(){var e,t;return`/hacsfiles/${null===(e=this.repository)||void 0===e?void 0:e.full_name.split("/")[1]}/${null===(t=this.repository)||void 0===t?void 0:t.file_name}`}},{kind:"method",key:"_updateRepository",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"update",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_setNotNew",value:async function(){await _(this.hass,this.repository.id)}},{kind:"method",key:"_installRepository",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"install",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepository",value:async function(){if("plugin"===this.repository.category&&"yaml"!==this.hacs.status.lovelace_mode){(await k(this.hass)).filter(e=>e.url===this._lovelaceUrl()).forEach(e=>{w(this.hass,String(e.id))})}await $(this.hass,this.repository.id)}},{kind:"get",static:!0,key:"styles",value:function(){return[S,m`
        ha-card {
          display: flex;
          flex-direction: column;
          height: 100%;
          width: 480px;
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
          border-color: transparent;
        }

        hacs-chip {
          margin: 8px 4px 0 0;
        }
        .title {
          display: flex;
          justify-content: space-between;
        }
        .card-content {
          padding: 0 0 3px 0;
          height: 100%;
        }
        .card-actions {
          border-top: none;
          bottom: 0;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 5px;
        }
        .group-header {
          height: auto;
          align-content: center;
        }
        .group-header h1 {
          margin: 0;
          padding: 8px 16px;
        }
        h1 {
          margin-top: 0;
          min-height: 24px;
        }
        paper-menu-button {
          padding: 0;
          float: right;
        }

        .pointer {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
        }

        .status-new {
          border-color: var(--hcv-color-new);
        }

        .status-update {
          border-color: var(--hcv-color-update);
        }

        .status-issue {
          border-color: var(--hcv-color-error);
        }

        .new-header {
          background-color: var(--hcv-color-new);
          color: var(--hcv-text-color-on-background);
          border-radius: var(--ha-card-border-radius, 4px);
        }

        .issue-header {
          background-color: var(--hcv-color-error);
          color: var(--hcv-text-color-on-background);
        }

        .update-header {
          background-color: var(--hcv-color-update);
          color: var(--hcv-text-color-on-background);
        }

        .default-header {
          padding: 10px 0 !important;
        }

        mwc-button.update-header {
          --mdc-theme-primary: var(--hcv-color-update);
          --mdc-theme-on-primary: var(--hcv-text-color-on-background);
        }

        .status-border {
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
        }

        .status-header {
          top: 0;
          padding: 6px 1px;
          margin: -1px;
          width: 100%;
          font-weight: 300;
          text-align: center;
          left: 0;
          border-top-left-radius: var(--ha-card-border-radius);
          border-top-right-radius: var(--ha-card-border-radius);
        }

        ha-card[narrow] {
          width: calc(100% - 24px);
          margin: 11px;
        }
        hacs-icon-button {
          color: var(--accent-color);
        }
      `]}}]}}),d);R({_template:P`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[I]});a([n("hacs-tabbed-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[c({attribute:!1})],key:"configuration",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"repositories",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"status",value:void 0},{kind:"method",key:"render",value:function(){var e,t,o;return i`<paper-menu-button
      slot="toolbar-icon"
      horizontal-align="right"
      vertical-align="top"
      vertical-offset="40"
      close-on-activate
    >
      <hacs-icon-button .icon=${x} slot="dropdown-trigger"></hacs-icon-button>
      <paper-listbox slot="dropdown-content">
        <hacs-link url="https://hacs.xyz/"
          ><paper-item>${g("menu.documentation")}</paper-item></hacs-link
        >
        ${0!==(null===(e=this.repositories)||void 0===e?void 0:e.filter(e=>e.new).length)?i` <paper-item @tap=${this._clearAllNewRepositories}
              >${g("menu.dismiss")}</paper-item
            >`:""}

        <hacs-link url="https://github.com/hacs"><paper-item>GitHub</paper-item></hacs-link>
        <hacs-link url="https://hacs.xyz/docs/issues"
          ><paper-item>${g("menu.open_issue")}</paper-item></hacs-link
        >
        ${(null===(t=this.status)||void 0===t?void 0:t.disabled)||(null===(o=this.status)||void 0===o?void 0:o.background_task)?"":i`<paper-item @tap=${this._showCustomRepositoriesDialog}
              >${g("menu.custom_repositories")}</paper-item
            >`}

        <paper-item @tap=${this._showAboutDialog}>${g("menu.about")}</paper-item>
      </paper-listbox>
    </paper-menu-button>`}},{kind:"method",key:"_clearAllNewRepositories",value:async function(){await z(this.hass,C(this.route).categories)}},{kind:"method",key:"_showAboutDialog",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"about",configuration:this.configuration,repositories:this.repositories},bubbles:!0,composed:!0}))}},{kind:"method",key:"_showCustomRepositoriesDialog",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"custom-repositories",repositories:this.repositories},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return m`
      paper-menu-button {
        color: var(--hcv-text-color-secondary);
        padding: 0;
      }
      hacs-icon-button {
        color: var(--sidebar-icon-color);
      }
      paper-item {
        cursor: pointer;
      }
      paper-item-body {
        opacity: var(--dark-primary-opacity);
      }
    `}}]}}),d);let ne=a([n("hacs-store-panel")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[c({attribute:!1})],key:"filters",value:()=>({})},{kind:"field",decorators:[c({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[c()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[c({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"isWide",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"repositories",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[c({attribute:!1})],key:"sections",value:void 0},{kind:"field",decorators:[c()],key:"section",value:void 0},{kind:"field",key:"_repositoriesInActiveSection",value(){return f((e,t)=>[(null==e?void 0:e.filter(e=>{var i,o,a;return(null===(i=this.hacs.sections)||void 0===i||null===(o=i.find(e=>e.id===t))||void 0===o||null===(a=o.categories)||void 0===a?void 0:a.includes(e.category))&&e.installed}))||[],(null==e?void 0:e.filter(e=>{var i,o,a;return(null===(i=this.hacs.sections)||void 0===i||null===(o=i.find(e=>e.id===t))||void 0===o||null===(a=o.categories)||void 0===a?void 0:a.includes(e.category))&&e.new&&!e.installed}))||[]])}},{kind:"get",key:"allRepositories",value:function(){const[e,t]=this._repositoriesInActiveSection(this.repositories,this.section);return t.concat(e)}},{kind:"field",key:"_filterRepositories",value:()=>f(B)},{kind:"get",key:"visibleRepositories",value:function(){const e=this.allRepositories.filter(e=>{var t,i;return null===(t=this.filters[this.section])||void 0===t||null===(i=t.find(t=>t.id===e.category))||void 0===i?void 0:i.checked});return this._filterRepositories(e,this._searchInput)}},{kind:"method",key:"firstUpdated",value:async function(){this.addEventListener("filter-change",e=>this._updateFilters(e))}},{kind:"method",key:"_updateFilters",value:function(e){var t;const i=null===(t=this.filters[this.section])||void 0===t?void 0:t.find(t=>t.id===e.detail.id);this.filters[this.section].find(e=>e.id===i.id).checked=!i.checked,this.requestUpdate()}},{kind:"method",key:"render",value:function(){var e;const t=this._repositoriesInActiveSection(this.repositories,this.section)[1];if(!this.filters[this.section]&&this.hacs.configuration.categories){var o;const e=null===(o=C(this.route))||void 0===o?void 0:o.categories;this.filters[this.section]=[],null==e||e.filter(e=>{var t;return null===(t=this.hacs.configuration)||void 0===t?void 0:t.categories.includes(e)}).forEach(e=>{this.filters[this.section].push({id:e,value:e,checked:!0})})}return i`<hass-tabs-subpage
      back-path="/hacs/entry"
      .hass=${this.hass}
      .narrow=${this.narrow}
      .route=${this.route}
      .tabs=${this.hacs.sections}
      hasFab
    >
      <hacs-tabbed-menu
        slot="toolbar-icon"
        .hass=${this.hass}
        .route=${this.route}
        .narrow=${this.narrow}
        .configuration=${this.hacs.configuration}
        .lovelace=${this.hacs.resources}
        .status=${this.hacs.status}
        .repositories=${this.repositories}
      >
      </hacs-tabbed-menu>
      ${this.narrow?i`
            <div slot="header">
              <slot name="header">
                <search-input
                  class="header"
                  no-label-float
                  .label=${this.hacs.localize("search.installed")}
                  .filter=${this._searchInput||""}
                  @value-changed=${this._inputValueChanged}
                ></search-input>
              </slot>
            </div>
          `:i`<div class="search">
            <search-input
              no-label-float
              .label=${0===t.length?this.hacs.localize("search.installed"):this.hacs.localize("search.installed_new")}
              .filter=${this._searchInput||""}
              @value-changed=${this._inputValueChanged}
            ></search-input>
          </div>`}
      <div class="content ${this.narrow?"narrow-content":""}">
        ${(null===(e=this.filters[this.section])||void 0===e?void 0:e.length)>1?i`<div class="filters">
              <hacs-filter .filters="${this.filters[this.section]}"></hacs-filter>
            </div>`:""}
        ${(null==t?void 0:t.length)>10?i`<div class="new-repositories">${g("store.new_repositories_note")}</div>`:""}
        <div class="container ${this.narrow?"narrow":""}">
          ${void 0===this.repositories?"":0===this.allRepositories.length?this._renderEmpty():0===this.visibleRepositories.length?this._renderNoResultsFound():this._renderRepositories()}
        </div>
      </div>
      <ha-fab
        slot="fab"
        .label=${this.hacs.localize("store.add")}
        extended
        @click=${this._addRepository}
      >
        <ha-svg-icon slot="icon" .path=${T}></ha-svg-icon>
      </ha-fab>
    </hass-tabs-subpage>`}},{kind:"method",key:"_renderRepositories",value:function(){return this.visibleRepositories.map(e=>i`<hacs-repository-card
          .hass=${this.hass}
          .hacs=${this.hacs}
          .repository=${e}
          .narrow=${this.narrow}
          ?narrow=${this.narrow}
          .status=${this.hacs.status}
          .removed=${this.hacs.removed}
          .addedToLovelace=${this.hacs.addedToLovelace(this.hacs,e)}
        ></hacs-repository-card>`)}},{kind:"method",key:"_renderNoResultsFound",value:function(){return i`<ha-card class="no-repositories">
      <div class="header">${g("store.no_repositories")} 😕</div>
      <p>
        ${g("store.no_repositories_found_desc1").replace("{searchInput}",this._searchInput)}
        <br />
        ${g("store.no_repositories_found_desc2")}
      </p>
    </ha-card>`}},{kind:"method",key:"_renderEmpty",value:function(){return i`<ha-card class="no-repositories">
      <div class="header">${g("store.no_repositories")} 😕</div>
      <p>
        ${g("store.no_repositories_desc1")}<br />${g("store.no_repositories_desc2")}
      </p>
    </ha-card>`}},{kind:"method",key:"_inputValueChanged",value:function(e){this._searchInput=e.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_addRepository",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"add-repository",repositories:this.repositories,section:this.section},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[S,E,A,U,j,m`
        .filter {
          border-bottom: 1px solid var(--divider-color);
        }
        .content {
          height: calc(100vh - 128px);
          overflow: auto;
        }
        .narrow-content {
          height: calc(100vh - 128px);
        }
        .container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
          justify-items: center;
          grid-gap: 8px 8px;
          padding: 8px 16px 16px;
          margin-bottom: 64px;
        }
        .no-repositories {
          width: 100%;
          text-align: center;
          margin-top: 12px;
        }
        .new-repositories {
          margin: 4px 16px 0 16px;
          color: var(--hcv-text-color-primary);
        }
        hacs-repository-card {
          max-width: 500px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        hacs-repository-card[narrow] {
          width: 100%;
        }
        hacs-repository-card[narrow]:last-of-type {
          margin-bottom: 64px;
        }
        .narrow {
          width: 100%;
          display: block;
          padding: 0px;
          margin: 0;
        }

        .container .narrow {
          margin-bottom: 128px;
        }

        .bottom-bar {
          position: fixed !important;
        }
      `]}}]}}),d);export{ne as HacsStorePanel};
