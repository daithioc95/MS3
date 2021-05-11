# Python and Data Centric Development Milestone Project 
<img src="static/images/wireframes/ms3_responsive_image.JPG">

<a href="https://ms3-quotes.herokuapp.com/" target="_blank">Visit Website</a>
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
#### quotes.html (Homepage)
##### Desktop
<img src="static/images/wireframes/homepage_desktop.png">

##### Mobile
<img src="static/images/wireframes/homepage_mobile.png">

#### authors.html
##### Desktop
<img src="static/images/wireframes/author_desktop.png">

##### Mobile
<img src="static/images/wireframes/author_mobile.png">

#### books.html 
##### Desktop
<img src="static/images/wireframes/books_desktop.png">

##### Mobile
<img src="static/images/wireframes/books_mobile.png">

#### indiv_author.html 
##### Desktop
<img src="static/images/wireframes/individual_author_desktop.png">

##### Mobile
<img src="static/images/wireframes/individual_author_mobile.png">

#### profile.html 
##### Desktop
<img src="static/images/wireframes/user_profile_desktop.png">

##### Mobile
<img src="static/images/wireframes/user_profile_mobile.png">

#### mood.html 
##### Desktop
<img src="static/images/wireframes/mood_desktop.png">

##### Mobile
<img src="static/images/wireframes/mood_mobile.png">



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

### Technologies Used

- HTML Used to add content to the website.
- CSS Used to add structure and design to my site.
- JavaScript & jQuery Used for the below features
  - Favourite Star: AJAX was used to send information to the python function.
  - Toast Messages
  - Share Quote link
  - Mood Board Carousel Slider
- Python
  - Used python for the backend elements of the Website used to interact with the database and feed data depending on users’ interactions.
  - Python (Pymongo) was also used from a data analytics perspective for organising and manipulating the database.
- Mongo DB
  - Mongo DB was used to the upload the JSON format, store the database and also to connect with the python code to Create, Read, Update and Delete any necessary documents.
  - Also used to allow me to create and search indexes.
- Flask
  - Flask and the Jinja Templating Language is used to allow for the high volume of information feed through to the HTML template pages.
- Heroku
  - Heroku is used to deploy and host the website.
- Werkzeug
  - Used to securely encrypt and stored passwords.
- Materialize was used throughout the website to easily implement attractive and consistent designs. The Materialize Grid System was implemented throughout.
  - Navbar
  - Carousel
  - Forms
  - icons
- Font Awesome
  - Font Awesome was used for the favourite star animation
- Balsamiq
  - Used in the design process for wireframes.
- Pxhere, Pexels, Unsplash, Wikipedia 
  - Used for images and design inspiration.
- GitPod
  - Used to create, commit and push the HTML, CSS, JavaScript and Python changes for the website.
- GitHub
  - Used to store files and code.
- Stackoverflow
  - Used for problem solving to implement desired designs.
  - Used to gain better understanding of how I should approach the implementation of elements.
- W3Schools
  - Used to gather a theoretical knowledge of elements and effects.
- W3 HTML Validator
  - Used throughout the project to ensure I was following best practices with HTML code.
- Jigsaw CSS Validator
  - Used throughout the project to ensure I was following best practices with CSS code.
- JSHint JavaScript Validator
  - Used this GitPod extension throughout the project to ensure I was following best practices with JavaScript code.
- Colors.share
  - Used to extract colour schemes to trial.
- Kaggle
  - Used to browse and discover a wealth of databases
- Google Fonts
  - Used for font implementation and inspiration.
- http://techsini.com/
  - Used for Responsive Theme image at beginning of this ReadME.

### Testing

#### Testing User Stories
##### As a visitor, I would like to browse and discover quotes which interest me so that I can find inspiration.
- Go to the website homepage
- If logged in with no favourited quotes or logged out, you can browse and discover quotes in order of popularity.

<img src="static/images/user-story-testing/logged-out-quotes.JPG">

- If you are logged in and have favourited quotes you can click the “View Popular Quotes” link where you can discover quotes in order of popularity.
- This will provide 20 pages of inspirational quotes.
- The search box can also be used to enter terms to discover quotes depending on a specific category.

<img src="static/images/user-story-testing/logged-in-quotes.JPG">

- The Author name can also be selected to route you to a page showing quotes and books exclusively from this Author.
- Links to Similar Authors pages can also be chosen.

<img src="static/images/user-story-testing/indiv_author.JPG">
<img src="static/images/user-story-testing/indiv_author-similar-authors.JPG">

##### As a visitor, I would like to save my favourite quotes/authors/books so that I can view at a later stage.
- Adding Quote
  - When logged in and the user sees a quote they like, select the star at the top right-hand corner of the quote box.

<img src="static/images/user-story-testing/quote-box.JPG">

  - Select the star.
  - The star should glow yellow and a confirmation “Added to Favourites toast message should appear.

<img src="static/images/user-story-testing/quote-box-added-to-favs.JPG">

- Adding Author
  - When logged in and the user sees an Author they like, select the star at the right-hand corner of the quote box.

<img src="static/images/user-story-testing/author-box.JPG">

  - The star should glow yellow and a confirmation “Added to Favourites toast message should appear.

<img src="static/images/user-story-testing/author-box-added-to-favs.JPG">

- Adding Book
  - When logged in and the user sees a book they like, select the link to the book page
  - To the right-hand side of the main book icon the user cans select this star.
  - The star will glow yellow and a confirmation “Added to Favourites toast message should appear.

<img src="static/images/user-story-testing/indiv_book.JPG">

- View favourites
  - When the user is signed in, they can go to the ‘profile’ page to see their favourited items.
  - The first heading will show the users favourited quotes.
  - The second heading will show the users favourited Authors
  - The third heading will show the users favourited Books

<img src="static/images/user-story-testing/profile-quotes.JPG">

<img src="static/images/user-story-testing/profile-authors.JPG">

<img src="static/images/user-story-testing/profile-books.JPG">

##### As a visitor, I would like to discover quotes which coincide with the current mood I am experiencing so that I can find inspiration.
- Open the Mood page which can be located in the navbar.
- The mood page will show a series of tags on the mood board.
- The user can select the tags which coincide with their current mood.
- They can then select the “generate mood” button.

<img src="static/images/user-story-testing/mood-board.JPG">

- When they scroll down, they can find inspiration in the quotes shown to them.

<img src="static/images/user-story-testing/mood-board-generated.JPG">

##### As a visitor, I would like to search quotes/authors/books from the database so that I can research quotes in the database depending on my specific interest.
- The user can use the homepage search bar to search Quotes, tags and Authors.

<img src="static/images/user-story-testing/homepage-searchbar.JPG">

- The user can use the Authors.HTML search bar to search by Author only.

- The user can use the Books.HTML search bar to search by Book only.

<img src="static/images/user-story-testing/books-searchbar.JPG">

<img src="static/images/user-story-testing/searchbar-results.JPG">

##### As a visitor, I would like to register and login so that I can view my favourite quotes/authors/books.
- The user can register by selecting the register button in the navbar.

<img src="static/images/user-story-testing/navbar-register.JPG">

- They can enter relevant info into the form as per below.

<img src="static/images/user-story-testing/register-form.JPG">

- If the username is unique and the input passes the validation, they will see the alert as per below.

<img src="static/images/user-story-testing/register-success.JPG">

- As they select favourited quotes/authors/books they can view at a later stage on the profile page.

### Browsers
Tested and working consistently on the below browsers for desktop.

- Google Chrome
- Microsoft Edge
- Firefox

- Mobile version manually tested throughout using google chrome on Xiaomi 8 and One Plus 9.
- Tested on below screen sizes using Google Chrome developer tools.
  - Moto G4
  - Galaxy S5
  - Pixel 2
  - Pixel 2 XL
  - iPhone 5/SE
  - iPhone 6/7/8
  - iPhone 6/7/8 Plus
  - iPhone X
  - iPad
  - iPad Pro
  - Surface Duo
  - Galaxy Fold

- The project passed the below validation tests. Please see below links to view validation screenshot.

  - W3 HTML Validator: https://validator.w3.org/
    - Validation was complete by using URL to avoid false error flagging from Jinja templating l.anguage

   - <a href="static/images/user-story-testing/quotes-validator.JPG" target="_blank">quotes.html Validator success</a>
   - <a href="static/images/user-story-testing/authors-validator.JPG" target="_blank">authors.html Validator success</a>
   - <a href="static/images/user-story-testing/books-validator.JPG" target="_blank">books.html Validator success</a>
   - <a href="static/images/user-story-testing/indiv_author-validator.JPG" target="_blank">indiv_author.html Validator success</a>
   - <a href="static/images/user-story-testing/indiv_book-validator.JPG" target="_blank">indiv_book.html Validator success</a>
   - <a href="static/images/user-story-testing/mood-validator.JPG" target="_blank">mood.html Validator success</a>
   - <a href="static/images/user-story-testing/profile-validator.JPG" target="_blank">profile.html Validator success</a>
   - <a href="static/images/user-story-testing/login-validator.JPG" target="_blank">login.html Validator success</a>
   - <a href="static/images/user-story-testing/register-validator.JPG" target="_blank">register.html Validator success</a>

  - Jigsaw CSS Validator: https://validator.w3.org/
   - <a href="static/images/user-story-testing/css-validator.JPG" target="_blank">CSS Validator success</a>

- JSHint JavaScript Validator: https://jshint.com/

  - js jint gitpod extention highlights no JS errors

### Known bugs and issues
- W3 HTML Validator Warnings
  - All pages have a "Section lacks heading. Consider using h2-h6 elements to add identifying headings to all sections.". This is because flash messaged are stored in a section container and when the flash messages are not activated the H element in which they are stored in is not visible.
- Foreign Language Authors
  - When authors with Foreign Language (such as arabic) is selected the page returned "Not Found". I believe this is due to an incompatability between the foreign Language and the database. This is for a tiny minority of the websites pages, however I intend to investigate this issue at a later point.
- Narrow screen issue
  - Author Box: for some very narrow screens the author box can become distored and the text may overlap the image. I will make no changed from this as the mobile version benefits from having these images and it occurs on a iregularly small screen size.
- Share link
  - The share link should sit vertically below the star however this was difficult to position on a all screen sizes due to the differing nature of both items elements. I will revisit this at a later time.

### Data schemes
The database is stored and hosted by MongoDB.
The database was downloaded in JSON format from Kaggle, because being pasted to my data.txt file.
Addition cleaning and preparation of the data was complete by using the mongo.py file which include removing dupes, creating additional collections and separating the values.
For example the Author section contained the authors name and the book title (if any), so a split action was needed here before creating a new "book" key
The cluster used for this project contains 4 collections in total which are outlined below.


### Deployment 
#### Working with the local Copy
- Install the requirements based on librarys needed by using the pip3 install -r requirements.txt command.
- A data base will be needed to work off for a local file, this can be created using MongoDB by following the below instructions.
  - Create a MongoDB account.
  - Create a cluster.
  - Create 4 (self-explanitary) collections; authors, books, quotes and users.
  - Set values for these collections as content for the website.
- The environment variables will then be needed to allow the website to access the database. Please follow the below instrutions.
  - Create a .gitignore file.
  - Type "env.py" in the .gitignore file to ensure this is being ignored.
  - Create the env.py file.
  - This is where you can insert the following environment variables; IP, PORT, SECRET_KEY, MONGO_URI, MONGO_DBNAME.
- The app can now be ran via the terminal, create the app.py file and enter the command "python3 app.py" and run the app.


#### Heroku Deployment
- To deploy the project to Heroky a local workspace will be needed to ensure the Heroku can run the backend code.
- This can be done by using the command "pip3 freeze -- local > requirements.txt" which will populate the file convieniently to provide heroku with information on what needs to be installed.
- To ensure Heroku knows that the app.py file is the main file and entry for this project, the Procfile will be needed by logging the following command, "python app.py > Procfile"

- The next step involves creating a heroku account.
  - Go to heroku.com
  - Set up and account, create an app by following the instructions and enter any relevant information requested.
  - Deploy the app on Github to ensure any updates on github will link to Heroku (reducing the risk for discrepencies)
   - This can be done by selecting "Connect to GitHub" in the deploy tab and selecting the relevant repository. 
  - Locate the Config variables in the settings section, click "Reveal Config Vars".
  - Enter the previously mentioned variables which are present in the env.py file; IP, PORT, SECRET_KEY, MONGO_URI, MONGO_DBNAME
   - Ensure these values those of which present in the env.py file.
   - Also ensure the requirments.txt and Procfile are pushed into the live environment by using the below set of commands.
    - $ git add requirements.txt
    - $ git commit -m "Add requirements.txt"
    - $ git add Procfile
    - $ git commit -m "Add Procfile" 
 - Enable automatic deployments on Heroky by going to the deploy tab, go to Automatic deployments and select enable.
 Heroku now has the relevant packages to be linked and host the website. You can locate the apps URL by selecting "Open App" on the right hand corner of your Heroku account.

#### Cloning the project
If you wish to clone this project, action the following instructions.

1. On the repository "Code" tab, select the "Code" option at the top right.
2. Copy the URL provided in the HTTPS section.
3. Open the GitPod (or favoured environment) terminal and change to the desired directory for the clone to be located. 
4. Enter command "git clone" and paste the previously copied URL.
5. Hit enter and the clone will be created.

### Credits
All quotes content was taken from the below Kaggle database from user Amit Mittal.
https://www.kaggle.com/akmittal/quotes-dataset
Images
Please see below image log for all used images. All images were reduced in quality by using https://picresize.com/ for a smoother user loading and user experience.
***Image log***
#### Acknowledgements
- Materialize
  - Icons
  - Forms
  - Mood Carousel - https://materializecss.com/carousel.html#two!
  - Toast - https://materializecss.com/toasts.html
 - Carousel Buttons
  - Paco Cervantes - https://codepen.io/Paco_Cervantes/pen/ZLxKpj 
- Mood Board Buttons Hover
- Radial-out option
  - https://ianlunn.github.io/Hover/
- Toast
  - https://stackoverflow.com/questions/33566041/materialize-css-change-position-of-toast-dialog
- Font awesome
  - Favourite Star
   - https://www.tutorialrepublic.com/faq/how-to-check-a-checkbox-is-checked-or-not-using-jquery.php
- Quote of the data / Share Quote
  - Joe Hastings - https://codepen.io/JoeHastings/pen/MOdRVm 
- Quote Box / Author Box
  - Desktop - Tigran Sargsyan - https://codepen.io/tiggr/pen/MWyJJEz
  - Mobile - Chris Smith - https://codepen.io/chris22smith/pen/oQWavL - Animated Border 
  - Author Quote box desktop spacing - https://stackoverflow.com/questions/7537439/how-to-increment-a-variable-on-a-for-loop-in-jinja-template
- Pagination
  - https://stackoverflow.com/questions/58031816/how-to-display-active-bootstrap-pagination-using-jinja-conditional 
- Login, Register forms:
  - Mini Project
  - Materialize
- Colors.share
  - https://mycolor.space/?hex=%237986CB&sub=1
- Copy to clipboard share feature
 - https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
 - https://stackoverflow.com/questions/63033012/copy-the-text-to-the-clipboard-without-using-any-input
- Logged out favourite star
  - https://www.w3schools.com/js/tryit.asp?filename=tryjs_alert
  - Below 2 videos helped in sending data from jQuery AJAX to Python
   - https://www.youtube.com/watch?v=v2TSTKlrPwo
   - https://www.youtube.com/watch?v=XYx5sIbU8B4
- Comments
  - Letter icon - https://stackoverflow.com/questions/29980387/how-to-make-a-circle-around-a-letter/29980453













