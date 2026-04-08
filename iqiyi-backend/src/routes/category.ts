import { Router } from 'express';
import { query } from '../db/db';

const router = Router();

// 获取分类列表
router.get('/list', async (req, res) => {
  try {
    const categories = await query('SELECT * FROM categories');
    res.json({
      code: 200,
      message: 'success',
      data: categories
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

// 获取某分类下的视频 (根据 tags 进行简单匹配)
router.get('/videos', async (req, res) => {
  const name = req.query.name as string;
  if (!name) {
    return res.status(400).json({ code: 400, message: 'Category name is required', data: null });
  }

  try {
    const searchPattern = `%"${name}"%`; // tags 是 JSON 字符串如 '["电影", "科幻"]'
    const results = await query(
      'SELECT id, title, coverUrl, playCount, score, isVip, desc, year, tags FROM videos WHERE tags LIKE ?',
      [searchPattern]
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
