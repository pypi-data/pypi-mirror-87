/*! For license information please see chunk.692b80117b61b66d1125.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[5667],{90440:(e,t,i)=>{"use strict";function r(e){return void 0===e&&(e=window),!!function(e){void 0===e&&(e=window);var t=!1;try{var i={get passive(){return t=!0,!1}},r=function(){};e.document.addEventListener("test",r,i),e.document.removeEventListener("test",r,i)}catch(e){t=!1}return t}(e)&&{passive:!0}}i.d(t,{K:()=>r})},51654:(e,t,i)=>{"use strict";i.d(t,{Z:()=>o,n:()=>n});i(43437);var r=i(75009),s=i(87156);const o={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,t){t&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var t=(0,s.vz)(e).path,i=0,r=t.indexOf(this);i<r;i++){var o=t[i];if(o.hasAttribute&&(o.hasAttribute("dialog-dismiss")||o.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(o.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},n=[r.$,o]},22626:(e,t,i)=>{"use strict";i(43437),i(65660);var r=i(51654),s=i(9672),o=i(50856);(0,s.k)({_template:o.d`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(r.Z)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},33243:(e,t,i)=>{"use strict";i.r(t);i(53918),i(22626),i(30879),i(31206);var r=i(15652),s=(i(34821),i(11654)),o=i(47181),n=i(86490);i(46583);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var s=t.placement;if(t.kind===r&&("static"===s||"prototype"===s)){var o="static"===s?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],s={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,s)}),this),e.forEach((function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,s);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],s=e.decorators,o=s.length-1;o>=0;o--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,s[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var s=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(s)||s);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var n=0;n<e.length-1;n++)for(var a=n+1;a<e.length;a++)if(e[n].key===e[a].key&&e[n].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var s=a();if(r)for(var o=0;o<r.length;o++)s=r[o](s);var n=t((function(e){s.initializeInstanceElements(e,h.elements)}),i),h=s.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var s,o=e[r];if("method"===o.kind&&(s=t.find(i)))if(p(o.descriptor)||p(s.descriptor)){if(d(o)||d(s))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");s.descriptor=o.descriptor}else{if(d(o)){if(d(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");s.decorators=o.decorators}c(o,s)}else t.push(o)}return t}(n.d.map(l)),e);s.initializeClassElements(n.F,h.elements),s.runClassFinishers(n.F,h.finishers)}([(0,r.Mo)("ha-dialog-import-blueprint")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_importing",value:()=>!1},{kind:"field",decorators:[(0,r.sz)()],key:"_saving",value:()=>!1},{kind:"field",decorators:[(0,r.sz)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_result",value:void 0},{kind:"field",decorators:[(0,r.IO)("#input")],key:"_input",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0}},{kind:"method",key:"closeDialog",value:function(){this._error=void 0,this._result=void 0,this._params=void 0,(0,o.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?r.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${this.hass.localize("ui.panel.config.blueprint.add.header")}
      >
        <div>
          ${this._error?r.dy` <div class="error">${this._error}</div> `:""}
          ${this._result?r.dy`${this.hass.localize("ui.panel.config.blueprint.add.import_header","name",r.dy`<b>${this._result.blueprint.metadata.name}</b>`,"domain",this._result.blueprint.metadata.domain)}
                <br />
                <p class="pre-line">
                  ${this._result.blueprint.metadata.description}
                </p>
                ${this._result.validation_errors?r.dy`
                      <p class="error">
                        ${this.hass.localize("ui.panel.config.blueprint.add.unsupported_blueprint")}
                      </p>
                      <ul class="error">
                        ${this._result.validation_errors.map((e=>r.dy`<li>${e}</li>`))}
                      </ul>
                    `:r.dy`
                      <paper-input
                        id="input"
                        .value=${this._result.suggested_filename}
                        .label=${this.hass.localize("ui.panel.config.blueprint.add.file_name")}
                      ></paper-input>
                    `}
                <ha-expansion-panel
                  .header=${this.hass.localize("ui.panel.config.blueprint.add.raw_blueprint")}
                >
                  <pre>${this._result.raw_data}</pre>
                </ha-expansion-panel>`:r.dy`${this.hass.localize("ui.panel.config.blueprint.add.import_introduction")}<paper-input
                  id="input"
                  .label=${this.hass.localize("ui.panel.config.blueprint.add.url")}
                  dialogInitialFocus
                ></paper-input>`}
        </div>
        ${this._result?r.dy`<mwc-button
                slot="secondaryAction"
                @click=${this.closeDialog}
                .disabled=${this._saving}
              >
                ${this.hass.localize("ui.common.cancel")}
              </mwc-button>
              <mwc-button
                slot="primaryAction"
                @click=${this._save}
                .disabled=${this._saving||this._result.validation_errors}
              >
                ${this._saving?r.dy`<ha-circular-progress
                      active
                      size="small"
                      .title=${this.hass.localize("ui.panel.config.blueprint.add.saving")}
                    ></ha-circular-progress>`:""}
                ${this.hass.localize("ui.panel.config.blueprint.add.save_btn")}
              </mwc-button>`:r.dy`<mwc-button
              slot="primaryAction"
              @click=${this._import}
              .disabled=${this._importing}
            >
              ${this._importing?r.dy`<ha-circular-progress
                    active
                    size="small"
                    .title=${this.hass.localize("ui.panel.config.blueprint.add.importing")}
                  ></ha-circular-progress>`:""}
              ${this.hass.localize("ui.panel.config.blueprint.add.import_btn")}
            </mwc-button>`}
      </ha-dialog>
    `:r.dy``}},{kind:"method",key:"_import",value:async function(){this._importing=!0,this._error=void 0;try{var e;const t=null===(e=this._input)||void 0===e?void 0:e.value;if(!t)return void(this._error=this.hass.localize("ui.panel.config.blueprint.add.error_no_url"));this._result=await(0,n.fQ)(this.hass,t)}catch(e){this._error=e.message}finally{this._importing=!1}}},{kind:"method",key:"_save",value:async function(){this._saving=!0;try{var e;const t=null===(e=this._input)||void 0===e?void 0:e.value;if(!t)return;await(0,n.Bp)(this.hass,this._result.blueprint.metadata.domain,t,this._result.raw_data,this._result.blueprint.metadata.source_url),this._params.importedCallback(),this.closeDialog()}catch(e){this._error=e.message}finally{this._saving=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[s.yu,r.iv`
        .pre-line {
          white-space: pre-line;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=chunk.692b80117b61b66d1125.js.map