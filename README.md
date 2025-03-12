# Short URL API

This is a simple URL shortener built with Flask and SQLite.

## How to Run

1. Clone the repository:
   
   git clone https://github.com/janet850305/short_url_test.git

2. cd short_url_test

3. Run the application:

    flask run
    or
    python app.py


# Docker Instructions
## To run the application in a Docker container:
```
docker pull your-dockerhub-username/short-url-api
docker run -p 5000:5000 your-dockerhub-username/short-url-api
```


API discribe:
1. Shorten a URL:

Request:
```
POST /shorten
Content-Type: application/json
{
  "original_url": "https://www.google.com.tw/?hl=zh_TW"
}
```
Response:
```
{
    "expriation_date": "Fri, 11 Apr 2025 22:03:25 GMT",
    "short_url": "hLiWzLvmuny0OYhrL34JyI",
    "success": true
}
```
2. Redirect to original URL:
```
GET /hLiWzLvmuny0OYhrL34JyI
```
