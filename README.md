# Simple-Cloud-Storage

## Requests

1. Login
2. Logout
3. Upload File
4. View All Uploaded File (by Uploader)
5. Download File

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

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/logout**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Logged out successfully!"
}
```

<br>

### Request 3: Upload File

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/upload**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Files uploaded successfully!"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

<br>

### Request 4: View All Uploaded File (by uploader)

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/file**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "files": [
    {
      "id_file": 1,
      "filename": "168656837599997.jpg"
    },
    {
      "id_file": 2,
      "filename": "-934988497.pdf"
    },
    {
      "id_file": 3,
      "filename": "-934988497168656837599997.pdf"
    }
  ]
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

#### There are still no uploaded file

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "There are still no file"
}
```
