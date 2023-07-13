class Header extends HTMLElement {
    constructor() {
      super();
    }

  connectedCallback() {
    this.innerHTML = `
      <header>
        <nav class="navbar">
        <div class="nav-brand">
            <a href="#">Portfoil.io</a>
        </div>
        <input id="menu-toggle" type="checkbox" />
        <label class='menu-button-container' for="menu-toggle">
        <div class='menu-button'></div>
        </label>
        <ul class="navbar-nav">   
            <li class="nav-item"><a class="nav-link" href="index.html"><i class="fa fa-home fa-2x fa-fw"></i> Home</a> </li>
            <li class="nav-item"><a class="nav-link" href="cv.html"><i class="fa fa-file-text fa-2x fa-fw"></i> Resume</a></li>
            <li class="nav-item"><a class="nav-link" href="projects.html"><i class="fa fa-cog fa-2x fa-fw"></i> Projects</a></li>
            <li class="nav-item"><a class="nav-link" href="blog.html"><i class="fa-solid fa-blog fa-2x fa-fw"></i> Blog</a></li>
            <li class="nav-item"><a class="nav-link" href="https://github.com/harvali"><i class="fa fa-github fa-2x fa-fw"></i> Github</a></li>
            <li class="nav-item"><a class="nav-link" href="https://www.linkedin.com/in/harvali/"><i class="fa fa-linkedin-square fa-2x fa-fw"></i> LinkedIn</a></li>
        </ul>
    </nav>


      </header>
    `;
  }
}



  customElements.define('header-component', Header);
