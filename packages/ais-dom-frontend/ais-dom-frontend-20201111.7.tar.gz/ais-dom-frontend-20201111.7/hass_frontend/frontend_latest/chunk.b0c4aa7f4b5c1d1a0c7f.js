(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2979],{54531:(e,t,i)=>{"use strict";i.d(t,{zJ:()=>o,Xr:()=>l,Qc:()=>c});const r=["zone","persistent_notification"],n=(e,t)=>{if("call-service"!==t.action||!t.service_data||!t.service_data.entity_id)return;let i=t.service_data.entity_id;Array.isArray(i)||(i=[i]);for(const r of i)e.add(r)},s=(e,t)=>{"string"!=typeof t?(t.entity&&e.add(t.entity),t.camera_image&&e.add(t.camera_image),t.tap_action&&n(e,t.tap_action),t.hold_action&&n(e,t.hold_action)):e.add(t)},a=(e,t)=>{t.entity&&s(e,t.entity),t.entities&&Array.isArray(t.entities)&&t.entities.forEach((t=>s(e,t))),t.card&&a(e,t.card),t.cards&&Array.isArray(t.cards)&&t.cards.forEach((t=>a(e,t))),t.elements&&Array.isArray(t.elements)&&t.elements.forEach((t=>a(e,t))),t.badges&&Array.isArray(t.badges)&&t.badges.forEach((t=>s(e,t)))},o=e=>{const t=new Set;return e.views.forEach((e=>a(t,e))),t},l=(e,t)=>{const i=new Set;for(const n of Object.keys(e.states))t.has(n)||r.includes(n.split(".",1)[0])||i.add(n);return i},c=(e,t)=>{const i=o(t);return l(e,i)}},32979:(e,t,i)=>{"use strict";i(16619),i(98553);var r=i(81480),n=i(15652),s=i(81471),a=i(79865),o=i(41181),l=i(14516),c=i(47181),d=(i(7164),i(31206),i(56007)),h=i(9893),p=i(54531),u=i(51153);const f=[{type:"alarm-panel",showElement:!0},{type:"button",showElement:!0},{type:"calendar",showElement:!0},{type:"entities",showElement:!0},{type:"entity",showElement:!0},{type:"gauge",showElement:!0},{type:"glance",showElement:!0},{type:"history-graph",showElement:!0},{type:"humidifier",showElement:!0},{type:"light",showElement:!0},{type:"map",showElement:!0},{type:"markdown",showElement:!0},{type:"media-control",showElement:!0},{type:"picture",showElement:!0},{type:"picture-elements",showElement:!0},{type:"picture-entity",showElement:!0},{type:"picture-glance",showElement:!0},{type:"plant-status",showElement:!0},{type:"sensor",showElement:!0},{type:"thermostat",showElement:!0},{type:"weather-forecast",showElement:!0},{type:"conditional"},{type:"entity-filter"},{type:"grid"},{type:"horizontal-stack"},{type:"iframe"},{type:"logbook"},{type:"vertical-stack"},{type:"shopping-list"}];function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!g(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=E(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function y(e){var t,i=E(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function E(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=m();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var a=t((function(e){n.initializeInstanceElements(e,o.elements)}),i),o=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(k(s.descriptor)||k(n.descriptor)){if(g(s)||g(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(g(s)){if(g(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}v(s,n)}else t.push(s)}return t}(a.d.map(y)),e);n.initializeClassElements(a.F,o.elements),n.runClassFinishers(a.F,o.finishers)}([(0,n.Mo)("hui-card-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_cards",value:()=>[]},{kind:"field",key:"lovelace",value:void 0},{kind:"field",key:"cardPicked",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_filter",value:()=>""},{kind:"field",decorators:[(0,n.sz)()],key:"_width",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_height",value:void 0},{kind:"field",key:"_unusedEntities",value:void 0},{kind:"field",key:"_usedEntities",value:void 0},{kind:"field",key:"_filterCards",value:()=>(0,l.Z)(((e,t)=>{if(!t)return e;let i=e.map((e=>e.card));const n=new r.Z(i,{keys:["type","name","description"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2});return i=n.search(t).map((e=>e.item)),e.filter((e=>i.includes(e.card)))}))},{kind:"method",key:"render",value:function(){return this.hass&&this.lovelace&&this._unusedEntities&&this._usedEntities?n.dy`
      <search-input
        .filter=${this._filter}
        no-label-float
        @value-changed=${this._handleSearchChange}
        .label=${this.hass.localize("ui.panel.lovelace.editor.edit_card.search_cards")}
      ></search-input>
      <div
        id="content"
        style=${(0,a.V)({width:this._width?this._width+"px":"auto",height:this._height?this._height+"px":"auto"})}
      >
        <div class="cards-container">
          ${this._filterCards(this._cards,this._filter).map((e=>e.element))}
        </div>
        <div class="cards-container">
          <div
            class="card manual"
            @click=${this._cardPicked}
            .config=${{type:""}}
          >
            <div class="card-header">
              ${this.hass.localize("ui.panel.lovelace.editor.card.generic.manual")}
            </div>
            <div class="preview description">
              ${this.hass.localize("ui.panel.lovelace.editor.card.generic.manual_description")}
            </div>
          </div>
        </div>
      </div>
    `:n.dy``}},{kind:"method",key:"shouldUpdate",value:function(e){const t=e.get("hass");return!t||t.language!==this.hass.language}},{kind:"method",key:"firstUpdated",value:function(){if(!this.hass||!this.lovelace)return;const e=(0,p.zJ)(this.lovelace),t=(0,p.Xr)(this.hass,e);this._usedEntities=[...e].filter((e=>this.hass.states[e]&&!d.V_.includes(this.hass.states[e].state))),this._unusedEntities=[...t].filter((e=>this.hass.states[e]&&!d.V_.includes(this.hass.states[e].state))),this._loadCards()}},{kind:"method",key:"_loadCards",value:function(){let e=f.map((e=>({name:this.hass.localize(`ui.panel.lovelace.editor.card.${e.type}.name`),description:this.hass.localize(`ui.panel.lovelace.editor.card.${e.type}.description`),...e})));h.kb.length>0&&(e=e.concat(h.kb.map((e=>({type:e.type,name:e.name,description:e.description,showElement:e.preview,isCustom:!0}))))),this._cards=e.map((e=>({card:e,element:n.dy`${(0,o.C)(this._renderCardElement(e),n.dy`
          <div class="card spinner">
            <ha-circular-progress active alt="Loading"></ha-circular-progress>
          </div>
        `)}`})))}},{kind:"method",key:"_handleSearchChange",value:function(e){const t=e.detail.value;if(t){if(!this._width||!this._height){const e=this.shadowRoot.getElementById("content");if(e&&!this._width){const t=e.clientWidth;t&&(this._width=t)}if(e&&!this._height){const t=e.clientHeight;t&&(this._height=t)}}}else this._width=void 0,this._height=void 0;this._filter=t}},{kind:"method",key:"_cardPicked",value:function(e){const t=e.currentTarget.config;(0,c.B)(this,"config-changed",{config:t})}},{kind:"method",key:"_tryCreateCardElement",value:function(e){const t=(0,u.l$)(e);return t.hass=this.hass,t.addEventListener("ll-rebuild",(i=>{i.stopPropagation(),this._rebuildCard(t,e)}),{once:!0}),t}},{kind:"method",key:"_rebuildCard",value:function(e,t){let i;try{i=this._tryCreateCardElement(t)}catch(r){return}e.parentElement&&e.parentElement.replaceChild(i,e)}},{kind:"method",key:"_renderCardElement",value:async function(e){let{type:t}=e;const{showElement:i,isCustom:r,name:a,description:o}=e,l=r?(0,h.cs)(t):void 0;let c;r&&(t=`${h.Qo}${t}`);let d={type:t};if(this.hass&&this.lovelace&&(d=await(async(e,t,i,r)=>{let n={type:t};const s=await(0,u.Do)(t);if(s&&s.getStubConfig){const t=s.getStubConfig(e,i,r);n={...n,...t}}return n})(this.hass,t,this._unusedEntities,this._usedEntities),i))try{c=this._tryCreateCardElement(d)}catch(p){c=void 0}return n.dy`
      <div class="card">
        <div
          class="overlay"
          @click=${this._cardPicked}
          .config=${d}
        ></div>
        <div class="card-header">
          ${l?`${this.hass.localize("ui.panel.lovelace.editor.cardpicker.custom_card")}: ${l.name||l.type}`:a}
        </div>
        <div
          class="preview ${(0,s.$)({description:!c||"HUI-ERROR-CARD"===c.tagName})}"
        >
          ${c&&"HUI-ERROR-CARD"!==c.tagName?c:l?l.description||this.hass.localize("ui.panel.lovelace.editor.cardpicker.no_description"):o}
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[n.iv`
        search-input {
          display: block;
          margin: 0 -8px;
        }

        .cards-container {
          display: grid;
          grid-gap: 8px 8px;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          margin-top: 20px;
        }

        .card {
          height: 100%;
          max-width: 500px;
          display: flex;
          flex-direction: column;
          border-radius: 4px;
          border: 1px solid var(--divider-color);
          background: var(--primary-background-color, #fafafa);
          cursor: pointer;
          box-sizing: border-box;
          position: relative;
        }

        .card-header {
          color: var(--ha-card-header-color, --primary-text-color);
          font-family: var(--ha-card-header-font-family, inherit);
          font-size: 16px;
          font-weight: bold;
          letter-spacing: -0.012em;
          line-height: 20px;
          padding: 12px 16px;
          display: block;
          text-align: center;
          background: var(
            --ha-card-background,
            var(--card-background-color, white)
          );
          border-radius: 0 0 4px 4px;
          border-bottom: 1px solid var(--divider-color);
        }

        .preview {
          pointer-events: none;
          margin: 20px;
          flex-grow: 1;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .preview > :first-child {
          zoom: 0.6;
          display: block;
          width: 100%;
        }

        .description {
          text-align: center;
        }

        .spinner {
          align-items: center;
          justify-content: center;
        }

        .overlay {
          position: absolute;
          width: 100%;
          height: 100%;
          z-index: 1;
        }

        .manual {
          max-width: none;
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.b0c4aa7f4b5c1d1a0c7f.js.map