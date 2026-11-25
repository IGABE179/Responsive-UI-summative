#EduFind - Educational Resource Finder

## 1. Project Description

EduFind is an educational resource discovery application that helps students find books and learning materials from different subjects.

The application uses the Open Library API to retrievebook information and display it to users.

## 2. Problem Statement

Students sometimes find it difficult to discover educational books and learning materials.

EduFind provides a simple platform where students can searchh for books and explore learning resources.

## 3. Features

- Search for educational books.
- Search by title, author or keyword.
- Filter resources by subject.
- Sort books alphabetically.
- Sort books by publication year.
- Display book titles, authors, and publication years.
- View additional book book information through Open Library.
- Handle API errors and empty search results.
- Responsive design for mobile and desktop devices.

## 4. Technologies Used

- HTML5
- CSS3
- JavaScript
- Open Library Search API
- Git and GitHub

## 5. External API

This project uses the Open Library Search API.

API Documentation:
https://openlibrary.org/dev/docs/api/search

Website:
https://openlibrary.org/

Open Library provides public book information including titles, authors, publication years and covers.

Credit is given to the Open Library project for providing the book data used in EduFind.

## 6. How to Run Locally

1. Clone this repository:
git clone 
2. Open the project folder: 
cd Responsive-UI-summative
3. Open index.html in your browser.

You can also use the Live Server extension in Visual Studio Code.

## 7.Deployment

The application will be deployed on two web servers:

- web01
- web02

Nginx will serve the application files.

HAProxy will be configured on Lb01 to distribute incoming requests between the two application servers.

Detailed deployment commands, server configurations, and load balancing tests will be documented after deployment is completed.

## 8. Error Handling

The application handles: 

- Failed API requests.
- Internet connection problems
- Empty search results.
- Missing book information.
- Missing book covers.

## 9. Future Improvements

- Add favorite books.
- Add more subject categories.
- Implement API response caching.
- Improve search performance.
- Add advanced filtering options.

## 10. Author
 
Developed as a Summative assignment of Web Infrastructure.

