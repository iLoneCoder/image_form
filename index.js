const form = document.getElementById("image-upload-form")


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

        console.log(data)
    } catch (error) {
        console.log(error)
    }
}