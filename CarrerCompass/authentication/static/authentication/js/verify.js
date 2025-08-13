document.addEventListener("DOMContentLoaded", function()
{
    // Showing form
    gsap.to(".verify-container", {"opacity" : 1,"top" : "50%", "duration" : 3})

    // Selecting form
    const verifyForm = document.querySelector("#verify-form")

    // Adding submit event on form
    verifyForm.addEventListener("submit", function(event)
    {
        event.preventDefault()

        // Getting form data
        data = new FormData(this)

        code = data.get("digit")

        if (!code || !parseInt(code) || parseInt(code) < 111111 || parseInt(code) > 999999)
        {
            // Show error message
            this.querySelector(".digit-error").textContent = "Invalid Verification Code"
            return 
        }

        this.submit()
    })
})