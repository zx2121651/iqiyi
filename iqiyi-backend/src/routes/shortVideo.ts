import { Router } from 'express';
import { query } from '../db/db';

const router = Router();

router.get('/list', async (req, res) => {
  try {
    const shortVideos = await query('SELECT * FROM short_videos');
    const processed = shortVideos.map(sv => ({
      ...sv,
      isLiked: sv.isLiked === 1
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
