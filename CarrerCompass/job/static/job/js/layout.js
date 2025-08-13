document.addEventListener("DOMContentLoaded", function()
{
    // Selecting menu bar and navigation container
    const menuBar = this.querySelector("#menu-bar")
    const navigationContainer = this.querySelector("#navigation-container")

    // Toggle show class of navigation container when menubar is clicked
    menuBar.addEventListener("click", function()
    {
        navigationContainer.classList.toggle("show")
    })

    // Selecing logo 
    const logo = this.querySelector("#logo")

    // Rotating logo when scroll happens
    window.addEventListener("scroll", function(event)
    {
        // Getting the amout to rotate
        rotation = this.scrollY

        // Rotatin logo
        logo.style.transform = `rotate(${rotation}deg)`
    })
})