# Blog API Backend

A REST API for blog built using Django Rest Framework

## Installation

### Requirements
- Python
- Django
- Django rest Framework

### Quickstart
- Clone the repo.  
    ```bash
    git clone https://github.com/sarahoushmand/blog-api.git
    ```

- Inside the backend folder, make a virtual environment and activate it 
    ```bash
    cd blog
    ```

- Install requirements from requirements.txt
    ```
    pip install -r requirements.txt
    ```

- Makemigrations and migrate the project
    ```
    python manage.py makemigrations && python manage.py migrate
    ```

- Create a superuser
    ```
    python manage.py createsuperuser
    ```

- Runserver
    ```
    python manage.py runserver
    ```


## API
<details>
<summary> User model </summary> 

- User:
    - username: string(unique),
    - email: email,
    - password: string(min 8 chars)

</details>

<details>
<summary> Post Model </summary>

- Post:
    - id: Post id(read only),
    - title: string,
    - author: user-id(read only),
    - content: string,
    - selected_image: image(optional),
    - state: choiceField(draft or released)
    - release_date: datetime
    - created_at: datetime(read only)
    - updated_at: datetime(read only)
    - images: relation to image model
    - badges: relation to badge model
</details>

<details>
<summary>Image Model </summary>

- Image:
    - id: Image id(read only),
    - image: image,
</details>

<details>
<summary>Badge Model </summary>

- Badge:
    - id: Badge id(read only),
    - name: str,
</details>



### Endpoints

Explanation of endpoints:

| Function                                                                                               | REQUEST    | Endpoint                                                | Authorization | form-data                                 |
|--------------------------------------------------------------------------------------------------------|------------|---------------------------------------------------------|---------------|-------------------------------------------|
| Get token (For Author)                                                                                        | GET       | http://127.0.0.1:8000/author/get-token/                   | Not Required  | username, password                 |
| Update Author profile                                                                    | PUT        | http://127.0.0.1:8000/author/update-profile                             | Authtoken    |   age, about, image                                        |
| Returns a List of Authors                                                                 | GET        | http://127.0.0.1:8000/author/                    | Not Required    |                                           |
| Create a post for blog                                                                  | POST | http://127.0.0.1:8000/post/create/                    | Authtoken    |     post model fields                                      |
| Update or Delete a post                                                                                | PUT, DELETE     | http://127.0.0.1:8000/post/{int:id}/                    | Authtoken    |      post model fields                                     |
| Returns a List of posts                                                                                                    |   GET           |      http://127.0.0.1:8000/post/                                                   |        Not Required        |                                           |
| Returns a list of Badges                                                                | GET        | http://127.0.0.1:8000/post/badges/                            | Not Required  |                                           |



### Test

Just create one Test!

```bash
 python manage.py test
```
