import re

with open('iqiyi-backend/src/index.ts', 'r', encoding='utf-8') as f:
    content = f.read()

imports = """import shortVideoRoutes from './routes/shortVideo';
import videoRoutes from './routes/video';
import vipRoutes from './routes/vip';
import userRoutes from './routes/user';
import searchRoutes from './routes/search';"""

content = re.sub(r"import shortVideoRoutes from './routes/shortVideo';\nimport videoRoutes from './routes/video';\nimport vipRoutes from './routes/vip';", imports, content)

app_uses = """app.use('/api/short-video', shortVideoRoutes);
app.use('/api/video', videoRoutes);
app.use('/api/vip', vipRoutes);
app.use('/api/user', userRoutes);
app.use('/api/search', searchRoutes);"""

content = re.sub(r"app\.use\('/api/short-video', shortVideoRoutes\);\napp\.use\('/api/video', videoRoutes\);\napp\.use\('/api/vip', vipRoutes\);", app_uses, content)

with open('iqiyi-backend/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(content)
