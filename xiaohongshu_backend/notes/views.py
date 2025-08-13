from rest_framework import viewsets, permissions
from django.db.models import Count
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnly

class NoteViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑笔记的 ViewSet。
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        重写 get_queryset 以添加注解和预取，优化性能。
        """
        return Note.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).prefetch_related(
            'images', 'likes', 'favorites'
        )

    def perform_create(self, serializer):
        """
        在创建新笔记时，将作者设置为当前登录的用户。
        如果是视频笔记，则为其生成缩略图。
        """
        note = serializer.save(author=self.request.user)
        if note.post_type == Note.POST_TYPE_VIDEO and note.video:
            generate_video_thumbnail(note)


import subprocess
import uuid
from django.conf import settings
from django.core.files.base import ContentFile

def generate_video_thumbnail(note_instance):
    """
    使用ffmpeg为视频文件生成缩略图
    """
    video_path = note_instance.video.path

    # 创建一个唯一的文件名
    thumbnail_filename = f"{uuid.uuid4()}.jpg"
    thumbnail_path = settings.MEDIA_ROOT / 'videos_thumbnails' / thumbnail_filename

    # 确保目录存在
    thumbnail_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # ffmpeg 命令: -i [输入文件] -ss [时间点] -vframes 1 [输出文件]
        # -ss 00:00:01 表示从视频的第1秒开始截图
        # -y 表示如果文件已存在则覆盖
        command = [
            'ffmpeg',
            '-i', str(video_path),
            '-ss', '00:00:01',
            '-vframes', '1',
            '-y',
            str(thumbnail_path)
        ]
        subprocess.run(command, check=True, capture_output=True)

        # 将生成的缩略图保存到模型的 ImageField
        # note_instance.video_thumbnail.save(thumbnail_filename, ContentFile(thumbnail_path.read_bytes()))
        # 上面的方法会重新读取文件，更直接的方式是直接设置name
        note_instance.video_thumbnail.name = f"videos_thumbnails/{thumbnail_filename}"
        note_instance.save(update_fields=['video_thumbnail'])

    except subprocess.CalledProcessError as e:
        # 处理ffmpeg执行失败的情况
        print(f"Error generating thumbnail for {video_path}: {e.stderr.decode()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
