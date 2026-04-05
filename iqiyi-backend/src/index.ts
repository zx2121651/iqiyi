import express from 'express';
import cors from 'cors';
import homeRoutes from './routes/home';
import shortVideoRoutes from './routes/shortVideo';
import videoRoutes from './routes/video';
import vipRoutes from './routes/vip';
import initDB from './db/init';

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// 注册路由
app.use('/api/home', homeRoutes);
app.use('/api/short-video', shortVideoRoutes);
app.use('/api/video', videoRoutes);
app.use('/api/vip', vipRoutes);

app.get('/', (req, res) => {
  res.send('iQiyi Clone Backend is running.');
});

// 初始化数据库后启动服务
initDB().then(() => {
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });
}).catch(err => {
  console.error("Failed to initialize database:", err);
});
