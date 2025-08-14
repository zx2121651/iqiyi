from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'media'  # S3 bucket中的子目录
    file_overwrite = False # 不覆盖同名文件
    default_acl = 'public-read' # 文件默认权限为公开可读
