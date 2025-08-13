// Username: 5–20 characters, starts with letters, optional numbers at the end
const USERNAME_REGEX = /^(?=.{5,20}$)[A-Za-z]+[0-9]*$/;

// Password: 8–20 chars, at least one uppercase, lowercase, digit, special char, no spaces
const PASSWORD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9])(?!.*\s).{8,20}$/;


document.addEventListener("DOMContentLoaded", function()
{

    // Adding resize event on window
    window.addEventListener("resize", function()
    {
        width = window.innerWidth

        // if width is less than 700 hide all text and show related form
        if (width < 700)
        {
            
            // Hide text
            loginText.style.display = "none"
            registerText.style.display = "none"

            // Check which form is currently display and hide the other one
            if (this.getComputedStyle(registerForm).display == "flex")
            {
                // Hide loginform
                loginForm.style.display = "none"

                // Change button style
                registerBtn.classList.add("primary-btn")
                loginBtn.classList.remove("primary-btn")
            }

            else 
            {
                registerForm.style.display = "none"

                // Change button style
                registerBtn.classList.remove("primary-btn")
                loginBtn.classList.add("primary-btn")
            }
        }

        // if greater than 700 show related form and text
        else 
        {
            if (this.getComputedStyle(registerForm).display == "flex")
            {
                // hide loginform and registertext
                loginForm.style.display = "none"
                registerText.style.display = "none"

                // Show logintext
                loginText.style.display = "flex"
            }

            else 
            {
                // hide register form and login text
                registerForm.style.display = "none"
                loginText.style.display = "none"

                // Show register text
                registerText.style.display = "flex"

                // Adjust position
                registerText.style.left = 0
                loginForm.style.left = "50%"
                loginText.style.left = 0
                registerForm.style.left = "50%"
            }
        }
    })

    // Showing animation
    showAnimation()

    // Selecting register button and login button and their container
    const registerBtn = document.querySelector(".register-btn")
    const loginBtn = this.documentElement.querySelector(".login-btn")
    const buttonContainer = document.querySelector(".button-container")

    // Selectin loginform and register form 
    const loginForm = document.querySelector("#login-form")
    const registerForm = document.querySelector("#register-form")

    // Selecing switch buttons
    const registerSwitch = document.querySelector(".register-switch-btn")
    const loginSwitch = document.querySelector(".login-switch-btn")

    // Selecing text for login and register
    const registerText = document.querySelector(".register-text")
    const loginText = document.querySelector(".login-text")

    const parentDiv = this.querySelector(".register-container")

    // Change button style according to login or register
    if (parentDiv.classList.contains("isLogging"))
    {
        registerBtn.classList.remove("primary-btn")
        loginBtn.classList.add("primary-btn")
    }

    // Adding event on ButtonContainer 
    buttonContainer.addEventListener("click", function(event)
    {
        // Check if user is clicking already active butto
        if (event.target.classList.contains("primary-btn"))
        {
            return 
        }
        
        // Check which button trigger the event 
        if (event.target.classList.contains("login-btn"))
        {
            // Showing form
            loginForm.style.display = "flex"

            // Hiding register
            registerForm.style.display = "none"

            // Chaning button style
            loginBtn.classList.add("primary-btn")
            registerBtn.classList.remove("primary-btn")

            showAnimation()
        }

        else 
        {
            // Showing register form
            registerForm.style.display = "flex"

            // Hiding register
            loginForm.style.display = "none"

            // Chaning button style
            registerBtn.classList.add("primary-btn")
            loginBtn.classList.remove("primary-btn")

            showAnimation()
        }
    })

    // Adding event on loginSwitch
    loginSwitch.addEventListener("click", function()
    {
        // Kill previous animation
        gsap.killTweensOf(["#register-form", "#login-form", ".register-text", ".login-text"])

        // Showing login form and register text
        gsap.timeline()
            .set("#register-form", { "left" : "50%", "display" : "none"})
            .set(".login-text", { "left" : "0", "display" : "none"})
            .to("#login-form", { "left" : "50%", "display" : "flex", "duration" : 0.5}, 0)
            .to(".register-text", { "left" : "0", "display" : "flex", "duration" : 0.5}, 0)
    })

    // Adding event on registerSwitch
    registerSwitch.addEventListener("click", function()
    {   
        // Kill previous animation
        gsap.killTweensOf(["#register-form", "#login-form", ".register-text", ".login-text"])

        // Hide login form and register text
        gsap.timeline()
            .set("#login-form", { "left" : "0", "display" : "none"})
            .set(".register-text", { "left" : "50%", "display" : "none"})
            .to("#register-form", { "left" : "0", "display" : "flex", "duration" : 0.5}, 0)
            .to(".login-text", { "left" : "50%", "display" : "flex", "duration" : 0.5}, 0)
    })

    //Adding event on register form
    registerForm.addEventListener("submit", function(event)
    {
        event.preventDefault()

        // Clearing all error message
        const spanList = this.querySelectorAll("span")
        spanList.forEach(function(span)
        {
            span.textContent = ""
        })

        // Validat user type
        const validType = ["employee", "employer"]

        // Getting userinput data
        const data = new FormData(this)

        const username = data.get("username").trim()
        const email = data.get("email").trim()
        const type = data.get("user_type")
        const password = data.get("password").trim()
        const confirm_password = data.get("confirm_password").trim()

        // Checking validation
        if (!username || !USERNAME_REGEX.test(username))
        {
            this.querySelector(".username-error").textContent = "Username must be 5–20 characters, starts with letters, optional numbers at the end"
            return 
        }

        if (!email)
        {
            this.querySelector(".register-email-error").textContent = "Invalid email"
            return 
        }

        if (!type || !validType.includes(type))
        {
            this.querySelector(".user-type-error").textContent = "Invalid User Type"
            return 
        }

        if (!password || !PASSWORD_REGEX.test(password))
        {
            this.querySelector(".register-password-error").textContent = "Password must be 8–20 chars, at least one uppercase, lowercase, digit, special char, no spaces"
            return 
        }

        if (!confirm_password || confirm_password != password)
        {
            this.querySelector(".confirm-password-error").textContent = "Passwords must match"
            return 
        }

        this.submit()
    })

    // Adding event on login form
    loginForm.addEventListener("submit", function(event)
    {
        console.log("submit")
        event.preventDefault()

        // Clearing all span message
        const oldSpans = this.querySelectorAll("span")
        oldSpans.forEach(function(span)
        {
            span.textContent = ""
        })

        // Getting form data
        data = new FormData(this) 

        // Getting user input
        email = data.get("email")
        password = data.get("password")

        if (!email)
        {
            this.querySelector(".login-email-error").textContent = "Invalid Email"
            return 
        }

        if (!password || !PASSWORD_REGEX.test(password))
        {
            this.querySelector(".login-password-error").textContent = "Password must be 8–20 chars, at least one uppercase, lowercase, digit, special char, no spaces"
            return 
        }

        this.submit()
    })
})

// Function for showing animation
function showAnimation()
{
    // Creating timeline
    const tl = gsap.timeline()

    // Adding animation
    tl.from(".button-container", { "opacity" : 0, "y" : -20, "duration" : 0.5})
    .from(".form", { "opacity" : 0, "y" : 30, "duration" : 0.5})
}