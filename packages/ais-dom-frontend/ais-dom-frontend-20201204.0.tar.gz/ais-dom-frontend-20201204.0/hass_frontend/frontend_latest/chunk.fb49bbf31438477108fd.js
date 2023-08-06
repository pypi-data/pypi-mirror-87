(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6169],{6169:(t,r,s)=>{"use strict";s.r(r);var e=s(15652),i=s(50467),o=s(99476);class n extends o.p{async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square)return this._cards.length/this.columns*2;const t=[];for(const r of this._cards)t.push((0,i.N)(r));const r=await Promise.all(t);return Math.max(...r)*(this._cards.length/this.columns)}get columns(){var t;return(null===(t=this._config)||void 0===t?void 0:t.columns)||3}get square(){var t;return!1!==(null===(t=this._config)||void 0===t?void 0:t.square)}setConfig(t){super.setConfig(t),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.toggleAttribute("square",this.square)}static get styles(){return[super.sharedStyles,e.iv`
        #root {
          display: grid;
          grid-template-columns: repeat(
            var(--grid-card-column-count, ${3}),
            minmax(0, 1fr)
          );
          grid-gap: var(--grid-card-gap, 8px);
        }
        :host([square]) #root {
          grid-auto-rows: 1fr;
        }
        :host([square]) #root::before {
          content: "";
          width: 0;
          padding-bottom: 100%;
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }

        :host([square]) #root > *:first-child {
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }
      `]}}customElements.define("hui-grid-card",n)}}]);
//# sourceMappingURL=chunk.fb49bbf31438477108fd.js.map