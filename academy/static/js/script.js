function vizualizando_elemento(classname) {
    console.log("executando função de vizualizar cadastro de usuário");
    const element = document.querySelector(`.${classname}`)
    element.style.display = "flex";
}