let password = document.querySelector("#pass")
let len = document.querySelector("#length")
let capital = document.querySelector("#capital")
let number = document.querySelector("#number")
let icons =  document.querySelectorAll(".icon")
let register = document.querySelector(".register")

let passwords = document.querySelectorAll(".pass")





// does not work on every page
// error stops the whole script??
if (password)
{
    password.addEventListener('keyup' , () => {
        let pass = password.value
        strengthChecker(pass)
        
    })  
}


function strengthChecker(str) {
    let strength = 0
    if (str.length > 7) 
    {   
        len.classList.remove("invalid")
        len.classList.add("valid")
        strength += 1
    }
    else {
        len.classList.remove("valid")
        len.classList.add("invalid")
    }

    if (str.match(/[0-9]/))
    {
        number.classList.remove("invalid")
        number.classList.add("valid")
        strength += 1
    }
    else 
    {
        number.classList.remove("valid")
        number.classList.add("invalid")
    }

    if (str.match(/[A-Z]/))
    {
        capital.classList.remove("invalid")
        capital.classList.add("valid")
        strength += 1
    }
    else 
    {
        capital.classList.remove("valid")
        capital.classList.add("invalid")
    }

    if (strength === 3) register.value = true
  
}



for (let i = 0 ; i < icons.length ; i++)
{
    let state = true
        icons[i].addEventListener("click" , () => {

            
        if (state) {
            passwords[i].setAttribute("type" , "text")
            icons[i].classList.remove("fa-eye")
            icons[i].classList.add("fa-eye-slash")
            state = false
        }

        else {
            passwords[i].setAttribute("type" , "password")
            icons[i].classList.remove("fa-eye-slash")
            icons[i].classList.add("fa-eye")
            state = true
        }
        
        })
    
}

