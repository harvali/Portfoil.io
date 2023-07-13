class TaskAdder extends HTMLElement {
    constructor() {
      super();
    }

  connectedCallback() {
    this.innerHTML = `
    <a href="#" onclick="clickFunction()"><div style="height:20px; width: 20px;" class="icons8-adder-bk" ></div></a>
    `;
  }
}


  customElements.define('add-er', TaskAdder);
