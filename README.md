
# URL Link Shortener

This is a URL Shortener, which leverages the use of fastapi for backend, mongodb for db, and redis for caching.

## Features

- MongoDB as DB
- Redis for caching
- Rate Limiting using IP Address


## Run Locally

Clone the project

```bash
  git clone https://github.com/soham-shee/URL-Link-Shortener.git
```

Go to the project directory

```bash
  cd URL-Link-Shortener
```

Install dependencies

```bash
  source venv/bin/activate
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn app.main:app --reload
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGO_URL`

`REDIS_URL`

`BASE_URL`

`RATE_LIMIT`


## API Reference

#### Generates the short link of URL

```https
  POST /shorten
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `json/string` |  Any URL |


#### Redirects to original URL

```https
  GET /{short_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `short_id`      | `string` |  short_id of the URL |


#### Shows the info of URL and it's short_id

```https
  GET /info/{short_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `short_id`      | `string` |  short_id of the URL |

## Documentation
From localhost (using Swagger) - 
[Documentation](/docs)


