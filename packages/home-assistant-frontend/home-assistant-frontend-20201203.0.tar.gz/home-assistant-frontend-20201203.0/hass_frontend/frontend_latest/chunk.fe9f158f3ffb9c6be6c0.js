/*! For license information please see chunk.fe9f158f3ffb9c6be6c0.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6810],{7323:(e,t,r)=>{"use strict";r.d(t,{p:()=>i});const i=(e,t)=>e&&-1!==e.config.components.indexOf(t)},49706:(e,t,r)=>{"use strict";r.d(t,{Rb:()=>i,Zy:()=>n,h2:()=>o,PS:()=>s,l:()=>a,ht:()=>l,f0:()=>c,tj:()=>d,uo:()=>h,lC:()=>u,Kk:()=>p,ot:()=>f,gD:()=>m,a1:()=>b,AZ:()=>y});const i="hass:bookmark",n={alert:"hass:alert",alexa:"hass:amazon-alexa",air_quality:"hass:air-filter",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:cog",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:form-textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer-outline",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",zone:"hass:map-marker-radius"},o={current:"hass:current-ac",energy:"hass:flash",humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",power_factor:"hass:angle-acute",signal_strength:"hass:wifi",timestamp:"hass:clock",voltage:"hass:sine-wave"},s=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","scene","script","timer","vacuum","water_heater"],a=["alarm_control_panel","automation","camera","climate","configurator","counter","cover","fan","group","humidifier","input_datetime","light","lock","media_player","person","script","sun","timer","vacuum","water_heater","weather"],l=["input_number","input_select","input_text","scene"],c=["camera","configurator","scene"],d=["closed","locked","off"],h="on",u="off",p=new Set(["fan","input_boolean","light","switch","group","automation","humidifier"]),f="°C",m="°F",b="group.default_view",y=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"]},9893:(e,t,r)=>{"use strict";r.d(t,{Qo:()=>i,kb:()=>o,cs:()=>s});const i="custom:",n=window;"customCards"in n||(n.customCards=[]);const o=n.customCards,s=e=>o.find((t=>t.type===e))},51444:(e,t,r)=>{"use strict";r.d(t,{_:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(5009),r.e(9462),r.e(2420)]).then(r.bind(r,72420)),o=e=>{(0,i.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:n,dialogParams:{}})}},27849:(e,t,r)=>{"use strict";r(39841);var i=r(50856);r(28426);class n extends(customElements.get("app-header-layout")){static get template(){return i.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",n)},51153:(e,t,r)=>{"use strict";r.d(t,{l$:()=>s,Z6:()=>a,Do:()=>l});r(10175),r(80251),r(99471),r(14888),r(69377),r(95035),r(38026),r(89173),r(41043),r(57464),r(24617),r(26136),r(82778);var i=r(7778);const n=new Set(["entity","entities","button","entity-button","glance","history-graph","horizontal-stack","light","sensor","thermostat","vertical-stack","weather-forecast"]),o={"alarm-panel":()=>r.e(5743).then(r.bind(r,81878)),error:()=>Promise.all([r.e(9033),r.e(947),r.e(8394)]).then(r.bind(r,55796)),"empty-state":()=>r.e(7284).then(r.bind(r,67284)),grid:()=>r.e(6169).then(r.bind(r,6169)),starting:()=>r.e(7873).then(r.bind(r,47873)),"entity-filter":()=>r.e(3688).then(r.bind(r,33688)),humidifier:()=>r.e(8558).then(r.bind(r,68558)),"media-control":()=>Promise.all([r.e(1935),r.e(3525)]).then(r.bind(r,13525)),"picture-elements":()=>Promise.all([r.e(4909),r.e(319),r.e(7282),r.e(9810),r.e(5475),r.e(1267)]).then(r.bind(r,83358)),"picture-entity":()=>Promise.all([r.e(319),r.e(7282),r.e(8317)]).then(r.bind(r,41500)),"picture-glance":()=>Promise.all([r.e(319),r.e(7282),r.e(7987)]).then(r.bind(r,66621)),"plant-status":()=>r.e(8723).then(r.bind(r,48723)),"safe-mode":()=>r.e(6983).then(r.bind(r,24503)),"shopping-list":()=>Promise.all([r.e(7440),r.e(3376)]).then(r.bind(r,43376)),conditional:()=>r.e(8857).then(r.bind(r,68857)),gauge:()=>r.e(5223).then(r.bind(r,25223)),iframe:()=>r.e(5018).then(r.bind(r,95018)),map:()=>r.e(76).then(r.bind(r,60076)),markdown:()=>Promise.all([r.e(4940),r.e(6474)]).then(r.bind(r,51282)),picture:()=>r.e(5338).then(r.bind(r,45338)),calendar:()=>Promise.resolve().then(r.bind(r,80251)),logbook:()=>Promise.all([r.e(9160),r.e(6576),r.e(851)]).then(r.bind(r,8436))},s=e=>(0,i.Xm)("card",e,n,o,void 0,void 0),a=e=>(0,i.Tw)("card",e,n,o,void 0,void 0),l=e=>(0,i.ED)(e,"card",n,o)},7778:(e,t,r)=>{"use strict";r.d(t,{N2:()=>o,Tw:()=>c,Xm:()=>d,ED:()=>h});var i=r(47181),n=r(9893);const o=(e,t)=>({type:"error",error:e,origConfig:t}),s=(e,t)=>{const r=document.createElement(e);return r.setConfig(t),r},a=(e,t)=>(e=>{const t=document.createElement("hui-error-card");return customElements.get("hui-error-card")?t.setConfig(e):(Promise.all([r.e(9033),r.e(947),r.e(8394)]).then(r.bind(r,55796)),customElements.whenDefined("hui-error-card").then((()=>{customElements.upgrade(t),t.setConfig(e)}))),t})(o(e,t)),l=e=>e.startsWith(n.Qo)?e.substr(n.Qo.length):void 0,c=(e,t,r,i,n,o)=>{try{return d(e,t,r,i,n,o)}catch(r){return console.error(e,t.type,r),a(r.message,t)}},d=(e,t,r,n,o,c)=>{if(!t||"object"!=typeof t)throw new Error("Config is not an object");if(!(t.type||c||o&&"entity"in t))throw new Error("No card type configured");const d=t.type?l(t.type):void 0;if(d)return((e,t)=>{if(customElements.get(e))return s(e,t);const r=a(`Custom element doesn't exist: ${e}.`,t);if(!e.includes("-"))return r;r.style.display="None";const n=window.setTimeout((()=>{r.style.display=""}),2e3);return customElements.whenDefined(e).then((()=>{clearTimeout(n),(0,i.B)(r,"ll-rebuild")})),r})(d,t);let h;if(o&&!t.type&&t.entity){h=(o[t.entity.split(".",1)[0]]||o._domain_not_found)+"-entity"}else h=t.type||c;if(void 0===h)throw new Error("No type specified");const u=`hui-${h}-${e}`;if(n&&h in n)return n[h](),((e,t)=>{if(customElements.get(e))return s(e,t);const r=document.createElement(e);return customElements.whenDefined(e).then((()=>{try{customElements.upgrade(r),r.setConfig(t)}catch(e){(0,i.B)(r,"ll-rebuild")}})),r})(u,t);if(r&&r.has(h))return s(u,t);throw new Error("Unknown type encountered: "+h)},h=async(e,t,r,i)=>{const n=l(e);if(n){const e=customElements.get(n);if(e)return e;if(!n.includes("-"))throw new Error("Custom element not found: "+n);return new Promise(((e,t)=>{setTimeout((()=>t(new Error("Custom element not found: "+n))),2e3),customElements.whenDefined(n).then((()=>e(customElements.get(n))))}))}const o=`hui-${e}-${t}`,s=customElements.get(o);if(r&&r.has(e))return s;if(i&&e in i)return s||i[e]().then((()=>customElements.get(o)));throw new Error("Unknown type: "+e)}},89026:(e,t,r)=>{"use strict";r.d(t,{t:()=>o,Q:()=>s});var i=r(7778);const n={picture:()=>r.e(9130).then(r.bind(r,69130)),buttons:()=>r.e(2587).then(r.bind(r,32587)),graph:()=>r.e(5773).then(r.bind(r,25773))},o=e=>(0,i.Tw)("header-footer",e,void 0,n,void 0,void 0),s=e=>(0,i.ED)(e,"header-footer",void 0,n)},37482:(e,t,r)=>{"use strict";r.d(t,{m:()=>a,T:()=>l});r(12141),r(31479),r(23266),r(65716),r(97600),r(83896),r(45340),r(56427),r(23658);var i=r(7778);const n=new Set(["media-player-entity","scene-entity","script-entity","sensor-entity","text-entity","toggle-entity","button","call-service"]),o={"climate-entity":()=>r.e(5642).then(r.bind(r,35642)),"cover-entity":()=>Promise.all([r.e(9448),r.e(6755)]).then(r.bind(r,16755)),"group-entity":()=>r.e(1534).then(r.bind(r,81534)),"humidifier-entity":()=>r.e(1102).then(r.bind(r,41102)),"input-datetime-entity":()=>Promise.all([r.e(5009),r.e(2955),r.e(8161),r.e(9543),r.e(7078),r.e(8559)]).then(r.bind(r,22350)),"input-number-entity":()=>r.e(2335).then(r.bind(r,12335)),"input-select-entity":()=>Promise.all([r.e(5009),r.e(2955),r.e(8161),r.e(1644),r.e(5675)]).then(r.bind(r,25675)),"input-text-entity":()=>r.e(3943).then(r.bind(r,73943)),"lock-entity":()=>r.e(1596).then(r.bind(r,61596)),"timer-entity":()=>r.e(1203).then(r.bind(r,31203)),conditional:()=>r.e(7749).then(r.bind(r,97749)),"weather-entity":()=>r.e(1850).then(r.bind(r,71850)),divider:()=>r.e(1930).then(r.bind(r,41930)),section:()=>r.e(4832).then(r.bind(r,94832)),weblink:()=>r.e(4689).then(r.bind(r,44689)),cast:()=>r.e(5840).then(r.bind(r,25840)),buttons:()=>r.e(2137).then(r.bind(r,82137)),attribute:()=>Promise.resolve().then(r.bind(r,45340)),text:()=>r.e(3459).then(r.bind(r,63459))},s={_domain_not_found:"text",alert:"toggle",automation:"toggle",climate:"climate",cover:"cover",fan:"toggle",group:"group",humidifier:"humidifier",input_boolean:"toggle",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",remote:"toggle",scene:"scene",script:"script",sensor:"sensor",timer:"timer",switch:"toggle",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime",weather:"weather"},a=e=>(0,i.Tw)("row",e,n,o,s,void 0),l=e=>(0,i.ED)(e,"row",n,o)},44295:(e,t,r)=>{"use strict";r.r(t);r(53268),r(12730);var i=r(15652),n=r(14516),o=r(55317),s=r(11654),a=r(51153),l=r(7323),c=r(51444);r(48932),r(27849);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=b(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function h(e){var t,r=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function g(e,t,r){return(g="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function v(e){return(v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=d();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(f(o.descriptor)||f(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}u(o,n)}else t.push(o)}return t}(s.d.map(h)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-panel-shopping-list")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_card",value:void 0},{kind:"field",key:"_conversation",value(){return(0,n.Z)((e=>(0,l.p)(this.hass,"conversation")))}},{kind:"method",key:"firstUpdated",value:function(e){g(v(r.prototype),"firstUpdated",this).call(this,e),this._card=(0,a.Z6)({type:"shopping-list"}),this._card.hass=this.hass}},{kind:"method",key:"updated",value:function(e){g(v(r.prototype),"updated",this).call(this,e),e.has("hass")&&(this._card.hass=this.hass)}},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>${this.hass.localize("panel.shopping_list")}</div>
            ${this._conversation(this.hass.config.components)?i.dy`
                  <mwc-icon-button
                    .label=${this.hass.localize("ui.panel.shopping_list.start_conversation")}
                    @click=${this._showVoiceCommandDialog}
                  >
                    <ha-svg-icon .path=${o.N3O}></ha-svg-icon>
                  </mwc-icon-button>
                `:""}
          </app-toolbar>
        </app-header>
        <div id="columns">
          <div class="column">
            ${this._card}
          </div>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,c._)(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,i.iv`
        :host {
          --mdc-theme-primary: var(--app-header-text-color);
          display: block;
          height: 100%;
        }
        :host([narrow]) app-toolbar mwc-button {
          width: 65px;
        }
        .heading {
          overflow: hidden;
          white-space: nowrap;
          margin-top: 4px;
        }
        #columns {
          display: flex;
          flex-direction: row;
          justify-content: center;
          margin-left: 4px;
          margin-right: 4px;
        }
        .column {
          flex: 1 0 0;
          max-width: 500px;
          min-width: 0;
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.fe9f158f3ffb9c6be6c0.js.map