document.addEventListener("DOMContentLoaded", function()
{
    gsap.to(".forgot-container", {
        "top" : "50%",
        "opacity" : 1,
        "duration" : 2
    })

    const forgotForm = this.querySelector("#forgot-form")

    // Adding event on forgotForm
    forgotForm.addEventListener("submit", function(event)
    {
        event.preventDefault()

        // Getting form data
        formData = new FormData(this)

        // Getting user input 
        const email = formData.get("email")

        if (!email)
        {
            this.querySelector(".email-error").textContent = "Invalid Email"
            return 
        }

        this.submit()
    })
})