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

export default router;
