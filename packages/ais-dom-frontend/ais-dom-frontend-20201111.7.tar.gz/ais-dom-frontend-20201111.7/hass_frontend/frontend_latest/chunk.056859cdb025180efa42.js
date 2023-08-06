(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2211],{1090:(e,t,a)=>{"use strict";a(8878),a(30879),a(53973),a(51095);var i=a(50856),n=a(28426);class o extends n.H3{static get template(){return i.d`
      <style>
        :host {
          display: block;
          @apply --paper-font-common-base;
        }

        paper-input {
          width: 30px;
          text-align: center;
          --paper-input-container-input: {
            /* Damn you firefox
             * Needed to hide spin num in firefox
             * http://stackoverflow.com/questions/3790935/can-i-hide-the-html5-number-input-s-spin-box
             */
            -moz-appearance: textfield;
            @apply --paper-time-input-cotnainer;
          }
          --paper-input-container-input-webkit-spinner: {
            -webkit-appearance: none;
            margin: 0;
            display: none;
          }
          --paper-input-container-shared-input-style_-_-webkit-appearance: textfield;
        }

        paper-dropdown-menu {
          width: 55px;
          padding: 0;
          /* Force ripple to use the whole container */
          --paper-dropdown-menu-ripple: {
            color: var(
              --paper-time-input-dropdown-ripple-color,
              var(--primary-color)
            );
          }
          --paper-input-container-input: {
            @apply --paper-font-button;
            text-align: center;
            padding-left: 5px;
            @apply --paper-time-dropdown-input-cotnainer;
          }
          --paper-input-container-underline: {
            border-color: transparent;
          }
          --paper-input-container-underline-focus: {
            border-color: transparent;
          }
        }

        paper-item {
          cursor: pointer;
          text-align: center;
          font-size: 14px;
        }

        paper-listbox {
          padding: 0;
        }

        label {
          @apply --paper-font-caption;
          color: var(
            --paper-input-container-color,
            var(--secondary-text-color)
          );
        }

        .time-input-wrap {
          @apply --layout-horizontal;
          @apply --layout-no-wrap;
        }

        [hidden] {
          display: none !important;
        }
      </style>

      <label hidden$="[[hideLabel]]">[[label]]</label>
      <div class="time-input-wrap">
        <!-- Hour Input -->
        <paper-input
          id="hour"
          type="number"
          value="{{hour}}"
          label="[[hourLabel]]"
          on-change="_shouldFormatHour"
          on-focus="_onFocus"
          required
          prevent-invalid-input
          auto-validate="[[autoValidate]]"
          maxlength="2"
          max="[[_computeHourMax(format)]]"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
        >
          <span suffix="" slot="suffix">:</span>
        </paper-input>

        <!-- Min Input -->
        <paper-input
          id="min"
          type="number"
          value="{{min}}"
          label="[[minLabel]]"
          on-change="_formatMin"
          on-focus="_onFocus"
          required
          auto-validate="[[autoValidate]]"
          prevent-invalid-input
          maxlength="2"
          max="59"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
        >
          <span hidden$="[[!enableSecond]]" suffix slot="suffix">:</span>
        </paper-input>

        <!-- Sec Input -->
        <paper-input
          id="sec"
          type="number"
          value="{{sec}}"
          label="[[secLabel]]"
          on-change="_formatSec"
          on-focus="_onFocus"
          required
          auto-validate="[[autoValidate]]"
          prevent-invalid-input
          maxlength="2"
          max="59"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
          hidden$="[[!enableSecond]]"
        >
        </paper-input>

        <!-- Dropdown Menu -->
        <paper-dropdown-menu
          id="dropdown"
          required=""
          hidden$="[[_equal(format, 24)]]"
          no-label-float=""
          disabled="[[disabled]]"
        >
          <paper-listbox
            attr-for-selected="name"
            selected="{{amPm}}"
            slot="dropdown-content"
          >
            <paper-item name="AM">AM</paper-item>
            <paper-item name="PM">PM</paper-item>
          </paper-listbox>
        </paper-dropdown-menu>
      </div>
    `}static get properties(){return{label:{type:String,value:"Time"},autoValidate:{type:Boolean,value:!0},hideLabel:{type:Boolean,value:!1},floatInputLabels:{type:Boolean,value:!1},alwaysFloatInputLabels:{type:Boolean,value:!1},format:{type:Number,value:12},disabled:{type:Boolean,value:!1},hour:{type:String,notify:!0},min:{type:String,notify:!0},sec:{type:String,notify:!0},hourLabel:{type:String,value:""},minLabel:{type:String,value:":"},secLabel:{type:String,value:""},enableSecond:{type:Boolean,value:!1},noHoursLimit:{type:Boolean,value:!1},amPm:{type:String,notify:!0,value:"AM"},value:{type:String,notify:!0,readOnly:!0,computed:"_computeTime(min, hour, sec, amPm)"}}}validate(){let e=!0;return this.$.hour.validate()&&this.$.min.validate()||(e=!1),this.enableSecond&&!this.$.sec.validate()&&(e=!1),12!==this.format||this.$.dropdown.validate()||(e=!1),e}_computeTime(e,t,a,i){let n;return(t||e||a&&this.enableSecond)&&(a=a||"00",n=(t=t||"00")+":"+(e=e||"00"),this.enableSecond&&a&&(n=n+":"+a),12===this.format&&(n=n+" "+i)),n}_onFocus(e){e.target.inputElement.inputElement.select()}_formatSec(){1===this.sec.toString().length&&(this.sec=this.sec.toString().padStart(2,"0"))}_formatMin(){1===this.min.toString().length&&(this.min=this.min.toString().padStart(2,"0"))}_shouldFormatHour(){24===this.format&&1===this.hour.toString().length&&(this.hour=this.hour.toString().padStart(2,"0"))}_computeHourMax(e){return this.noHoursLimit?null:12===e?e:23}_equal(e,t){return e===t}}customElements.define("paper-time-input",o)},40164:(e,t,a)=>{"use strict";a.r(t);a(53268),a(12730);var i=a(50856),n=a(28426),o=(a(60010),a(38353),a(63081),a(47181));a(1090);class s extends n.H3{static get template(){return i.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }

        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .card-actions {
          display: flex;
        }
        ha-card > paper-toggle-button {
          margin: -4px 0;
          position: absolute;
          top: 32px;
          right: 8px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        div.person {
          display: inline-block;
          margin: 10px;
        }
        img {
          border-radius: 50%;
          width: 100px;
          height: 100px;
          border: 20px;
        }
        img.person-img-selected {
          border: 7px solid var(--primary-color);
          width: 110px;
          height: 110px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienia głosu Asystenta</span>
            <span slot="introduction"
              >Możesz zmienić głos asystenta i dostosować szybkość i ton mowy
              oraz godziny, w których asystent powinien być ściszony</span
            >
            <ha-card header="Wybór głosu Asystenta">
              <div class="card-content">
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Jola online")]]'
                    data-voice="Jola online"
                    alt="Jola Online"
                    title="Jola Online"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Ania.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Jola lokalnie")]]'
                    data-voice="Jola lokalnie"
                    alt="Jola Lokalnie"
                    title="Jola Lokalnie"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Asia.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Celina")]]'
                    data-voice="Celina"
                    alt="Celina"
                    title="Celina"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Celka.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Anżela")]]'
                    data-voice="Anżela"
                    alt="Anżela"
                    title="Anżela"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Anzela.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Asia")]]'
                    data-voice="Asia"
                    alt="Asia"
                    title="Asia"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Kasia.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Sebastian")]]'
                    data-voice="Sebastian"
                    alt="Sebastian"
                    title="Sebastian"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Sebastian.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Bartek")]]'
                    data-voice="Bartek"
                    alt="Bartek"
                    title="Bartek"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Bartek.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class$='[[personImgClass(selectedVoice, "Andrzej")]]'
                    data-voice="Andrzej"
                    alt="Andrzej"
                    title="Andrzej"
                    on-click="switchTtsPerson"
                    src="/static/ais_dom/Andrzej.jpg"
                  />
                </div>
              </div>
              <div class="card-actions person-actions">
                <div on-click="tuneVoiceTone">
                  <ha-icon-button
                    class="user-button"
                    icon="hass:tune"
                  ></ha-icon-button
                  ><mwc-button>Ton mowy</mwc-button>
                </div>
                <div on-click="tuneVoiceSpeed">
                  <ha-icon-button
                    class="user-button"
                    icon="hass:play-speed"
                  ></ha-icon-button
                  ><mwc-button>Szybkość mowy</mwc-button>
                </div>
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:account"
                  ></ha-icon-button
                  ><mwc-button>[[selectedVoice]]</mwc-button>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,selectedVoice:{type:String,computed:"_computeAisSelectedVoice(hass)"}}}computeClasses(e){return e?"content":"content narrow"}_computeAisSelectedVoice(e){return e.states["input_select.assistant_voice"].state}personImgClass(e,t){return e===t?"person-img-selected":""}tuneVoiceSpeed(){(0,o.B)(this,"hass-more-info",{entityId:"input_number.assistant_rate"})}tuneVoiceTone(){(0,o.B)(this,"hass-more-info",{entityId:"input_number.assistant_tone"})}switchTtsPerson(e){this.hass.callService("input_select","select_option",{entity_id:"input_select.assistant_voice",option:e.target.dataset.voice})}}customElements.define("ha-config-ais-dom-config-tts",s)}}]);
//# sourceMappingURL=chunk.056859cdb025180efa42.js.map