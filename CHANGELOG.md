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
- 403.html file to show custom 403 error  
  
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
