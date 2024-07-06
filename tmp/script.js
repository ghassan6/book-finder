    
// 1

for (let i = 0 ; i < 10 ; i++)
    {

        if (!books.includes({"title": book.items[i].volumeInfo.title}))
        {
            let item = book.items[i].volumeInfo
            let title = item.title,
                authors = item.authors,
                img = item.imageLinks,
                desc = item.description,
                ISBN = item.industryIdentifiers,
                pages = item.pageCount,
                category = item.categories, 
                date = item.publishedDate

                // console.log(img)
            if (item.imageLinks == undefined) {console.log(i)}

            books[i] = {
                "title": title === undefined ? "" : title,
                "authors": authors === undefined ? "" : authors,
                "img": img === undefined ? "" : img,
                "desc": desc === undefined ? "" : desc,
                "ISBN":  ISBN === undefined ? "" : ISBN,
                "pages": pages === undefined ? "" : pages,
                "category": category === undefined ? "" : category,
                "date": date === undefined ? "" : date,
                "id": i, 
            }
        }   
    }


// 2 

for (let i = 0 ; i < 10 ; i++)
{
    if(!books.includes({"title": book.items[i].volumeInfo.title}))
    {
        books[i] = {
            "info": book.items[i],
            "id": i
        }
    }
}


// for the arrow up and the display

let state = true
document.querySelector(".show").addEventListener("click" , () => {
    
    document.querySelector(".header").classList.toggle("display")
    if (state)
    {
        arr.classList.remove("fa-arrow-up")
        arr.classList.add("fa-arrow-down")
        state = false
    }
    else {
        arr.classList.remove("fa-arrow-down")
        arr.classList.add("fa-arrow-up")
        state = true
    }
    
})

// open library API

let test = document.querySelector("#testt")
if (test) {
    test.addEventListener("input" , async function() {
    
        let response = await fetch(`https://openlibrary.org/search.json?q=${test.value}`)
        let book = await response.json()
        let books = []
    
        for (let i = 0 ; i < 10 ; i++)
        {
            if(!books.includes({"title": book.docs[i].title })) 
            {
                books[i] = {
                    "title": book.docs[i].title,
                    "authors": book.docs[i].author_name[0],
    
                }
            }
        }
        console.log(book)
        // console.log(book.docs[0].title)
        console.log(typeof(books))
        console.log(books)
    
    })
}
