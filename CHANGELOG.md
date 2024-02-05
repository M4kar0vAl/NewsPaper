## 05.02.2024

### Added

- Logging configuration
  - if `DEBUG = True`:
    - messages logged to console
  - if `DEBUG = False`:
    - INFO messages logged to file `general.log` and sent to admins email if message level is ERROR or higher
  - regardless of `DEBUG` setting:
    - ERROR and higher messages logged to file `errors.log`
    - security messages logged to file `security.log`
  - `.log` files live in `logs` directory in project's working directory

## 27.01.2024

### Changed

- `sqlite3` db --> `PostgreSQL` db
- moved all data to a new db
- updated `.env`

## 20.01.2024

### Added

- `deleteposts` command that takes one or more category names as argument and deletes all posts in these categories
- On admin panel:
  - models now show more information about their objects
  - added search and filters to models
  - added `Update rating` action to Author model
  - added `Nullify rating` action to Post, Author and Comment models

## 30.12.2023

### Added

- filesystem caching for:
  - [home](http://127.0.0.1:8000/news/) page for 1 min
  - post detail page until it changes
  - navbar for logged in users for 100 sec
  - [subscriptions](http://127.0.0.1:8000/news/subscriptions) page until it changes

### Fixed

- categories dropdown not overlapping next div
- error that occured when not logged in user tried to get pages with categories dropdowns

## 27.12.2023  
  
### Added  

- "Clear filters" button on [search](http://127.0.0.1:8000/news/search) page which shows all posts  
- custom filter "is_subscribed" to check whether the user subscribed on category or not

### Changed  
  
- list of posts now shown as divs not table  
- for each post categories are shown  
- shown categories are dropdowns with:  
  - "Subscribe"/"Unsubscribe" button depending on whether user unsubscribed or subscribed to this category  
  - "Search this category" button which redirects on [search](http://127.0.0.1:8000/news/search) page and applies filter on this category
- filter on [search](http://127.0.0.1:8000/news/search) page now can filter by multiple categories  
- forms look better  
- every post in list of posts now shows 50 words as preview

### Fixed

- newsletter when new post added now works as intended (emails send only when new post created and not when changed existing one)  
- number of posts shown now takes pagination into account and displays correct value  

## 22.12.2023  
  
### Added  
  
- established a connection with Redis to use it as message broker  
- configured Celery to use with Django  
  
### Changed  
  
- added 2 environment vriables required to connect to Redis db  
- made post add newsletter and weekly newsletter async  
  
## 20.12.2023  
  
### Added  
  
- Subscriptions page (can be ) where users can manage their subscriptions on post categories (uses Subscriber model)  
- "Subscriptions" button on navbar to access the subscriptions page  
- Newsletters:  
  - welcome letter upon user regstration
  - a letter with a link to the post for users subscribed to post categories when publishing a new post
  - Users subscribed to categories are sent emails with links to posts in these categories every week (can't run with server simultaneously yet)  
- _.env_example_ file containing environment variables' names that should be defined in _.env_ file in same direcory as _.env_example_  

## 14.12.2023  
  
### Changed  
  
- less hardcoding in news/views.py  
  
## 11.12.2023  
  
### Added  
  
- bootstarp core js  
  
### Changed  
  
- table with posts is looking better now
- renamed:  
  - "Изменить" --> "Change"
  - "Удалить" --> "Delete" 
  
### Fixed  
  
- "Add" button is actually working now  
  
## 10.12.2023  
  
### Added  
  
- registration via:  
  - email + password  
  - yandex  
- all registered users now added to the authors group, which means they can:  
  - add posts  
  - edit posts  
- "Изменить" and "Удалить" buttons next to the post preview for users that have permission to change posts and delete posts respectively  
- On navbar:  
  - "Log out" button for logged in users  
  - "Sign up" and "Log in" buttons for not logged in users  
  - "Add" button, which supposed to be a dropdown button with selection of post type to add (not working yet)  
- _403.html_ file to show custom 403 error  
  
### Changed  
  
- renamed:  
  - "Поиск" --> "Search"  
  - "Главная" --> "Home"  
  - "Все новости" --> "All posts"  
  - "Всего статей" --> "Total posts"  
  - "Заголовок" --> "Heading"  
  - "Дата публикации" --> "Published"  
- moved "Search" button to the navigation bar 
  
### Removed  
  
- flatpages app
  
## 05.12.2023  

### Added  

- Filtration remains when page is switched  
- Pages for creating, editing and deleting posts  
- Search button on the main page leading to the search page  
  
### Changed  
  
- Filter form more human friendly now  
- Filter for obscene words more accurate now  
- Moved search to a separate page  
- Posts headings are now a hyperlinks leading to the page with a certain post  
- Post titles are now a different color and in bold  
- Responsive navbar: Home renamed to Главная and added a hyperlink leading to a main page with all posts  
  
## 02.12.2023  
  
### Added  
  
- Maximum of 1 post on one page.  
- Search form on main page with following filters:  
  * heading contains  
  * category  
  * publication date later than  
  
## 25.11.2023  
  
### Added  
  
- All posts displayed on main page. (url: localhost:8000/news)  
- Separate page for each post. (no hyperlinks yet) (url: localhost:8000/news/int:<post_id>)  
- Filter for obscene words defined in the program  
  
## 19.11.2023  
  
### Added  
  
- Created following models:  
  * Author  
  * Category  
  * Post  
  * PostCategory, representing ManyToMany relation between Post and Category  
  * Comment  
