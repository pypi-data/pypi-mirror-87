(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4723],{72986:(t,e,i)=>{"use strict";i.d(e,{z:()=>a});i(43437);var s=i(87156),n=i(74460),r=new Set;const a={properties:{_parentResizable:{type:Object,observer:"_parentResizableChanged"},_notifyingDescendant:{type:Boolean,value:!1}},listeners:{"iron-request-resize-notifications":"_onIronRequestResizeNotifications"},created:function(){this._interestedResizables=[],this._boundNotifyResize=this.notifyResize.bind(this),this._boundOnDescendantIronResize=this._onDescendantIronResize.bind(this)},attached:function(){this._requestResizeNotifications()},detached:function(){this._parentResizable?this._parentResizable.stopResizeNotificationsFor(this):(r.delete(this),window.removeEventListener("resize",this._boundNotifyResize)),this._parentResizable=null},notifyResize:function(){this.isAttached&&(this._interestedResizables.forEach((function(t){this.resizerShouldNotify(t)&&this._notifyDescendant(t)}),this),this._fireResize())},assignParentResizable:function(t){this._parentResizable&&this._parentResizable.stopResizeNotificationsFor(this),this._parentResizable=t,t&&-1===t._interestedResizables.indexOf(this)&&(t._interestedResizables.push(this),t._subscribeIronResize(this))},stopResizeNotificationsFor:function(t){var e=this._interestedResizables.indexOf(t);e>-1&&(this._interestedResizables.splice(e,1),this._unsubscribeIronResize(t))},_subscribeIronResize:function(t){t.addEventListener("iron-resize",this._boundOnDescendantIronResize)},_unsubscribeIronResize:function(t){t.removeEventListener("iron-resize",this._boundOnDescendantIronResize)},resizerShouldNotify:function(t){return!0},_onDescendantIronResize:function(t){this._notifyingDescendant?t.stopPropagation():n.my||this._fireResize()},_fireResize:function(){this.fire("iron-resize",null,{node:this,bubbles:!1})},_onIronRequestResizeNotifications:function(t){var e=(0,s.vz)(t).rootTarget;e!==this&&(e.assignParentResizable(this),this._notifyDescendant(e),t.stopPropagation())},_parentResizableChanged:function(t){t&&window.removeEventListener("resize",this._boundNotifyResize)},_notifyDescendant:function(t){this.isAttached&&(this._notifyingDescendant=!0,t.notifyResize(),this._notifyingDescendant=!1)},_requestResizeNotifications:function(){if(this.isAttached)if("loading"===document.readyState){var t=this._requestResizeNotifications.bind(this);document.addEventListener("readystatechange",(function e(){document.removeEventListener("readystatechange",e),t()}))}else this._findParent(),this._parentResizable?this._parentResizable._interestedResizables.forEach((function(t){t!==this&&t._findParent()}),this):(r.forEach((function(t){t!==this&&t._findParent()}),this),window.addEventListener("resize",this._boundNotifyResize),this.notifyResize())},_findParent:function(){this.assignParentResizable(null),this.fire("iron-request-resize-notifications",null,{node:this,bubbles:!0,cancelable:!0}),this._parentResizable?r.delete(this):r.add(this)}}},32333:(t,e,i)=>{"use strict";var s=i(15652);class n extends s.oi{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},readonly:{type:Boolean},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number},valueLabel:{type:String},lowLabel:{type:String},highLabel:{type:String}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.readonly=!1,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1,this.attachedListeners=!1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _showHandle(){return!this.readonly&&(null!=this.value||null!=this.high&&null!=this.low)}_angleInside(t){let e=(this.startAngle+this.arcLength/2-t+180+360)%360-180;return e<this.arcLength/2&&e>-this.arcLength/2}_angle2xy(t){return this.rtl?{x:-Math.cos(t),y:Math.sin(t)}:{x:Math.cos(t),y:Math.sin(t)}}_xy2angle(t,e){return this.rtl&&(t=-t),(Math.atan2(e,t)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(t){const e=((t=Math.min(this.max,Math.max(this.min,t)))-this.min)/(this.max-this.min);return this._start+e*this._len}_angle2value(t){return Math.round((t/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const t=this._angle2xy(this._start),e=this._angle2xy(this._end);let i=1;this._angleInside(270)||(i=Math.max(-t.y,-e.y));let s=1;this._angleInside(90)||(s=Math.max(t.y,e.y));let n=1;this._angleInside(180)||(n=Math.max(-t.x,-e.x));let r=1;return this._angleInside(0)||(r=Math.max(t.x,e.x)),{up:i,down:s,left:n,right:r,height:i+s,width:n+r}}_mouse2value(t){const e=t.type.startsWith("touch")?t.touches[0].clientX:t.clientX,i=t.type.startsWith("touch")?t.touches[0].clientY:t.clientY,s=this.shadowRoot.querySelector("svg").getBoundingClientRect(),n=this._boundaries,r=e-(s.left+n.left*s.width/n.width),a=i-(s.top+n.up*s.height/n.height),o=this._xy2angle(r,a);return this._angle2value(o)}dragStart(t){if(!this._showHandle||this.disabled)return;let e=t.target,i=void 0;if(this._rotation&&"focus"!==this._rotation.type)return;if(e.classList.contains("shadowpath"))if("touchstart"===t.type&&(i=window.setTimeout((()=>{this._rotation&&(this._rotation.cooldown=void 0)}),200)),null==this.low)e=this.shadowRoot.querySelector("#value");else{const i=this._mouse2value(t);e=Math.abs(i-this.low)<Math.abs(i-this.high)?this.shadowRoot.querySelector("#low"):this.shadowRoot.querySelector("#high")}if(e.classList.contains("overflow")&&(e=e.nextElementSibling),!e.classList.contains("handle"))return;e.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const s="high"===e.id?this.low:this.min,n="low"===e.id?this.high:this.max;this._rotation={handle:e,min:s,max:n,start:this[e.id],type:t.type,cooldown:i},this.dragging=!0}_cleanupRotation(){const t=this._rotation.handle;t.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,t.blur()}dragEnd(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;this._cleanupRotation();let i=new CustomEvent("value-changed",{detail:{[e.id]:this[e.id]},bubbles:!0,composed:!0});this.dispatchEvent(i),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;if(this._rotation.cooldown)return window.clearTimeout(this._rotation.coldown),void this._cleanupRotation();if("focus"===this._rotation.type)return;t.preventDefault();const e=this._mouse2value(t);this._dragpos(e)}_dragpos(t){if(t<this._rotation.min||t>this._rotation.max)return;const e=this._rotation.handle;this[e.id]=t;let i=new CustomEvent("value-changing",{detail:{[e.id]:t},bubbles:!0,composed:!0});this.dispatchEvent(i)}_keyStep(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;"ArrowLeft"!==t.key&&"ArrowDown"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]+this.step):this._dragpos(this[e.id]-this.step)),"ArrowRight"!==t.key&&"ArrowUp"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]-this.step):this._dragpos(this[e.id]+this.step)),"Home"===t.key&&(t.preventDefault(),this._dragpos(this.min)),"End"===t.key&&(t.preventDefault(),this._dragpos(this.max))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(t){if(this.shadowRoot.querySelector(".slider")){const t=window.getComputedStyle(this.shadowRoot.querySelector(".slider"));if(t&&t.strokeWidth){const e=parseFloat(t.strokeWidth);if(e>this.handleSize*this.handleZoom){const t=this._boundaries,i=`\n          ${e/2*Math.abs(t.up)}px\n          ${e/2*Math.abs(t.right)}px\n          ${e/2*Math.abs(t.down)}px\n          ${e/2*Math.abs(t.left)}px`;this.shadowRoot.querySelector("svg").style.margin=i}}}if(this.shadowRoot.querySelector("svg")&&void 0===this.shadowRoot.querySelector("svg").style.vectorEffect){t.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach((t=>{if(t.getAttribute("stroke-width"))return;const e=parseFloat(getComputedStyle(t).getPropertyValue("stroke-width"));t.style.strokeWidth=e*this._scale+"px"}));const e=this.shadowRoot.querySelector("svg").getBoundingClientRect(),i=Math.max(e.width,e.height);this._scale=2/i}}_renderArc(t,e){const i=e-t;return t=this._angle2xy(t),e=this._angle2xy(e+.001),`\n      M ${t.x} ${t.y}\n      A 1 1,\n        0,\n        ${i>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${e.x} ${e.y}\n    `}_renderHandle(t){const e=this._value2angle(this[t]),i=this._angle2xy(e),n={value:this.valueLabel,low:this.lowLabel,high:this.highLabel}[t]||"";return s.YP`
      <g class="${t} handle">
        <path
          id=${t}
          class="overflow"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${t}
          class="handle"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          role="slider"
          aria-valuemin=${this.min}
          aria-valuemax=${this.max}
          aria-valuenow=${this[t]}
          aria-disabled=${this.disabled}
          aria-label=${n||""}
          />
        </g>
      `}render(){const t=this._boundaries;return s.dy`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-t.left} ${-t.up} ${t.width} ${t.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        ?disabled=${this.disabled}
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          <path
            class="bar"
            vector-effect="non-scaling-stroke"
            d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
          />
          <path
            class="shadowpath"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
            stroke="rgba(0,0,0,0)"
            stroke-width="${3*this.handleSize*this._scale}"
            stroke-linecap="butt"
          />

        </g>

        <g class="handles">
        ${this._showHandle?null!=this.low?this._reverseOrder?s.dy`${this._renderHandle("high")} ${this._renderHandle("low")}`:s.dy`${this._renderHandle("low")} ${this._renderHandle("high")}`:s.dy`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return s.iv`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
        display: block;
      }
      path {
        transition: stroke 1s ease-out, stroke-width 200ms ease-out;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      svg[disabled] .bar {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
        cursor: var(--round-slider-handle-cursor, pointer);
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      svg[disabled] g.handles {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      .handle:focus {
        outline: unset;
      }
    `}}customElements.define("round-slider",n)},14516:(t,e,i)=>{"use strict";i.d(e,{Z:()=>n});var s=function(t,e){return t.length===e.length&&t.every((function(t,i){return s=t,n=e[i],s===n;var s,n}))};const n=function(t,e){var i;void 0===e&&(e=s);var n,r=[],a=!1;return function(){for(var s=arguments.length,o=new Array(s),h=0;h<s;h++)o[h]=arguments[h];return a&&i===this&&e(o,r)||(n=t.apply(this,o),a=!0,i=this,r=o),n}}}}]);
//# sourceMappingURL=chunk.da700f56c41fa1ff2626.js.map