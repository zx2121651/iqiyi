import { Router } from 'express';
import { query } from '../db/db';

const router = Router();

router.get('/banners', async (req, res) => {
  try {
    const banners = await query('SELECT * FROM banners');
    res.json({
      code: 200,
      message: 'success',
      data: banners,
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

router.get('/videos', async (req, res) => {
  try {
    const videos = await query('SELECT * FROM videos');
    // 对于 isVip 字段转换回 boolean
    const processedVideos = videos.map(v => ({
      ...v,
      isVip: v.isVip === 1,
      tags: JSON.parse(v.tags)
    }));
    res.json({
      code: 200,
      message: 'success',
      data: processedVideos,
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

export default router;
