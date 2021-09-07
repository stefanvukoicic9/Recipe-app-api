# Recipe-app-api
## Setup
  - Run the following commands
  ```bash
    git clone https://github.com/stefanvukoicic9/Recipe-app-api.git
    cd Recipe-app-api
    docker-compose run --rm app sh -c "python manage.py makemigrations"
    docker-compose run --rm app sh -c "python manage.py migrate"
    docker-compose -f docker-compose.yml up --build -d
  ```
  
  - create super user
  
        docker-compose run --rm app sh -c "python manage.py createsuperuser"
        
  - Import Postman collection (Recipe_app_api.postman_collection.json) into the Postman
  
  - Test implemented endpoint
  
    - signin
    
        url:
        
            127.0.0.1:8000/api/user/signin/

         method: POST

         data: 


           {
          "first_name": string,
          "last_name": string,
          "email": string,
          "password": string
          }
          
          
    - log in

         url:
         
          127.0.0.1:8000/api/user/login/
        
         
          method: POST

          data:
          
         
            {
            "username": string,
            "password": string
            }
          
          
    - create ingredient
   
          url:
          
          
              127.0.0.1:8000/api/recipe/ingredients/
          
          
          method: Post

          data:
          
         
            {
              "name": string
            }
          
          
    - create recipe
   
          url:
          
              127.0.0.1:8000/api/recipe/recipe/
              
          method: Post

          data:
          
            {
              "name": string,
              "text": string,
              "price": Decimal,
              "ingredients": [
                Integer
              ]
            }
          
          
    - reating recipe
   
        url:
        
        
            127.0.0.1:8000/api/recipe/rate_recipe/
        
        
        method: Post

        data:
        
          {
            "recipe": Recipe object id(pk),
            "assessment": Number between 1 and 5
          }
        
        
    - list all recipes
   
        url:
        
        
            127.0.0.1:8000/api/recipe/recipe_list/
        
        
        method: Get
        
        url params: 
        
              127.0.0.1:8000/api/recipe/recipe/?name=string
              127.0.0.1:8000/api/recipe/recipe/?text=string
              127.0.0.1:8000/api/recipe/recipe/ingredients=array_id_ingredinets
              127.0.0.1:8000/api/recipe/recipe/?name=string&text=string&ingredients=array_id_ingredinets
      
    - list owner recipes
   
        url:
        
        
            127.0.0.1:8000/api/recipe/recipe/
       
        
        method: Get 
        
        filter: name, text and Ingredients
        url params: 
        
              127.0.0.1:8000/api/recipe/recipe/?name=string
              127.0.0.1:8000/api/recipe/recipe/?text=string
              127.0.0.1:8000/api/recipe/recipe/ingredients=array_id_ingredinets
              127.0.0.1:8000/api/recipe/recipe/?name=string&text=string&ingredients=array_id_ingredinets
      
    - top 5 userd ingredients
   
        url:
        
        
          127.0.0.1:8000/api/recipe/topingredients/
        
        
        method: Get 
## API documentation
  Generated at http://http://localhost:8000
      
## Entities
  - User
    * Email
    * Last Name
    * First Name

  - Owner
    * User (Foreign Key)
    * city (max length= 255, null, blank)
    * state (max length= 255, null, blank)
    * photo (max length= 255, null, blank)
    * linkedin (max length= 255, null, blank)
    * location (max length= 255, null, blank)
    * employment_domain (max length= 255, null, blank)
    * employment_name (max length= 255, null, blank)
    * employment_area (max length= 255, null, blank)
    * employment_role (max length= 255, null, blank)
    * employment_seniority (max length= 255, null, blank)

  - Ingredient
    * User (Foreign Key)
    * name (max length= 255)
  
  - Recipe
    * User (Foreign Key)
    * name (max length= 255)
    * text (max length= 255)
    * price (decimal, max digits=5, decimal places=2)
    * ingredients (Array Ingredient ids)
   
  - RateRecipe
    * User (Foreign Key)
    * Recipe (Foreign Key)
    * assessment (Number, between 1 and 5)
    
## Docker compose commands
    docker-compose up -V
    docker-compose down
    
## Testing
    docker-compose run --rm app sh -c "python manage.py test"
    
## Technologies used
  - Python
  - Django rest framework
