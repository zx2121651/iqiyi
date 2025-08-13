# 仿小红书 App 后端服务

本项目是“仿小红书App”的后端服务，采用 Python 的 Django 框架开发。实现了模块化的开发方式，具备清晰的项目结构和完整的用户认证功能。

## 项目特色

- **前后端分离**: 提供 RESTful API，方便与前端（Web、iOS、Android）对接。
- **模块化开发**: 应用功能高度解耦，易于维护和扩展。
- **JWT认证**: 使用 JSON Web Tokens 进行无状态的用户认证。
- **强大的后台**: 自带 Django Admin 后台，方便内容和用户管理。
- **详细文档**: 提供详细的设计和API文档。

## 技术栈

- **后端框架**: Django
- **API框架**: Django REST Framework (DRF)
- **数据库**: PostgreSQL (开发阶段使用 SQLite)
- **用户认证**: djangorestframework-simplejwt (JWT)

## 环境搭建与运行

1.  **克隆项目**
    ```bash
    git clone <your-repo-url>
    cd xiaohongshu-backend
    ```

2.  **创建并激活虚拟环境**
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows use `venv\Scripts\activate`
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```
    *注意: `requirements.txt` 文件需要手动生成: `pip freeze > requirements.txt`*

4.  **应用数据库迁移**
    ```bash
    python manage.py migrate
    ```

5.  **创建超级用户 (用于访问Admin后台)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **运行开发服务器**
    ```bash
    python manage.py runserver
    ```
    服务将在 `http://127.0.0.1:8000/` 上运行。

## 下一步

请查阅 `docs/` 目录下的文档，了解更多关于系统设计和API的详细信息。
