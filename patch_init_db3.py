import re

with open('iqiyi-backend/src/db/init.ts', 'r', encoding='utf-8') as f:
    content = f.read()

new_tables = """
    await run(`
      CREATE TABLE IF NOT EXISTS play_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId TEXT,
        videoId TEXT,
        progress INTEGER,
        lastViewedAt DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS categories (
        id TEXT PRIMARY KEY,
        name TEXT,
        icon TEXT
      )
    `);
"""

content = content.replace("db.get('SELECT count(*) as count FROM banners'", new_tables + "\n    db.get('SELECT count(*) as count FROM banners'")


seed_data = """
  const history = [
      { userId: "u1", videoId: "v1", progress: 1200 },
      { userId: "u1", videoId: "v4", progress: 3450 },
      { userId: "u2", videoId: "v2", progress: 600 }
  ];
  for (const h of history) {
      await run('INSERT INTO play_history (userId, videoId, progress) VALUES (?, ?, ?)', [h.userId, h.videoId, h.progress]);
  }

  const categories = [
      { id: "cat_1", name: "电视剧", icon: "📺" },
      { id: "cat_2", name: "电影", icon: "🎬" },
      { id: "cat_3", name: "动漫", icon: "✨" },
      { id: "cat_4", name: "综艺", icon: "🎤" },
      { id: "cat_5", name: "纪录片", icon: "🎞️" }
  ];
  for (const c of categories) {
      await run('INSERT INTO categories (id, name, icon) VALUES (?, ?, ?)', [c.id, c.name, c.icon]);
  }
"""

content = content.replace("export default initDB;", seed_data + "\n};\n\nexport default initDB;")

with open('iqiyi-backend/src/db/init.ts', 'w', encoding='utf-8') as f:
    f.write(content)
