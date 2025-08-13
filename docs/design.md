# 系统设计文档

本文档描述了“仿小红书App”后端项目的整体架构设计和数据库模型设计。

## 1. 系统架构

项目遵循经典的前后端分离架构模式。

- **后端 (本项目)**:
    - 基于 `Django` 和 `Django REST Framework` 构建。
    - 负责处理业务逻辑、数据存储、用户认证和提供 API 接口。
    - 通过 RESTful API 与前端进行数据交换，数据格式为 JSON。
- **前端 (未包含在此项目中)**:
    - 可以是 Web 应用 (如 React/Vue)、iOS App 或 Android App。
    - 负责用户界面的渲染和用户交互。
    - 通过消费后端提供的 API 来获取和提交数据。
- **数据库**:
    - 生产环境计划使用 `PostgreSQL`，它是一款功能强大且稳定的开源关系型数据库。
    - 开发环境为了便捷，使用 `SQLite`。
- **缓存 (未来规划)**:
    - 可以引入 `Redis` 作为缓存系统，用于缓存热点数据、降低数据库压力，并可用于实现如验证码、消息队列等功能。

## 2. 数据库模型设计 (V1)

### 用户模块 (`users.User`)

我们没有直接使用 Django 内置的 `User` 模型，而是通过继承 `AbstractUser` 创建了一个自定义的用户模型，以便未来灵活地添加更多字段。

**模型名称**: `User`
**所在App**: `users`

**字段详情**:

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `password` | CharField | 哈希后的密码 | 由 Django `AbstractUser` 提供 |
| `last_login` | DateTimeField | 最后登录时间 | 由 Django `AbstractUser` 提供 |
| `is_superuser` | BooleanField | 是否为超级用户 | 由 Django `AbstractUser` 提供 |
| `username` | CharField | 用户名 | 必填，唯一。用于登录。 |
| `first_name` | CharField | 名字 | Django 自带，本项目中可忽略 |
| `last_name` | CharField | 姓氏 | Django 自带，本项目中可忽略 |
| `email` | EmailField | 电子邮箱 | 可选 |
| `is_staff` | BooleanField | 是否为员工（可登录Admin） | 由 Django `AbstractUser` 提供 |
| `is_active` | BooleanField | 用户是否激活 | 由 Django `AbstractUser` 提供 |
| `date_joined` | DateTimeField | 注册时间 | 由 Django `AbstractUser` 提供 |
| `nickname` | CharField | **昵称** | 用户显示的名称，可以重复 |
| `avatar` | ImageField | **头像** | 指向用户上传的头像图片文件 |
| `phone_number` | CharField | **手机号** | 可选，唯一。可用于登录或找回密码。 |
| `bio` | TextField | **个人简介** | 用户的自我介绍 |

### 笔记模块 (`notes`)

#### 模型: `Note`

存储笔记/帖子的核心内容。

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `author` | ForeignKey | 作者 | 指向 `users.User` 模型，级联删除 |
| `title` | CharField | 标题 | 笔记的标题，最大长度200 |
| `content` | TextField | 内容 | 笔记的正文 |
| `post_type` | CharField | 帖子类型 | 'image' (图文) 或 'video' (视频) |
| `video` | FileField | 视频文件 | `post_type`为'video'时使用 |
| `video_thumbnail` | ImageField | 视频封面 | `post_type`为'video'时自动生成 |
| `created_at` | DateTimeField | 创建时间 | 自动记录创建时的时间 |
| `updated_at` | DateTimeField | 更新时间 | 自动记录每次更新时的时间 |

#### 模型: `NoteImage`

存储与笔记关联的图片。一个笔记可以有多张图片。

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `note` | ForeignKey | 所属笔记 | 指向 `notes.Note` 模型，级联删除 |
| `image` | ImageField | 图片文件 | 上传的图片 |
| `uploaded_at`| DateTimeField | 上传时间 | 自动记录上传时的时间 |


### 交互模块 (`interactions`)

#### 模型: `Comment` (评论)

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `author` | ForeignKey | 作者 | 指向 `users.User` 模型 |
| `note` | ForeignKey | 所属笔记 | 指向 `notes.Note` 模型 |
| `content` | TextField | 评论内容 | - |
| `parent` | ForeignKey | 父评论 | 指向自身，用于实现二级回复 |
| `created_at` | DateTimeField | 创建时间 | 自动记录 |

#### 模型: `Like` (点赞)

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `user` | ForeignKey | 点赞用户 | 指向 `users.User` 模型 |
| `note` | ForeignKey | 被点赞的笔记 | 指向 `notes.Note` 模型 |
| `created_at` | DateTimeField | 点赞时间 | 自动记录 |

*注: `user` 和 `note` 字段上设置了联合唯一约束。*

#### 模型: `Favorite` (收藏)

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `user` | ForeignKey | 收藏用户 | 指向 `users.User` 模型 |
| `note` | ForeignKey | 被收藏的笔记 | 指向 `notes.Note` 模型 |
| `created_at` | DateTimeField | 收藏时间 | 自动记录 |

*注: `user` 和 `note` 字段上设置了联合唯一约束。*

#### 模型: `Follow` (关注)

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `follower` | ForeignKey | 关注者 | 指向 `users.User` 模型 |
| `followed` | ForeignKey | 被关注者 | 指向 `users.User` 模型 |
| `created_at` | DateTimeField | 关注时间 | 自动记录 |

*注: `follower` 和 `followed` 字段上设置了联合唯一约束。*

### 通知模块 (`notifications`)

#### 模型: `Notification` (通知)

使用Django的 `ContentType` 框架来实现通用外键，使通知可以指向任何其他模型对象。

| 字段名 | 类型 | 说明 | 备注 |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | 主键 | Django 自动创建 |
| `recipient` | ForeignKey | 接收者 | 指向 `users.User`，通知的接收方 |
| `sender` | ForeignKey | 发送者 | 指向 `users.User`，触发通知的用户 |
| `verb` | CharField | 通知类型 | 如 'like', 'comment', 'follow' 等 |
| `action_object` | GenericForeignKey | 动作对象 | 指向触发动作的实例，如一个`Like`或`Comment`对象 |
| `is_read` | BooleanField | 是否已读 | 默认为 `False` |
| `created_at` | DateTimeField | 创建时间 | 自动记录 |


---

*（随着项目功能的增加，此文档将持续更新...）*
