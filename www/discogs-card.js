import { LitElement, html, css } from "https://unpkg.com/lit-element@2.0.1/lit-element.js?module";

class DiscogsCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {}
    };
  }

  static get styles() {
    return css`
      ha-card {
        width: 500px;
        height: 500px;
        background-size: cover;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }

      .record-text {
        background: white;
        z-index: 1;
        padding: 1rem;
        font-size: 1.2rem;
        font-weight: bold;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        padding: 0 1.2rem;
      }

      .record-text div {

      }

      .record-format {
        font-size: 0.9rem;
        color: gray;
      }
    `
  }


  getAttributes(entity) {
    const { attributes } = entity;
    return attributes;
  }

  setConfig(config) {
    if (!config.entity) throw new Error('You need to define your sensor.discogs_random_record entity');
    this.config = config;
  }

  getCardSize() {
    return 3;
  }

  render() {
    const entity = this.hass.states[this.config.entity];
    const { cover_image, released, format } = this.getAttributes(entity);
    const { state } = entity;

    return html`
      <ha-card style="background-image: url('${cover_image}')">
        <div class="record-text">
          <div>
            <p>${state}<p>
            <p class="record-format">${format}<p>
          </div>
          <date>${released}</date>
        </div>
      </ha-card>
    `
  }
}

customElements.define('discogs-card', DiscogsCard);
