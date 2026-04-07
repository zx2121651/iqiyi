import { Router } from 'express';
import { get, query } from '../db/db';

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

export default router;
