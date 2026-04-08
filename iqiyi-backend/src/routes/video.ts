import { Router } from 'express';
import { get, query, run } from '../db/db';

const router = Router();

router.get('/detail', async (req, res) => {
  const id = req.query.id as string || "v1";
  try {
    const video = await get('SELECT * FROM videos WHERE id = ?', [id]);
    if (video) {
      video.isVip = video.isVip === 1;
      video.tags = JSON.parse(video.tags);
      res.json({
        code: 200,
        message: 'success',
        data: video,
      });
    } else {
      res.status(404).json({ code: 404, message: 'Video not found', data: null });
    }
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

router.get('/related', async (req, res) => {
  try {
    const related = await query('SELECT * FROM related_videos');
    res.json({
      code: 200,
      message: 'success',
      data: related,
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});


router.get('/comments', async (req, res) => {
  const videoId = req.query.videoId as string;
  if (!videoId) {
    return res.status(400).json({ code: 400, message: 'videoId is required', data: null });
  }

  try {
    const comments = await query(`
      SELECT c.id, c.content, c.likeCount, c.createdAt,
             p.nickname, p.avatarUrl, p.vipLevel, p.isVip
      FROM comments c
      LEFT JOIN user_profiles p ON c.userId = p.userId
      WHERE c.videoId = ?
      ORDER BY c.createdAt DESC
    `, [videoId]);

    const processed = comments.map(c => ({
      ...c,
      isVip: c.isVip === 1
    }));

    res.json({
      code: 200,
      message: 'success',
      data: processed,
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});


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
