import re

with open('iqiyi-backend/src/routes/user.ts', 'r', encoding='utf-8') as f:
    content = f.read()

history_route = """
// 获取播放历史记录
router.get('/history', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ code: 401, message: 'Unauthorized', data: null });
  }

  const token = authHeader.split(' ')[1]; // 此处的 token 就是 userId

  try {
    const history = await query(`
      SELECT h.progress, h.lastViewedAt,
             v.id as videoId, v.title, v.coverUrl, v.isVip
      FROM play_history h
      JOIN videos v ON h.videoId = v.id
      WHERE h.userId = ?
      ORDER BY h.lastViewedAt DESC
    `, [token]);

    const processed = history.map(h => ({
      ...h,
      isVip: h.isVip === 1
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
"""

content = content.replace("import { get } from '../db/db';", "import { get, query } from '../db/db';")
content = content.replace("export default router;", history_route)

with open('iqiyi-backend/src/routes/user.ts', 'w', encoding='utf-8') as f:
    f.write(content)
