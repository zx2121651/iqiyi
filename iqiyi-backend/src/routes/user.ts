import { Router } from 'express';
import { get, query } from '../db/db';

const router = Router();

// 简单的登录接口，返回伪造的 token (即 userId)
router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ code: 400, message: 'Missing username or password', data: null });
  }

  try {
    const user = await get('SELECT * FROM users WHERE username = ? AND password = ?', [username, password]);
    if (user) {
      // 在实际项目中这里应当签发 JWT，本处简化处理返回 user.id 作为 token
      res.json({
        code: 200,
        message: 'success',
        data: {
          token: user.id
        }
      });
    } else {
      res.status(401).json({ code: 401, message: 'Invalid username or password', data: null });
    }
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

// 获取用户资料信息
router.get('/profile', async (req, res) => {
  // 从 Authorization header 中获取 token, 形如 "Bearer u1"
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ code: 401, message: 'Unauthorized', data: null });
  }

  const token = authHeader.split(' ')[1]; // 此处的 token 就是 userId

  try {
    const profile = await get('SELECT * FROM user_profiles WHERE userId = ?', [token]);
    if (profile) {
      profile.isVip = profile.isVip === 1;
      res.json({
        code: 200,
        message: 'success',
        data: profile
      });
    } else {
      res.status(404).json({ code: 404, message: 'User profile not found', data: null });
    }
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});


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
