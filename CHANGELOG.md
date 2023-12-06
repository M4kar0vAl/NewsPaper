
05.12.2023  

### Added  

-Filtration remains when page is switched  
-Pages for creating, editing and deleting posts  
-Search button on the main page leading to the search page  
  
### Changed  
  
-Filter form more human friendly now  
-Filter for obscene words more accurate now  
-Moved search to a separate page  
-Posts headings are now a hyperlinks leading to the page with a certain post  
-Post titles are now a different color and in bold  
-Responsive navbar: Home renamed to Главная and added a hyperlink leading to a main page with all posts  
  
02.12.2023  
  
### Added  
  
-Maximum of 1 post on one page.  
- Search form on main page with following filters:  
  * heading contains  
  * category  
  * publication date later than  
  
25.11.2023  
  
### Added  
  
-All posts displayed on main page. (url: localhost:8000/news)  
-Separate page for each post. (no hyperlinks yet) (url: localhost:8000/news/int:<post_id>)  
-Filter for obscene words defined in the program  
  
19.11.2023  
  
### Added  
  
- Created following models:  
  * Author  
  * Category  
  * Post  
  * PostCategory, representing ManyToMany relation between Post and Category  
  * Comment  
