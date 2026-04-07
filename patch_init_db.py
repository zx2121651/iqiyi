import re

with open('iqiyi-backend/src/db/init.ts', 'r', encoding='utf-8') as f:
    content = f.read()

new_tables = """
    await run(`
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS user_profiles (
        userId TEXT PRIMARY KEY,
        nickname TEXT,
        avatarUrl TEXT,
        vipLevel INTEGER,
        isVip INTEGER
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS comments (
        id TEXT PRIMARY KEY,
        videoId TEXT,
        userId TEXT,
        content TEXT,
        likeCount INTEGER,
        createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
"""

content = content.replace("db.get('SELECT count(*) as count FROM banners'", new_tables + "\n    db.get('SELECT count(*) as count FROM banners'")


seed_data = """
  const users = [
      { id: "u1", username: "admin", password: "password123" },
      { id: "u2", username: "test", password: "password123" }
  ];
  for (const u of users) {
      await run('INSERT INTO users (id, username, password) VALUES (?, ?, ?)', [u.id, u.username, u.password]);
  }

  const profiles = [
      { userId: "u1", nickname: "管理员", avatarUrl: "https://dummyimage.com/100x100/ff4d4f/fff&text=Admin", vipLevel: 5, isVip: 1 },
      { userId: "u2", nickname: "热心网友", avatarUrl: "https://dummyimage.com/100x100/1890ff/fff&text=User", vipLevel: 0, isVip: 0 }
  ];
  for (const p of profiles) {
      await run('INSERT INTO user_profiles (userId, nickname, avatarUrl, vipLevel, isVip) VALUES (?, ?, ?, ?, ?)', [p.userId, p.nickname, p.avatarUrl, p.vipLevel, p.isVip]);
  }

  const comments = [
      { id: "c1", videoId: "v1", userId: "u1", content: "三体拍得太好了，国产科幻之光！", likeCount: 500 },
      { id: "c2", videoId: "v1", userId: "u2", content: "叶文洁那段绝了", likeCount: 120 },
      { id: "c3", videoId: "v2", userId: "u2", content: "宋轶好美！", likeCount: 88 }
  ];
  for (const c of comments) {
      await run('INSERT INTO comments (id, videoId, userId, content, likeCount) VALUES (?, ?, ?, ?, ?)', [c.id, c.videoId, c.userId, c.content, c.likeCount]);
  }
"""

content = content.replace("export default initDB;", seed_data + "\n};\n\nexport default initDB;")

with open('iqiyi-backend/src/db/init.ts', 'w', encoding='utf-8') as f:
    f.write(content)
