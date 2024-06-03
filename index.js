const form = document.getElementById("image-upload-form")


form.addEventListener("submit", handleSubmit)

function handleSubmit(e) {
    e.preventDefault()
    console.log("submited")
}