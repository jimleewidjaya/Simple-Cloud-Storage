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

#### Not found

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Your Username and Password are Not Defined"
}
```

<br>

### Request 2: Logout

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/logout**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Logged out successfully!"
}
```
