const form = document.getElementById("image-upload-form")
const options_wrapper = document.querySelector(".options_wrapper")
const li_elemts = document.querySelectorAll("ul > li")
const input = document.getElementById("model")
const resultMessage = document.querySelector(".result")


form.addEventListener("submit", handleSubmit)

async function handleSubmit(e) {
    e.preventDefault()
    const bodyFormat = new FormData()
    const file = document.getElementById("image").files[0]

    bodyFormat.append("name", document.getElementById("model").value)   
    bodyFormat.append("file", file)

    try {
        const response = await fetch("https://ez3vlribw0.execute-api.us-east-1.amazonaws.com/v1", {
            method: "POST",

            body: bodyFormat
        })

        const data = await response.json()
        resultMessage.classList.add("visible")
        console.log(data)
    } catch (error) {
        console.log(error)
    }
}



li_elemts.forEach(li_elem => {
    li_elem.addEventListener("click", () => {
        input.value = li_elem.innerText
        options_wrapper.classList.toggle("visible")
    }) 
})

input.addEventListener("focus", () => options_wrapper.classList.toggle("visible"))
input.addEventListener("blur", () =>  setTimeout(() => options_wrapper.classList.remove("visible"), 260))