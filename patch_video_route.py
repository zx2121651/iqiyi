import re

with open('iqiyi-backend/src/routes/video.ts', 'r', encoding='utf-8') as f:
    content = f.read()

comments_route = """
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
"""

content = content.replace("export default router;", comments_route)

with open('iqiyi-backend/src/routes/video.ts', 'w', encoding='utf-8') as f:
    f.write(content)
