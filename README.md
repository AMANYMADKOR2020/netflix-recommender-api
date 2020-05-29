# Netflix recommendation  API using flask and sklearn

you can use this api by json like the following:
```json
{
    "title": "Rocky"
}
```
with **post** request to the following endpoint 
:`/title`
example request
```bash
curl --location --request POST 'localhost:5000/title' \
--header 'Content-Type: application/json' \
--data-raw {
    "title": "Rocky"
}
```
output respond
```bash
[
  {
    "confidence": 0.56,
    "title": "Rocky III"
  },
  {
    "confidence": 0.55,
    "title": "Rocky II"
  },
  {
    "confidence": 0.5,
    "title": "Rocky IV"
  },
  {
    "confidence": 0.41,
    "title": "Rocky V"
  },
  {
    "confidence": 0.13,
    "title": "Spy Kids 3: Game Over"
  }
]
```
```bash
heroku link
```
