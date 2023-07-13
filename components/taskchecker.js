class TaskChecker extends HTMLElement {
    constructor() {
      super();
    }

  connectedCallback() {
    this.innerHTML = `
    <div style="height:20px; width: 20px;" class="icons8-checked-bk"></div><div style="height:20px; width: 20px;" class="icons8-trash-bk"></div>
    `;
  }
}



  customElements.define('chec-ker', TaskChecker);
