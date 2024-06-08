const form = document.getElementById("image-upload-form")


form.addEventListener("submit", handleSubmit)

async function handleSubmit(e) {
    e.preventDefault()
    const bodyFormat = new FormData()
    // const myHeaders = new Headers();
    // myHeaders.append("Content-Type", "multipart/form-data");

    const file = document.getElementById("image").files[0]

    bodyFormat.append("name", document.getElementById("model").value)   
    bodyFormat.append("file", file)

    try {
        const response = await fetch("https://ez3vlribw0.execute-api.us-east-1.amazonaws.com/v1", {
            method: "POST",
            headers: {
                "Content-type": "multipart/form-data"
            },
            body: bodyFormat
        })

        const data = await response.json()

        console.log(data)
    } catch (error) {
        console.log(error)
    }
}