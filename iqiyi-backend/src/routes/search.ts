import { Router } from 'express';
import { query } from '../db/db';

const router = Router();

router.get('/', async (req, res) => {
  const keyword = req.query.keyword as string;
  if (!keyword) {
    return res.status(400).json({ code: 400, message: 'Keyword is required', data: null });
  }

  try {
    // 模糊匹配标题或描述
    const searchPattern = `%${keyword}%`;
    const results = await query(
      'SELECT id, title, coverUrl, playCount, score, isVip, desc, year, tags FROM videos WHERE title LIKE ? OR desc LIKE ?',
      [searchPattern, searchPattern]
    );

    const processed = results.map(v => ({
      ...v,
      isVip: v.isVip === 1,
      tags: v.tags ? JSON.parse(v.tags) : []
    }));

    res.json({
      code: 200,
      message: 'success',
      data: processed
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

export default router;
