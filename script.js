const searchForm=document.getElementById("search-form");
const searchInput=document.getElementById("search-input");
const subjectFilter=document.getElementById("subject-filter");
const sortFilter=document.getElementById("sort-filter");
const booksContainer=document.getElementById("books-container");
const message=document.getElementById("message");

let books=[];

async function fetchBooks(searchTerm = "education"){

    message.textContent = "Loading books...";
    booksContainer.innerHTML = "";
    
    try{
    
        const params = new URLSearchParams({
            q: searchTerm,
            fields:"key,title,author_name,first_publish_year,edition_count,cover_i",
            limit: "25"
        });

        const apiURL = `https://openlibrary.org/search.json?${params}`;
        const response = await fetch (apiURL);

        if (!response.ok){
      throw new Error ("Unable to fetch books. Please try again");  
    }
    const data = await response.json();
    books = data.docs || [];

    displayBooks(books);
}
catch (error){
    message.textContent = 
    "Something went wrong. Please check your internet connection and try again.";
    console.error ("API Error:", error);
}
}
function displayBooks(bookList){
    booksContainer.innerHTML = "";

    if (bookList.length === 0){
        message.textContent = "No books found. Try another search.";
        return;
    }
    message.textContent = `Found ${bookList.length} books.`;
    bookList.forEach(book =>{
        const card = document.createElement("div");
            card.classList.add("book-card");
const title = book.title || "Unknown Title";
const author = book.author_name
? book.author_name.slice(0,2).join(",")
: "Unknown Author";
      
const year = book.first_publish_year || "Not available";

const cover = book.cover_i
?`https://covers.openlibrary.org/b/id/${book.cover_i}-M.jpg`
:"";

const image = document.createElement("img");

if (cover){
    image.src = cover;
    image.alt = `Cover of ${title}`;
} else {
    image.alt = "No cover available";
}
image.loading = "lazy";

image.onerror = function(){
    image.removeAttribute("src");
    image.alt = "Book cover unavailable";
};
const bookTitle = document.createElement("h3");
bookTitle.textContent = title;

const bookAuthor = document.createElement("p");
bookAuthor.textContent = `Author: ${author}`;

const bookYear = document.createElement("p");
bookYear.textContent = `Published: ${year}`;

const editions = document.createElement("p");
editions.textContent = `Edition: ${book.edition_count || "Not available"}`;

const link = document.createElement("a");

link.href = book.key 
? `https://openlibrary.org${book.key}`
: "https://openlibrary.org/";

link.textContent = "View Book";

link.target = "_blank";
link.rel = "noopener noreferrer";

card.appendChild(image);
card.appendChild(bookTitle);
card.appendChild(bookAuthor);
card.appendChild(bookYear);
card.appendChild(editions);
card.appendChild(link);

booksContainer.appendChild(card);
});

}

function searchBooks(){
     
 const searchTerm = searchInput.value.trim();
 const subject = subjectFilter.value;

 if (!searchTerm && subject === "all"){
    message.textContent = " Please enter a search term or choose a subject.";
    return;
 }
 let query = searchTerm;

 if (subject !== "all"){
    query = `${query} ${subject}`.trim();
 }
 fetchBooks(query);
}

searchForm.addEventListener("submit", function (event){
    event.preventDefault();
    searchBooks();
});

subjectFilter.addEventListener("change", function () {

    searchBooks();
});

sortFilter.addEventListener("change", function(){

    const sortedBooks = [...books];

    if (sortFilter.value === "title"){

        sortedBooks.sort((a,b)=>
        (a.title || "").localeCompare(b.title || ""));
    } else if (sortFilter.value === "newest"){

        sortedBooks.sort((a,b)=>
        (b.first_publish_year || 0) -
        (a.first_publish_year || 0)
    );
    } else if (sortFilter.value === "oldest"){
        sortedBooks.sort((a,b)=>
        (a.first_publish_year || Infinity) -
    (b.first_publish_year || Infinity)
);
    }
    displayBooks(sortedBooks);
});

fetchBooks("education");