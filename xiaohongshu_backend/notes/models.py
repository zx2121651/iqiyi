from django.db import models
from django.conf import settings

class Note(models.Model):
    """
    笔记/帖子模型
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="作者"
    )
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "笔记"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class NoteImage(models.Model):
    """
    笔记图片模型
    """
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="所属笔记"
    )
    image = models.ImageField(upload_to='notes_images/', verbose_name="图片")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    class Meta:
        verbose_name = "笔记图片"
        verbose_name_plural = verbose_name
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for note: {self.note.title} ({self.id})"
