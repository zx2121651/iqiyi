# API 文档 (V1)

本文档详细描述了“仿小红书App”后端第一阶段可用的API接口。

**API 根路径**: `/api/v1/`

---

## 1. 用户认证 (Authentication)

### 1.1 用户注册

- **Endpoint**: `auth/register/`
- **Method**: `POST`
- **Description**: 创建一个新用户。
- **Authentication**: 无需认证。
- **Request Body**: `application/json`

**Parameters**:

| 字段名 | 类型 | 是否必须 | 说明 |
| :--- | :--- | :--- | :--- |
| `username` | string | 是 | 用户的登录名，必须唯一。 |
| `password` | string | 是 | 用户密码，长度建议8位以上。 |
| `phone_number` | string | 否 | 用户的手机号，必须唯一。 |
| `nickname` | string | 否 | 用户的昵称。 |

**Success Response (201 Created)**:

```json
{
    "username": "newuser",
    "phone_number": "13800138000",
    "nickname": "小红薯"
}
```
*注意: 响应中不包含密码。*

---

### 1.2 用户登录 (获取Token)

- **Endpoint**: `auth/login/`
- **Method**: `POST`
- **Description**: 使用用户名和密码登录，成功后返回 access 和 refresh token。
- **Authentication**: 无需认证。
- **Request Body**: `application/json`

**Parameters**:

| 字段名 | 类型 | 是否必须 | 说明 |
| :--- | :--- | :--- | :--- |
| `username` | string | 是 | 用户的登录名。 |
| `password` | string | 是 | 用户密码。 |

**Success Response (200 OK)**:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzQwOTg2NywiaWF0IjoxNzE2ODg1MDY3LCJqdGkiOiI5Zj...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2ODg1MzY3LCJpYXQiOjE3MTY4ODUwNjcsImp0aSI6IjU0..."
}
```
*`access` token 用于后续请求的认证, `refresh` token 用于在 access token 过期后获取新的 token。*

---

### 1.3 刷新 Access Token

- **Endpoint**: `auth/token/refresh/`
- **Method**: `POST`
- **Description**: 使用 refresh token 获取一个新的 access token。
- **Authentication**: 无需认证。
- **Request Body**: `application/json`

**Parameters**:

| 字段名 | 类型 | 是否必须 | 说明 |
| :--- | :--- | :--- | :--- |
| `refresh` | string | 是 | 从登录接口获取到的 refresh token。 |

**Success Response (200 OK)**:

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2ODg1MzY3LCJpYXQiOjE3MTY4ODUwNjcsImp0aSI6IjU0..."
}
```

---

## 2. 用户信息 (Users)

### 2.1 获取当前用户信息

- **Endpoint**: `users/me/`
- **Method**: `GET`
- **Description**: 获取当前登录用户的详细信息。
- **Authentication**: **需要认证**。请求头中必须包含 `Authorization: Bearer <access_token>`。

**Parameters**: 无

**Success Response (200 OK)**:

```json
{
    "id": 1,
    "username": "testuser",
    "nickname": "我的昵称",
    "avatar": null,
    "bio": "这是我的个人简介。",
    "phone_number": "13912345678"
}
```

---

## 3. 笔记 (Notes)

### 3.1 获取笔记列表

- **Endpoint**: `notes/`
- **Method**: `GET`
- **Description**: 获取所有笔记的分页列表。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**:
  ```json
  {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
          {
              "id": 1,
              "author_username": "testuser",
              "title": "My First Note",
              "content": "This is the content of my first note.",
              "created_at": "2023-10-27T10:00:00Z",
              "updated_at": "2023-10-27T10:00:00Z",
              "images": [
                  {
                      "id": 1,
                      "image": "/media/notes_images/my_image.jpg",
                      "uploaded_at": "2023-10-27T10:00:00Z"
                  }
              ]
          }
      ]
  }
  ```

### 3.2 创建一篇新笔记

- **Endpoint**: `notes/`
- **Method**: `POST`
- **Description**: 创建一篇新的笔记，可以同时上传图片。
- **Authentication**: **需要认证**.
- **Request Body**: `multipart/form-data`

**Parameters**:

| 字段名 | 类型 | 是否必须 | 说明 |
| :--- | :--- | :--- | :--- |
| `title` | string | 是 | 笔记的标题。 |
| `content`| string | 是 | 笔记的正文内容。 |
| `uploaded_images` | list of files | 否 | 一个或多个图片文件。 |

**Success Response (201 Created)**:
  ```json
  {
      "id": 2,
      "author_username": "newuser",
      "title": "A New Note",
      "content": "Content of the new note.",
      "created_at": "2023-10-27T11:00:00Z",
      "updated_at": "2023-10-27T11:00:00Z",
      "images": [
          {
              "id": 2,
              "image": "/media/notes_images/new_image.jpg",
              "uploaded_at": "2023-10-27T11:00:00Z"
          }
      ]
  }
  ```

### 3.3 获取单篇笔记详情

- **Endpoint**: `notes/<id>/`
- **Method**: `GET`
- **Description**: 根据ID获取一篇笔记的详细信息。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**: (响应体与列表中的单个对象结构相同)

### 3.4 更新一篇笔记

- **Endpoint**: `notes/<id>/`
- **Method**: `PUT` / `PATCH`
- **Description**: 更新一篇笔记。只有笔记的作者才能更新。
- **Authentication**: **需要认证**.
- **Request Body**: `application/json` (如果只更新文本字段) 或 `multipart/form-data` (如果需要添加图片)。

**Parameters**: 与创建时相同。

**Success Response (200 OK)**: (响应体与列表中的单个对象结构相同)

### 3.5 删除一篇笔记

- **Endpoint**: `notes/<id>/`
- **Method**: `DELETE`
- **Description**: 删除一篇笔记。只有笔记的作者才能删除。
- **Authentication**: **需要认证**.
- **Success Response**: `204 No Content`
