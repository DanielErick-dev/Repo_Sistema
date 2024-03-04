function vizualizando_elemento(classname) {
    console.log("executando função de vizualização");
    const element = document.querySelector(`.${classname}`)
    console.log(element)
    element.style.visibility = 'visible';

}

