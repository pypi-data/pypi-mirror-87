(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7852],{25721:(e,t,r)=>{"use strict";r.r(t);r(53918),r(30879),r(53973),r(89194),r(16509);var i=r(15652),o=r(76307),a=r(47181);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var a="static"===o?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!d(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,a=o.length-1;a>=0;a--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[a])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var s=0;s<e.length-1;s++)for(var n=s+1;n<e.length;n++)if(e[s].key===e[n].key&&e[s].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function n(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function f(e,t,r){return(f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var o=s();if(i)for(var a=0;a<i.length;a++)o=i[a](o);var p=t((function(e){o.initializeInstanceElements(e,u.elements)}),r),u=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var o,a=e[i];if("method"===a.kind&&(o=t.find(r)))if(c(a.descriptor)||c(o.descriptor)){if(d(a)||d(o))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");o.descriptor=a.descriptor}else{if(d(a)){if(d(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");o.decorators=a.decorators}l(a,o)}else t.push(a)}return t}(p.d.map(n)),e);o.initializeClassElements(p.F,u.elements),o.runClassFinishers(p.F,u.finishers)}([(0,i.Mo)("onboarding-restore-backup")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)()],key:"localize",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"_username",value:()=>""},{kind:"field",decorators:[(0,i.Cb)()],key:"_password",value:()=>""},{kind:"field",decorators:[(0,i.Cb)()],key:"_backup_password",value:()=>""},{kind:"field",decorators:[(0,i.Cb)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)()],key:"_errorMsg",value(){}},{kind:"field",decorators:[(0,i.Cb)()],key:"_aisGates",value:()=>[]},{kind:"field",decorators:[(0,i.Cb)()],key:"_aisLogged",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)()],key:"_infoMsg",value(){}},{kind:"method",key:"render",value:function(){return i.dy`
    <br>
      <p>
          <b>${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_restore_intro")}</b>
      </p>
    ${this._aisLogged?"":i.dy`
            <p>
              ${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_restore_intro_step1")}
            </p>
            <onboarding-ais-wifi
              .hass=${this.hass}
              .localize=${this.localize}
            ></onboarding-ais-wifi>
          `}

    ${this._infoMsg?i.dy`
            <p class="info">
              ${this._infoMsg}
            </p>
          `:""}

    ${this._errorMsg?i.dy`
            <p class="error">
              ${this.localize("ui.panel.page-onboarding.user.error."+this._errorMsg)||this._errorMsg}
            </p>
          `:""}

    <form>
    ${this._aisLogged?i.dy` <span>
              ${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_restore_intro_step2")}
            </span>
            <paper-input
              name="backup_password"
              label="${this.localize("ui.panel.page-onboarding.user.data.password")}"
              value=${this._backup_password}
              @value-changed=${this._handleValueChanged}
              .disabled=${this._loading}
              type="password"
            ></paper-input>
            <p>
              ${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_restore_intro_step3")}
            </p>`:""}

    ${this._aisLogged?this._aisGates.map((e=>i.dy`
              <paper-item class="option">
                <paper-item-body four-line>
                  <div>${e.gate_id}</div>
                  <div secondary>
                    ${e.gate_name} &nbsp; ${e.gate_desc}
                  </div>
                  <div secondary>
                    <ha-icon icon="mdi:home-assistant"></ha-icon>&nbsp;
                    ${e.gate_backup_ha}
                  </div>
                  <div secondary>
                    <ha-icon icon="mdi:zigbee"></ha-icon>&nbsp;
                    ${e.gate_backup_zigbee}
                  </div>
                </paper-item-body>
                <mwc-button
                  .slug=${e.gate_id}
                  title="Restore"
                  @click=${this._restoreFromAis}
                  .disabled=${this._loading}
                  data-gate_id=${e.gate_id}
                  data-backup_password=${this._backup_password}
                >
                  ${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_restore_button")}
                </mwc-button>
              </paper-item>
            `)):i.dy` <paper-input
              name="username"
              label="${this.localize("ui.panel.page-onboarding.user.data.username")}"
              value=${this._username}
              @value-changed=${this._handleValueChanged}
              required
              auto-validate
              autocapitalize="none"
              .errorMessage="${this.localize("ui.panel.page-onboarding.user.required_field")}"
            ></paper-input>

            <paper-input
              name="password"
              label="${this.localize("ui.panel.page-onboarding.user.data.password")}"
              value=${this._password}
              @value-changed=${this._handleValueChanged}
              required
              type="password"
              auto-validate
              .errorMessage="${this.localize("ui.panel.page-onboarding.user.required_field")}"
            ></paper-input>`}

      ${this._aisLogged?i.dy` <p class="action">
              <mwc-button
                raised
                @click=${this._logoutFromAis}
                .disabled=${this._loading}
              >
                ${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_logout")}
              </mwc-button>
            </p>`:i.dy` <p class="action">
              <mwc-button
                raised
                @click=${this._submitForm}
                .disabled=${this._loading}
              >
                ${this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_login")}
              </mwc-button>
            </p>`}
    </div>
  </form>
  <div class="footer">
        <mwc-button @click=${this._finish}>
          ${this.localize("ui.panel.page-onboarding.ais-restore-backup.finish")}
        </mwc-button>
  </div>
`}},{kind:"method",key:"_finish",value:async function(e){e.preventDefault();try{const e=await(0,o.ZO)(this.hass);(0,a.B)(this,"onboarding-step",{type:"ais_restore_backup",result:e})}catch(t){alert("Failed to save: "+t.message)}}},{kind:"method",key:"firstUpdated",value:function(e){f(g(r.prototype),"firstUpdated",this).call(this,e),setTimeout((()=>this.shadowRoot.querySelector("paper-input").focus()),100),this.addEventListener("keypress",(e=>{13===e.keyCode&&this._submitForm(e)}))}},{kind:"method",key:"_handleValueChanged",value:function(e){this["_"+e.target.name]=e.detail.value}},{kind:"method",key:"_logoutFromAis",value:async function(e){e.preventDefault(),this._aisLogged=!1,this._aisGates=[],this._username="",this._password=""}},{kind:"method",key:"_restoreFromAis",value:async function(e){e.preventDefault();const t=e.target.dataset.gate_id,r=e.target.dataset.backup_password;this._loading=!0,this._infoMsg=this.localize("ui.panel.page-onboarding.ais-restore-backup.ais_restore_ok_info_step1")+" "+t;try{const e=await(0,o.gi)({gate_id:t,backup_password:r});"invalid"===e.result?(this._errorMsg=e.message,this._infoMsg="",this._loading=!1):(this._errorMsg="",this._infoMsg=e.message,this._loading=!1)}catch(i){this._infoMsg="",this._loading=!1,this._errorMsg=i.body.message}}},{kind:"method",key:"_submitForm",value:async function(e){if(e.preventDefault(),this._username&&this._password){this._loading=!0,this._errorMsg="";try{const e=await(0,o.lZ)({username:this._username,password:this._password,language:this.language});"invalid"===e.result?(this._errorMsg=e.error,this._loading=!1,this._aisLogged=!1):(this._aisLogged=!0,this._aisGates=e.gates,this._loading=!1)}catch(t){console.error(t),this._loading=!1,this._errorMsg=t.body.message}}else this._errorMsg="required_fields"}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      .error {
        color: red;
      }
      .info {
        color: green;
      }
      .action {
        margin: 32px 0;
        text-align: center;
      }
      button {
        cursor: pointer;
        padding: 0;
        border: 0;
        background: 0;
        font: inherit;
      }
      .footer {
        margin-top: 2em;
        text-align: right;
      }
      .column {
        flex: 50%;
        padding: 5px;
      }
      .row {
        display: flex;
      }
    `}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.45da4d1258fbfe4bbf38.js.map