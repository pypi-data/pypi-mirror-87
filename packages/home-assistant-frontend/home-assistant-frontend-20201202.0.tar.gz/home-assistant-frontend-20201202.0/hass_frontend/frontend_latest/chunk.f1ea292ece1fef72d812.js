/*! For license information please see chunk.f1ea292ece1fef72d812.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3262],{28417:(e,t,a)=>{"use strict";a(50808);var s=a(33367),o=a(93592),l=a(87156);const i={getTabbableNodes:function(e){const t=[];return this._collectTabbableNodes(e,t)?o.H._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!o.H._isVisible(e))return!1;const a=e,s=o.H._normalizedTabIndex(a);let i,p=s>0;s>=0&&t.push(a),i="content"===a.localName||"slot"===a.localName?(0,l.vz)(a).getDistributedNodes():(0,l.vz)(a.shadowRoot||a.root||a).children;for(let e=0;e<i.length;e++)p=this._collectTabbableNodes(i[e],t)||p;return p}},p=customElements.get("paper-dialog"),r={get _focusableNodes(){return i.getTabbableNodes(this)}};class n extends((0,s.P)([r],p)){}customElements.define("ha-paper-dialog",n)},3262:(e,t,a)=>{"use strict";a.r(t);a(53918),a(22626),a(31206);var s=a(50856),o=a(28426),l=(a(28417),a(68331),a(4940),a(11052)),i=a(1265);a(36436);let p=0;class r extends((0,i.Z)((0,l.I)(o.H3))){static get template(){return s.d`
      <style include="ha-style-dialog">
        .error {
          color: red;
        }
        ha-paper-dialog {
          max-width: 500px;
        }
        h2 {
          white-space: normal;
        }
        ha-markdown {
          --markdown-svg-background-color: white;
          --markdown-svg-color: black;
          display: block;
          margin: 0 auto;
        }
        ha-markdown a {
          color: var(--primary-color);
        }
        .init-spinner {
          padding: 10px 100px 34px;
          text-align: center;
        }
        .submit-spinner {
          margin-right: 16px;
        }
      </style>
      <ha-paper-dialog
        id="dialog"
        with-backdrop=""
        opened="{{_opened}}"
        on-opened-changed="_openedChanged"
      >
        <h2>
          <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
            [[localize('ui.panel.profile.mfa_setup.title_aborted')]]
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
            [[localize('ui.panel.profile.mfa_setup.title_success')]]
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
            [[_computeStepTitle(localize, _step)]]
          </template>
        </h2>
        <paper-dialog-scrollable>
          <template is="dom-if" if="[[_errorMsg]]">
            <div class="error">[[_errorMsg]]</div>
          </template>
          <template is="dom-if" if="[[!_step]]">
            <div class="init-spinner">
              <ha-circular-progress active></ha-circular-progress>
            </div>
          </template>
          <template is="dom-if" if="[[_step]]">
            <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
              <ha-markdown
                allowsvg
                breaks
                content="[[_computeStepAbortedReason(localize, _step)]]"
              ></ha-markdown>
            </template>

            <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
              <p>
                [[localize('ui.panel.profile.mfa_setup.step_done', 'step',
                _step.title)]]
              </p>
            </template>

            <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
              <template
                is="dom-if"
                if="[[_computeStepDescription(localize, _step)]]"
              >
                <ha-markdown
                  allowsvg
                  breaks
                  content="[[_computeStepDescription(localize, _step)]]"
                ></ha-markdown>
              </template>

              <ha-form
                data="{{_stepData}}"
                schema="[[_step.data_schema]]"
                error="[[_step.errors]]"
                compute-label="[[_computeLabelCallback(localize, _step)]]"
                compute-error="[[_computeErrorCallback(localize, _step)]]"
              ></ha-form>
            </template>
          </template>
        </paper-dialog-scrollable>
        <div class="buttons">
          <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
            <mwc-button on-click="_flowDone"
              >[[localize('ui.panel.profile.mfa_setup.close')]]</mwc-button
            >
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
            <mwc-button on-click="_flowDone"
              >[[localize('ui.panel.profile.mfa_setup.close')]]</mwc-button
            >
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
            <template is="dom-if" if="[[_loading]]">
              <div class="submit-spinner">
                <ha-circular-progress active></ha-circular-progress>
              </div>
            </template>
            <template is="dom-if" if="[[!_loading]]">
              <mwc-button on-click="_submitStep"
                >[[localize('ui.panel.profile.mfa_setup.submit')]]</mwc-button
              >
            </template>
          </template>
        </div>
      </ha-paper-dialog>
    `}static get properties(){return{_hass:Object,_dialogClosedCallback:Function,_instance:Number,_loading:{type:Boolean,value:!1},_errorMsg:String,_opened:{type:Boolean,value:!1},_step:{type:Object,value:null},_stepData:Object}}ready(){super.ready(),this.hass.loadBackendTranslation("mfa_setup","auth"),this.addEventListener("keypress",(e=>{13===e.keyCode&&this._submitStep()}))}showDialog({hass:e,continueFlowId:t,mfaModuleId:a,dialogClosedCallback:s}){this.hass=e,this._instance=p++,this._dialogClosedCallback=s,this._createdFromHandler=!!a,this._loading=!0,this._opened=!0;const o=t?this.hass.callWS({type:"auth/setup_mfa",flow_id:t}):this.hass.callWS({type:"auth/setup_mfa",mfa_module_id:a}),l=this._instance;o.then((e=>{l===this._instance&&(this._processStep(e),this._loading=!1,setTimeout((()=>this.$.dialog.center()),0))}))}_submitStep(){this._loading=!0,this._errorMsg=null;const e=this._instance;this.hass.callWS({type:"auth/setup_mfa",flow_id:this._step.flow_id,user_input:this._stepData}).then((t=>{e===this._instance&&(this._processStep(t),this._loading=!1)}),(e=>{this._errorMsg=e&&e.body&&e.body.message||"Unknown error occurred",this._loading=!1}))}_processStep(e){e.errors||(e.errors={}),this._step=e,0===Object.keys(e.errors).length&&(this._stepData={})}_flowDone(){this._opened=!1;const e=this._step&&["create_entry","abort"].includes(this._step.type);this._step&&!e&&this._createdFromHandler,this._dialogClosedCallback({flowFinished:e}),this._errorMsg=null,this._step=null,this._stepData={},this._dialogClosedCallback=null}_equals(e,t){return e===t}_openedChanged(e){this._step&&!e.detail.value&&this._flowDone()}_computeStepAbortedReason(e,t){return e(`component.auth.mfa_setup.${t.handler}.abort.${t.reason}`)}_computeStepTitle(e,t){return e(`component.auth.mfa_setup.${t.handler}.step.${t.step_id}.title`)||"Setup Multi-factor Authentication"}_computeStepDescription(e,t){const a=[`component.auth.mfa_setup.${t.handler}.step.${t.step_id}.description`],s=t.description_placeholders||{};return Object.keys(s).forEach((e=>{a.push(e),a.push(s[e])})),e(...a)}_computeLabelCallback(e,t){return a=>e(`component.auth.mfa_setup.${t.handler}.step.${t.step_id}.data.${a.name}`)||a.name}_computeErrorCallback(e,t){return a=>e(`component.auth.mfa_setup.${t.handler}.error.${a}`)||a}}customElements.define("ha-mfa-module-setup-flow",r)},36436:(e,t,a)=>{"use strict";a(21384);var s=a(11654);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML=`<dom-module id="ha-style-dialog">\n<template>\n  <style>\n    ${s.yu.cssText}\n  </style>\n</template>\n</dom-module>`,document.head.appendChild(o.content)}}]);
//# sourceMappingURL=chunk.f1ea292ece1fef72d812.js.map