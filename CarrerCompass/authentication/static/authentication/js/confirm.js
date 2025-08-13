document.addEventListener("DOMContentLoaded", function()
{
    gsap.to(".otp-container", {
        "top" : "50%",
        "opacity" : 1,
        "duration" : 2
    })

    // Selecting form
    const otpForm = this.querySelector("#otp-form")

    otpForm.addEventListener("submit", function(event)
    {
        event.preventDefault()

        const formData = new FormData(this)

        const otpCode = formData.get("otp")

        if (!otpCode || !parseInt(otpCode) || parseInt(otpCode) < 100000 || parseInt(otpCode) > 999999)
        {
            this.querySelector(".otp-error").textContent = "Invalid Code"
            return 
        }

        this.submit()
    })
})