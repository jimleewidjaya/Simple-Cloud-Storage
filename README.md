# Simple-Cloud-Storage

## Requests

1. Login
2. Logout
3. Upload File
4. Download File

### Request 1: Login

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/login**</span>

```json
{
  "username": "janeDoe",
  "password": "QchpCEKOIsVhOXVj"
}
```

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Login Success!"
}
```

#### Success

![Not Found](https://badgen.net/badge/Not Found/404/red)

```json
{
  "status": "error",
  "message": "Your Username and Password are Not Defined"
}
```