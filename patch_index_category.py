import re

with open('iqiyi-backend/src/index.ts', 'r', encoding='utf-8') as f:
    content = f.read()

imports = """import searchRoutes from './routes/search';
import categoryRoutes from './routes/category';"""
content = re.sub(r"import searchRoutes from './routes/search';", imports, content)

app_uses = """app.use('/api/search', searchRoutes);
app.use('/api/category', categoryRoutes);"""
content = re.sub(r"app\.use\('/api/search', searchRoutes\);", app_uses, content)

with open('iqiyi-backend/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(content)
