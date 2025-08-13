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
              "post_type": "video",
              "video": "/media/notes_videos/my_video.mp4",
              "video_thumbnail": "/media/videos_thumbnails/my_thumbnail.jpg",
              "images": [],
              "likes_count": 1,
              "comments_count": 0,
              "is_liked": true,
              "is_favorited": false
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
| `uploaded_images` | list of files | 条件 | 图文笔记需要。与 `video` 二选一。 |
| `video` | file | 条件 | 视频笔记需要。与 `uploaded_images` 二选一。 |

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

---

## 4. 交互 (Interactions)

### 4.1 获取笔记的评论列表

- **Endpoint**: `notes/<note_id>/comments/`
- **Method**: `GET`
- **Description**: 获取某篇笔记下的所有顶层评论（回复会在评论对象中嵌套显示）。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**:
  ```json
  [
      {
          "id": 1,
          "author_username": "commenter",
          "content": "This is a great note!",
          "created_at": "2023-10-27T12:00:00Z",
          "parent": null,
          "replies": [
              {
                  "id": 2,
                  "author_username": "original_poster",
                  "content": "Thanks!",
                  "created_at": "2023-10-27T12:05:00Z"
              }
          ]
      }
  ]
  ```

### 4.2 创建新评论

- **Endpoint**: `notes/<note_id>/comments/`
- **Method**: `POST`
- **Description**: 为一篇笔记添加新评论。如果提供了 `parent` 字段，则为创建回复。
- **Authentication**: **需要认证**.
- **Request Body**: `application/json`

**Parameters**:

| 字段名 | 类型 | 是否必须 | 说明 |
| :--- | :--- | :--- | :--- |
| `content` | string | 是 | 评论的内容。 |
| `parent` | integer | 否 | 父评论的ID，用于回复。 |

**Success Response (201 Created)**: (响应体与列表中的单个对象结构相同)

### 4.3 删除评论

- **Endpoint**: `comments/<comment_id>/`
- **Method**: `DELETE`
- **Description**: 删除一条评论。只有评论的作者才能删除。
- **Authentication**: **需要认证**.
- **Success Response**: `204 No Content`

### 4.4 点赞/取消点赞笔记

- **Endpoint**: `notes/<note_id>/like/`
- **Method**: `POST`
- **Description**: 切换对某篇笔记的点赞状态。第一次请求为点赞，第二次为取消点赞。
- **Authentication**: **需要认证**.
- **Success Response**:
    - `201 Created` (点赞成功时)
    - `204 No Content` (取消点赞成功时)

### 4.5 收藏/取消收藏笔记

- **Endpoint**: `notes/<note_id>/favorite/`
- **Method**: `POST`
- **Description**: 切换对某篇笔记的收藏状态。第一次请求为收藏，第二次为取消收藏。
- **Authentication**: **需要认证**.
- **Success Response**:
    - `201 Created` (收藏成功时)
    - `204 No Content` (取消收藏成功时)

---

## 5. 用户 (Users)

### 5.1 获取当前用户信息 (`/me`)

- **Endpoint**: `users/me/`
- **Method**: `GET`
- **Description**: 获取当前登录用户的个人信息。
- **Authentication**: **需要认证**。
- **Success Response (200 OK)**:
  ```json
  {
    "id": 1,
    "username": "currentuser",
    "nickname": "My Nickname",
    "avatar": null,
    "bio": "My bio here.",
    "phone_number": "13800138000",
    "followers_count": 10,
    "following_count": 5,
    "is_following": false
  }
  ```

### 5.2 获取指定用户公开主页

- **Endpoint**: `users/<id>/`
- **Method**: `GET`
- **Description**: 获取指定ID用户的公开主页信息，包含其发布的笔记列表。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**:
  ```json
  {
    "id": 2,
    "username": "otheruser",
    "nickname": "Other's Nickname",
    "avatar": null,
    "bio": "Bio of other user.",
    "phone_number": null,
    "followers_count": 25,
    "following_count": 15,
    "is_following": true,
    "notes": [
        {
            "id": 10,
            "author_username": "otheruser",
            "title": "A great note",
            "content": "...",
            "likes_count": 150,
            "...": "..."
        }
    ]
  }
  ```

### 5.3 关注/取消关注用户

- **Endpoint**: `users/<id>/follow/`
- **Method**: `POST`
- **Description**: 切换对指定ID用户的关注状态。
- **Authentication**: **需要认证**。
- **Success Response**:
    - `201 Created` (关注成功时)
    - `204 No Content` (取消关注成功时)

### 5.4 获取粉丝列表

- **Endpoint**: `users/<id>/followers/`
- **Method**: `GET`
- **Description**: 获取指定ID用户的粉丝列表。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**: (返回一个 `UserSerializer` 序列化的用户列表)

### 5.5 获取关注列表

- **Endpoint**: `users/<id>/following/`
- **Method**: `GET`
- **Description**: 获取指定ID用户正在关注的用户列表。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**: (返回一个 `UserSerializer` 序列化的用户列表)

---

## 6. 信息流 (Feeds)

### 6.1 获取“关注”信息流

- **Endpoint**: `feed/following/`
- **Method**: `GET`
- **Description**: 获取当前用户所关注的人发布的笔记列表，按时间倒序排列。
- **Authentication**: **需要认证**。
- **Success Response (200 OK)**: (返回一个 `NoteSerializer` 序列化的笔记分页列表)

### 6.2 获取“发现”信息流

- **Endpoint**: `feed/explore/`
- **Method**: `GET`
- **Description**: 获取平台上的所有笔记，用于“发现”或“广场”功能，按时间倒序排列。
- **Authentication**: 无需认证。
- **Success Response (200 OK)**: (返回一个 `NoteSerializer` 序列化的笔记分页列表)

---

## 7. 搜索 (Search)

### 7.1 搜索笔记

- **Endpoint**: `search/notes/`
- **Method**: `GET`
- **Description**: 根据关键词搜索笔记的标题和内容。
- **Authentication**: 无需认证。
- **Query Parameters**:
    - `q` (string, required): 搜索的关键词。
- **Success Response (200 OK)**: (返回一个 `NoteSerializer` 序列化的笔记分页列表)

### 7.2 搜索用户

- **Endpoint**: `search/users/`
- **Method**: `GET`
- **Description**: 根据关键词搜索用户的用户名和昵称。
- **Authentication**: 无需认证。
- **Query Parameters**:
    - `q` (string, required): 搜索的关键词。
- **Success Response (200 OK)**: (返回一个 `UserSerializer` 序列化的用户列表)

---

## 8. 通知 (Notifications)

### 8.1 获取通知列表

- **Endpoint**: `notifications/`
- **Method**: `GET`
- **Description**: 获取当前登录用户的通知列表。
- **Authentication**: **需要认证**。
- **Query Parameters**:
    - `unread` (boolean, optional): 如果为 `true`，则只返回未读通知。
- **Success Response (200 OK)**:
  ```json
  [
      {
          "id": 1,
          "sender": { "id": 2, "username": "otheruser", "...": "..." },
          "verb": "follow",
          "action_object": { "id": 2, "username": "otheruser", "...": "..." },
          "is_read": false,
          "created_at": "2023-10-28T10:00:00Z"
      },
      {
          "id": 2,
          "sender": { "id": 3, "username": "anotheruser", "...": "..." },
          "verb": "like",
          "action_object": { "id": 5, "title": "My Note Title" },
          "is_read": true,
          "created_at": "2023-10-28T09:00:00Z"
      }
  ]
  ```

### 8.2 将单条通知标记为已读

- **Endpoint**: `notifications/<id>/mark-as-read/`
- **Method**: `POST`
- **Description**: 将指定的单条通知标记为已读。
- **Authentication**: **需要认证**。
- **Success Response (200 OK)**:
  ```json
  {
      "status": "notification marked as read"
  }
  ```

### 8.3 将所有通知标记为已读

- **Endpoint**: `notifications/mark-all-as-read/`
- **Method**: `POST`
- **Description**: 将当前用户的所有未读通知一键标记为已读。
- **Authentication**: **需要认证**。
- **Success Response (200 OK)**:
  ```json
  {
      "status": "all notifications marked as read"
  }
  ```

---

## 9. 私信 (Messaging)

### 9.1 获取会话列表

- **Endpoint**: `conversations/`
- **Method**: `GET`
- **Description**: 获取当前登录用户的所有私信会话列表，按最新消息时间排序。
- **Authentication**: **需要认证**。
- **Success Response (200 OK)**:
  ```json
  [
      {
          "id": 1,
          "other_participant": {
              "id": 2,
              "username": "otheruser",
              "nickname": "Other's Nickname",
              "avatar": "/media/avatars/other.jpg"
          },
          "last_message": {
              "text": "Hi, User1!",
              "created_at": "2023-10-28T14:00:00Z",
              "is_read": false
          },
          "updated_at": "2023-10-28T14:00:00Z"
      }
  ]
  ```

### 9.2 获取会话的历史消息

- **Endpoint**: `conversations/<conversation_id>/messages/`
- **Method**: `GET`
- **Description**: 获取指定会话中的消息列表，按时间正序排列。获取时，属于对方的消息会自动标记为已读。
- **Authentication**: **需要认证**。
- **Success Response (200 OK)**:
  ```json
  [
      {
          "id": 1,
          "sender": { ... },
          "text": "Hello!",
          "created_at": "2023-10-28T13:59:00Z",
          "is_read": true,
          "is_me": true
      },
      {
          "id": 2,
          "sender": { ... },
          "text": "Hi, User1!",
          "created_at": "2023-10-28T14:00:00Z",
          "is_read": true,
          "is_me": false
      }
  ]
  ```

### 9.3 发送消息

- **Endpoint**: `conversations/<conversation_id>/messages/`
- **Method**: `POST`
- **Description**: 在一个已存在的会话中发送一条新消息。
- **Authentication**: **需要认证**。
- **Request Body**: `{"text": "Your message here"}`
- **Success Response (201 Created)**: (返回新创建的 Message 对象)

### 9.4 发起新会话并发送第一条消息

- **Endpoint**: `users/<recipient_id>/messages/`
- **Method**: `POST`
- **Description**: 与指定用户发起一个新的会话（如果会话已存在，则直接使用现有会话）并发送第一条消息。
- **Authentication**: **需要认证**。
- **Request Body**: `{"text": "Your first message"}`
- **Success Response (201 Created)**: (返回新创建的 Message 对象)
