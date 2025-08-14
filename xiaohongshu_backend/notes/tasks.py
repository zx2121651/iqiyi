from celery import shared_task
import subprocess
import uuid
import tempfile
import os
from django.core.files.base import ContentFile
from .models import Note

@shared_task
def generate_thumbnail_task(note_id):
    """
    一个Celery任务，用于在后台为视频笔记生成缩略图。
    此任务与存储后端无关。
    """
    try:
        note_instance = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return f"Note with id {note_id} not found."

    if not note_instance.video or note_instance.post_type != Note.POST_TYPE_VIDEO:
        return f"Note with id {note_id} is not a video post or has no video."

    # 创建临时文件来处理视频和缩略图
    with tempfile.NamedTemporaryFile(suffix='.mp4') as temp_video_file:
        # 从存储中读取视频内容并写入临时文件
        with note_instance.video.open('rb') as video_stream:
            temp_video_file.write(video_stream.read())
            temp_video_file.flush()

        # 为输出的缩略图创建临时文件路径
        thumbnail_filename = f"{uuid.uuid4()}.jpg"
        temp_thumb_path = os.path.join(tempfile.gettempdir(), thumbnail_filename)

        try:
            # ffmpeg 命令现在作用于本地临时文件
            # The order of arguments can matter. -ss before -i is faster.
            command = [
                'ffmpeg',
                '-ss', '00:00:01',
                '-i', temp_video_file.name,
                '-vframes', '1',
                '-y',
                temp_thumb_path
            ]
            subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)

            # 读取生成的缩略图内容并保存到模型的ImageField
            with open(temp_thumb_path, 'rb') as thumb_file:
                thumbnail_content = ContentFile(thumb_file.read(), name=thumbnail_filename)
                note_instance.video_thumbnail.save(thumbnail_filename, thumbnail_content, save=True)

            return f"Successfully generated thumbnail for note {note_id}"

        except subprocess.TimeoutExpired:
            error_message = f"Thumbnail generation timed out for note {note_id}"
            print(error_message)
            return error_message
        except subprocess.CalledProcessError as e:
            error_message = f"Error generating thumbnail for note {note_id}: {e.stderr}"
            print(error_message)
            return error_message
        except Exception as e:
            error_message = f"An unexpected error of type {type(e).__name__} occurred for note {note_id}: {e}"
            print(error_message)
            return error_message
        finally:
            # 确保临时缩略图文件在任务结束时被删除
            if os.path.exists(temp_thumb_path):
                os.remove(temp_thumb_path)
