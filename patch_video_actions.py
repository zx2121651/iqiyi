import re

with open('iqiyi-backend/src/routes/video.ts', 'r', encoding='utf-8') as f:
    content = f.read()

actions_route = """
// 发表评论
router.post('/comment', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ code: 401, message: 'Unauthorized', data: null });
  }
  const userId = authHeader.split(' ')[1];
  const { videoId, content } = req.body;

  if (!videoId || !content) {
    return res.status(400).json({ code: 400, message: 'videoId and content are required', data: null });
  }

  const commentId = 'c_' + Date.now();
  try {
    await run('INSERT INTO comments (id, videoId, userId, content, likeCount) VALUES (?, ?, ?, ?, 0)', [commentId, videoId, userId, content]);
    res.json({
      code: 200,
      message: 'success',
      data: { id: commentId }
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

// 视频点赞 (仅模拟增加点赞数)
router.post('/like', async (req, res) => {
  const { videoId } = req.body;
  if (!videoId) {
    return res.status(400).json({ code: 400, message: 'videoId is required', data: null });
  }

  try {
    await run('UPDATE videos SET likeCount = likeCount + 1 WHERE id = ?', [videoId]);
    const video = await get('SELECT likeCount FROM videos WHERE id = ?', [videoId]);
    res.json({
      code: 200,
      message: 'success',
      data: { likeCount: video ? video.likeCount : 0 }
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

export default router;
"""

content = content.replace("import { get, query } from '../db/db';", "import { get, query, run } from '../db/db';")
content = content.replace("export default router;", actions_route)

with open('iqiyi-backend/src/routes/video.ts', 'w', encoding='utf-8') as f:
    f.write(content)
