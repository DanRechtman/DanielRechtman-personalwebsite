const template = document.createElement("template")
template.innerHTML =
`
<style>
   
</style>
<input type="text" placeholder='Text'>
`

class SearchItem extends HTMLElement {
    constructor(){
        super()
        const shadow = this.attachShadow({mode:'open'})
        shadow.append(template.content.cloneNode(true))
    }

    connectedCallback(){
        this.inputElement = this.shadowRoot.querySelector( "input");
        this.inputElement.addEventListener("input",this.handleInput);
    }
    handleInput = (event)=>{
        if (event.target.value.length > 2){
            console.log('InputValue:',event.target.value);
        }
    }
    
}

customElements.define("search-item",SearchItem)