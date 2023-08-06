(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6549],{32520:(e,t,r)=>{"use strict";r.r(t);var i=r(15652),n=r(66386),o=(r(15291),r(60010),r(31206),r(47181)),s=r(11654);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!d(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function m(e,t,r){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=a();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,u.elements)}),r),u=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(p(o.descriptor)||p(n.descriptor)){if(d(o)||d(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(d(o)){if(d(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(s.d.map(l)),e);n.initializeClassElements(s.F,u.elements),n.runClassFinishers(s.F,u.finishers)}([(0,i.Mo)("ha-config-aiszigbee")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,i.sz)()],key:"_access_token",value:()=>""},{kind:"method",key:"render",value:function(){const e=(0,n.GQ)();this._access_token=null==e?void 0:e.access_token;const t=this.hass.states["sensor.status_serwisu_zigbee2mqtt"];if("online"===t.state){const e=i.dy` <iframe
        src="/api/zigbee2mqtt/${this._access_token}/"
      ></iframe>`;return i.dy`<hass-subpage header="Zigbee2Mqtt" .narrow=${this.narrow}>
        ${e}
      </hass-subpage>`}return i.dy`<hass-subpage header="Zigbee2Mqtt" .narrow=${this.narrow}>
      <div
        style="width: 100%; height: 100%; display: flex; align-items: center;"
      >
        <div style="width: 100%;">
          <p style="text-align: center;">
            <span class="text"><b>BRAK POŁĄCZENIA Z ZIGBEE2MQTT</b></span>
            <span class="icon">
              <svg style="width:24px;height:24px" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M8 2C6.9 2 6 2.9 6 4V12H5V16L9 20V22H15V20L19 16V12H18V4C18 2.9 17.11 2 16 2M8 4H16V12H8M9 7V9H11V7M13 7V9H15V7Z"
                />
              </svg>
            </span>
            <br />
          </p>
          <svg
            style="width:84px;height:84px;display:block;margin:auto;"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M11.6 13V12.9L11.3 12.6H11.2L9.6 12C10 11.7 10.4 11.5 10.9 11.5C11.4 11.5 11.9 11.7 12.3 12.1C12.7 12.5 12.9 12.9 12.9 13.4C12.9 13.9 12.8 14.3 12.4 14.7L11.6 13M9.7 19.3C9.4 18.3 9.6 17.1 10.4 15.5L11.6 18.6C11.8 19.2 11.6 19.6 11 19.9C10.4 20.2 10 20 9.7 19.3M4.1 13.1C4.3 12.5 4.7 12.3 5.3 12.5L8.5 13.7C6.9 14.5 5.7 14.7 4.7 14.4C4.1 14.1 3.9 13.7 4.1 13.1M12 8.1H11V9.5H10.6C9.5 9.5 8.6 9.9 7.8 10.7L7.4 11.3L6 10.5C5.7 10.4 5.4 10.4 5 10.4C4.4 10.4 3.8 10.6 3.3 11S2.4 11.8 2.2 12.4C2 13.1 2 13.7 2.2 14.4C2.5 15.1 2.8 15.6 3.3 15.9C2.9 17.4 3.2 18.7 4.3 19.8C5.1 20.6 6 21 7.1 21C7.6 21 7.9 21 8.2 20.9C8.8 21.7 9.6 22.2 10.6 22.2C10.9 22.2 11.3 22.2 11.6 22.1C12.2 21.9 12.6 21.5 13 21C13.4 20.4 13.6 19.9 13.6 19.3C13.6 18.9 13.6 18.6 13.5 18.3L12.9 16.9L13.5 16.5C14.3 15.7 14.7 14.6 14.6 13.4H16V12.4H14.4C14 11.2 13.2 10.4 12 10V8.1M17.3 6.8C17.1 6.6 17 6.3 17 6.1C17 5.8 17.1 5.6 17.3 5.4C17.5 5.2 17.7 5.1 18 5.1S18.5 5.2 18.7 5.4C18.9 5.5 19 5.8 19 6.1C19 6.4 18.9 6.6 18.7 6.8C18.5 7 18.3 7 18 7S17.5 7 17.3 6.8M20.7 4.1H19.6L19.3 3.2C19.1 2.5 18.7 2.2 18 2.2C17.3 2.2 16.8 2.5 16.7 3.2L16.4 4.1H15.3C14.7 4.1 14.3 4.4 14 5C13.8 5.6 14 6.1 14.6 6.5L15.5 7L15.1 8.2C14.9 8.6 15 9 15.2 9.4C15.5 9.8 15.8 10 16.3 10C16.7 10 17 9.9 17.2 9.7L18 9.1L18.8 9.8C19 9.9 19.3 10 19.7 10C20.2 10 20.5 9.8 20.8 9.4C21 9 21.1 8.6 20.9 8.2L20.5 7L21.3 6.5C21.9 6.1 22.1 5.6 21.9 5C21.7 4.3 21.3 4.1 20.7 4.1Z"
            />
          </svg>
          <p style="text-align: center;">
            <span class="text"
              ><b
                >usługa zigbee2mqtt jest
                <span
                  .onclick="${this.showZigbeeStatus}"
                  style="text-decoration: underline; cursor: pointer;"
                >
                  <a> ${t.state} </a> </span
                >, czekam na połączenie, to może potrwać kilka minut...</b
              ></span
            >
            <br /><br />
            <ha-circular-progress active></ha-circular-progress>
            <br />
            <br />
            W razie problemów sprawdz logi, wpisując w
            <a href="/developer-tools/console">konsoli</a> komendę:
            <b>pm2 logs</b><br />
            Szczegóły w dokumentacji:
            <a href="https://www.ai-speaker.com/docs/ais_app_integration_zigbee"
              >Integracja Zigbee2MQTT</a
            >
          </p>
        </div>
      </div>
    </hass-subpage>`}},{kind:"method",key:"updated",value:function(e){m(y(r.prototype),"updated",this).call(this,e)}},{kind:"method",key:"showZigbeeStatus",value:function(){(0,o.B)(this,"hass-more-info",{entityId:"sensor.status_serwisu_zigbee2mqtt"})}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,i.iv`
        iframe {
          display: block;
          width: 100%;
          height: 100%;
          border: 0;
        }
        .header + iframe {
          height: calc(100% - 40px);
        }
        .header {
          display: flex;
          align-items: center;
          font-size: 16px;
          height: 40px;
          padding: 0 16px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
          --mdc-icon-size: 20px;
        }

        .main-title {
          margin: 0 0 0 24px;
          line-height: 20px;
          flex-grow: 1;
        }

        mwc-icon-button {
          pointer-events: auto;
        }

        hass-subpage {
          --app-header-background-color: var(--sidebar-background-color);
          --app-header-text-color: var(--sidebar-text-color);
          --app-header-border-bottom: 1px solid var(--divider-color);
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.25b0dca50da9e22b52a8.js.map