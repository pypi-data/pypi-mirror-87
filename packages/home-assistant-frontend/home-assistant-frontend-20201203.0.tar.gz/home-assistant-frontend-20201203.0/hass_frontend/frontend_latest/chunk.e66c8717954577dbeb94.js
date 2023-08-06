/*! For license information please see chunk.e66c8717954577dbeb94.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1389,2926,5823,3099],{90440:(t,e,i)=>{"use strict";function r(t){return void 0===t&&(t=window),!!function(t){void 0===t&&(t=window);var e=!1;try{var i={get passive(){return e=!0,!1}},r=function(){};t.document.addEventListener("test",r,i),t.document.removeEventListener("test",r,i)}catch(t){e=!1}return e}(t)&&{passive:!0}}i.d(e,{K:()=>r})},8470:(t,e,i)=>{"use strict";i.d(e,{o:()=>r});const r=i(15652).iv`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch)[dir=rtl]{margin-left:10px}`},50190:(t,e,i)=>{"use strict";var r=i(87480),o=i(15652),a=i(72774),n={ROOT:"mdc-form-field"},l={LABEL_SELECTOR:".mdc-form-field > label"};const d=function(t){function e(i){var o=t.call(this,(0,r.pi)((0,r.pi)({},e.defaultAdapter),i))||this;return o.click=function(){o.handleClick()},o}return(0,r.ZT)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return n},enumerable:!0,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return l},enumerable:!0,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!0,configurable:!0}),e.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},e.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},e.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},e}(a.K);var s=i(78220),p=i(18601),c=i(14114),f=i(82612),m=i(81471);class y extends s.H{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=d}createAdapter(){return{registerInteractionHandler:(t,e)=>{this.labelEl.addEventListener(t,e)},deregisterInteractionHandler:(t,e)=>{this.labelEl.removeEventListener(t,e)},activateInputRipple:async()=>{const t=this.input;if(t instanceof p.Wg){const e=await t.ripple;e&&e.startPress()}},deactivateInputRipple:async()=>{const t=this.input;if(t instanceof p.Wg){const e=await t.ripple;e&&e.endPress()}}}}get input(){return(0,f.f6)(this.slotEl,"*")}render(){const t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return o.dy`
      <div class="mdc-form-field ${(0,m.$)(t)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}_labelClick(){const t=this.input;t&&(t.focus(),t.click())}}(0,r.gn)([(0,o.Cb)({type:Boolean})],y.prototype,"alignEnd",void 0),(0,r.gn)([(0,o.Cb)({type:Boolean})],y.prototype,"spaceBetween",void 0),(0,r.gn)([(0,o.Cb)({type:Boolean})],y.prototype,"nowrap",void 0),(0,r.gn)([(0,o.Cb)({type:String}),(0,c.P)((async function(t){const e=this.input;e&&("input"===e.localName?e.setAttribute("aria-label",t):e instanceof p.Wg&&(await e.updateComplete,e.setAriaLabel(t)))}))],y.prototype,"label",void 0),(0,r.gn)([(0,o.IO)(".mdc-form-field")],y.prototype,"mdcRoot",void 0),(0,r.gn)([(0,o.IO)("slot")],y.prototype,"slotEl",void 0),(0,r.gn)([(0,o.IO)("label")],y.prototype,"labelEl",void 0);var h=i(8470);let g=class extends y{};g.styles=h.o,g=(0,r.gn)([(0,o.Mo)("mwc-formfield")],g)},25782:(t,e,i)=>{"use strict";i(43437),i(65660),i(70019),i(97968);var r=i(9672),o=i(50856),a=i(33760);(0,r.k)({_template:o.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[a.U]})},89194:(t,e,i)=>{"use strict";i(43437),i(65660),i(70019);var r=i(9672),o=i(50856);(0,r.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},1275:(t,e,i)=>{"use strict";i.d(e,{l:()=>a});var r=i(94707);const o=new WeakMap,a=(0,r.XM)(((t,e)=>i=>{const r=o.get(i);if(Array.isArray(t)){if(Array.isArray(r)&&r.length===t.length&&t.every(((t,e)=>t===r[e])))return}else if(r===t&&(void 0!==t||o.has(i)))return;i.setValue(e()),o.set(i,Array.isArray(t)?Array.from(t):t)}))}}]);
//# sourceMappingURL=chunk.e66c8717954577dbeb94.js.map