# Python and Data Centric Development Milestone Project 

This website is collection of over 35,000 quotes gather and organised based on author, book, categories and popularity. The website is a community by which users can store their favourite quotes,  books and authors. They can additionally share quotes with friends and comment on authors and books to express their opinions. Users can use the “mood” section so that they can discover favourite authors depending on how they feel.
This information is presented in an interactive, picturesque manner with a simple, easy on the eye design.

## UX
When designing this website, I followed the 5 levels of development, a well know web design process mentioned in Jesse James Garrett's book, The Elements of User Experience. The planning of each of these planes are to follow the same order as below with each plane aligning to the previous plane’s requirements. This ensures that the main objectives for the website identified in the Strategy plane aligns all the way through to the Surface Plane which identifies the actual features on the website.

- Strategy Plane
- Scope Plane
- Structure Plane
- Skeleton Plane
- Surface Plane
- Strategy Plane

### Strategy Plane

#### Project Objectives

- Allow for users to browse and discover quotes, authors and books.
- Allow for users to register an account and login.
- Provide users with the functionality to save their favourite quotes, authors and books so that they can revisit for inspiration at any time.
- Easy sharing platform for quotes, authors and books.
- Create a community whereby users can comment and share their thoughts on authors and books.

#### User Stories
- As a visitor, I would like to browse and discover quotes which interest me so that I can find inspiration.
- As a visitor, I would like to save my favourite quotes/authors/books so that I can view at a later stage.
- As a visitor, I would like to discover quotes which coincide with the current mood I am experiencing so that I can find inspiration.
- As a visitor, I would like to search quotes/authors/books from the database so that I can research quotes in the database depending on my specific interest.
- As a visitor, I would like to register and login so that I can view my favourite quotes/authors/books.

### Scope Plane

The scope plane ensures that the website sections align to the objects and that these don’t grow in number throughout the project.
Necessary sections which align to the project objectives and user stories mentioned in the Structure plane.
For this project we will include all phase 1 sections and omit phase 2 sections until a later sprint due to resource capacity.

#### Phase 1

The first phase of the website will consist of 10 pages.

- Home
- Mood
- Authors
- Books
- Log in
- Register
- Individual Author Page
- Individual Book Page
- Users Private Profile page
- Share Quote page

#### Phase 2

Phase 2 will consist of upgrading the current pages. This will include increasing the number of author pictures. Allow for user profile image uploads and other functionalities below.

- Users Public Profile page
  - Allow user to upload profile picture
- Quote based on whether
  - Deliver a quote to the user depending on the weather in their location. For example, if it’s sunny/rainy, search the “Happiness”/”Inspiration tag.
- Improve individual book images
  - I used to materialize books icon with a rotation of colours for phase 1 but for phase 2 I intend to implement actual book images to give a more realistic effect.
- Improve Author profile
  - Can be done with Author profile information and uploading a new collection with information such as Author, DOB, Nationality etc.
- Allow for users to add their own quotes
  - Improve and increase the quotes database by allowing users to add quotes to the database.

### Structure Plane

The Structure plane is focused on taking the content selected from the scope plane and outlining how to portray this from a design aspect.

#### Design Process

- Considering the website consists of a collection of text, many pages will contain images to encourage engagement.
- The quote boxes will be an important aspect as these will present the collection of texts to the users.
- I have chosen an indigo/Lavender colour as the primary colour featuring as the Navbar and footer.
- This colour is also used on buttons and icons throughout the site.
- For font, a standard black is used for the quotes and text. For H2’s a Navy is used which contrasts wells with the lavender and is attention grapping. Sub heading and info messages are a lighter, less intense blue.
- Other colours chosen for the book icons, I selected using trial and error from the mycolor  pallet below.
  - https://mycolor.space/?hex=%237986CB&sub=1
- The Mood Board, Books and Authors pages all contain landing images whereas the home page include a “quote of the day” in large 'EB Garamond' font. This is used to portray the website concept on the main landing page.
- Materialize icons are used throughout.

### Skeleton Plane

Once the sections and layout has been identified as in the previous planes, we can get started with the Skeleton Plane. The Skeleton Planes outlines the arrangement of each section on the website and the best way to design these are by creating wireframes. I initially drew these wireframes before creating using Balsamiq software.

### Surface Plane
The surface plane is the least conceptual plane and consists of the actual content and features on the website.

#### Features
- Navbar
  - A fixed Navbar with active classes so the user can tell what page they’re on. This renders for mobile with a slide out menu on the side
- Quote of the day
  - A Welcome Quote box to provide daily inspiration. The same styling is implemented for the share quote page.
- Search
  - Considering the size of the database we have implemented search options for the Quotes, Authors and Books page so users can explore by wording or locate exact authors, books or quotes.
- Form
  - To meet the community-based requirements such as login, register and comment, forms will be imperative to feed information to the database.
- Copy quote link
  - I created an instant copy to clipboard link using a materialize icon in the quote box. This will allow the user to share the link of the quote with their friends (weather they have registered or not.
- Favourite icon
  - I have implemented a bright yellow favourited icon using Font Awesome. This animates to a glowing yellow when checked. When checking, this also feeds the information to store this as the users favourite in the database.
  - “Toast” prompt messages also pop up to inform the user when added or removed. For logged out customers, it also informs the user with relevant information.
- Mood board
  - The mood board is the most interactive feature and great for users who don’t have any particular authors in mind and would like to stumble upon a treasure of quotes.
  - It consists of a welcome image and 16 options taken form the most frequently mentioned tags throughout the database.
  - When the user selects the “Generate Quotes” button, these tags search the database and return the most relevant quotes to these queries.
  - The user can go back and play around with the remaing tags.
- Mood board Carousel
  - The 16 options would look like overkill but this range of tags is necessary to ensure the search returns depth in the choice of quotes. For this reason, I included these tags on an interactive carousel (8 on each side) so the user can browse and select moods in an interactive manner.
  - The search logic behind this board is that the highlighted tags are fed into an index created in the quotes collection which returns results based on a text index for quote, author and tags.
- Search features
  - The user may have a specific Author, book or quote in mind, for this reason, we have included 3 different search bars throughout the website.
  - Quotes: This search bar is the on the homepage for the user, it returns results based on a text index for quote, author and tags.
  - Author: On the Author page this search bar returns results for based on a text index for author name only.
  - Book: On the Book page, this search bar returns results based on a text index for Book name only.
- Comment
  - In addition to the previously mentioned comments form, the comments section is visible at the bottom of the specified books page and the individual authors page which shows the posted comments.










