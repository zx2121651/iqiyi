import { Router } from 'express';
import { query } from '../db/db';

const router = Router();

router.get('/privileges', async (req, res) => {
  try {
    const privileges = await query('SELECT * FROM vip_privileges');
    // 移除暴露的 db 内部 id
    const processed = privileges.map(p => {
        const { id, ...rest } = p;
        return rest;
    });
    res.json({
      code: 200,
      message: 'success',
      data: processed,
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

router.get('/recommends', async (req, res) => {
  try {
    const recommends = await query('SELECT * FROM vip_recommends');
    res.json({
      code: 200,
      message: 'success',
      data: recommends,
    });
  } catch (error) {
    res.status(500).json({ code: 500, message: 'Database error', data: null });
  }
});

export default router;
