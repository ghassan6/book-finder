let password = document.querySelectorAll(".check")
let len = document.querySelector("#length")
let capital = document.querySelector("#capital")
let number = document.querySelector("#number")
let icons =  document.querySelectorAll(".icon")
let register = document.querySelector(".register")
let passwords = document.querySelectorAll(".pass")
let arr = document.querySelector(".arr")

if (password)
{
    password.forEach(el => {
        el.addEventListener('keyup' , () => {   
            let pass = el.value
            strengthChecker(pass) 
         })
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

//  API
let search = document.querySelector("#book")
if (search)
{
    search.addEventListener("input" , async function() {
        let response = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${search.value}&orderBy=relevance`)
        let book = await response.json()
        let books = []
        let noImage = '/static/pics/not-available.jpg'
        for (let i = 0 ; i < 10 ; i++)
        {
            if (!books.includes({"title": book.items[i].volumeInfo.title}))
            {      

                let item = book.items[i].volumeInfo
                books[i] = {
                    "title": item.title,
                    "authors": item.authors === undefined ? "Unknown" : item.authors[0],
                    "img": item.imageLinks === undefined ? noImage : item.imageLinks.thumbnail,
                    "desc": item.description === undefined ? "No Description available." : item.description,
                    "identifier": get_identifier(item.industryIdentifiers),
                    "pages": item.pageCount === undefined ? "-" : item.pageCount,
                    "category": item.categories === undefined ? "" : item.categories,
                    "date": item.publishedDate === undefined ? "" : item.publishedDate,
                    "googleLink": item.infoLink === undefined ? "" : item.infoLink,
                    "publisher": item.publisher === undefined ? "" : item.publisher,
                    "id": i, 
                }
            } 
            
        }

        fetch(`${window.origin}/result`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(books),
            cache: "no-cache",
            headers: new Headers({
                "Content-Type": "application/json"
            })
          })
        
    })
}

// message

function submit_message() {

    let fname = document.querySelector("#fName")
    let lname = document.querySelector("#lName")
    let message = document.querySelector("#message")
    let email = document.querySelector("#email")

    let feedback = {
        "first-name": fname.value,
        "last-name": lname.value,
        "email": email.value,
        "message": message.value,
    }

    fetch(`${window.origin}/contact/feedback` , {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(feedback),
        cache: "no-cache",
        headers: new Headers ({
            "content-type": "application/json"
        })
    })
}

function get_identifier(identifier) {
    if (!identifier) return "None"
    else if (identifier[0]["type"] == "OTHER") return identifier[0]['identifier']
    else if (identifier.length == 2) 
    {
        if (identifier[0]['type'] == "ISBN_10") return `ISBN: ${identifier[0]['identifier']}`
        else return `ISBN ${identifier[1]['identifier']}`
    }
    else return `ISBN ${identifier[0]['identifier']}`
}
