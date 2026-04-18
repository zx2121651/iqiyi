import re

with open('iqiyi-backend/src/db/init.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the duplicate '};' and misplaced code by writing a clean file
content = """import db, { run } from './db';

const initDB = async () => {
  try {
    // 启用外键约束
    await run('PRAGMA foreign_keys = ON');

    console.log('Creating tables...');
    await run(`
      CREATE TABLE IF NOT EXISTS banners (
        id TEXT PRIMARY KEY,
        title TEXT,
        imageUrl TEXT,
        link TEXT
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        title TEXT,
        coverUrl TEXT,
        playCount INTEGER,
        score REAL,
        isVip INTEGER,
        desc TEXT,
        playUrl TEXT,
        year TEXT,
        tags TEXT,
        likeCount INTEGER,
        commentCount INTEGER
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS short_videos (
        id TEXT PRIMARY KEY,
        authorName TEXT,
        authorAvatar TEXT,
        desc TEXT,
        coverUrl TEXT,
        likeCount INTEGER,
        commentCount INTEGER,
        shareCount INTEGER,
        isLiked INTEGER
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS related_videos (
        id TEXT PRIMARY KEY,
        title TEXT,
        coverUrl TEXT,
        playCount INTEGER,
        duration TEXT
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS vip_privileges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        icon TEXT,
        name TEXT,
        desc TEXT
      )
    `);

    await run(`
      CREATE TABLE IF NOT EXISTS vip_recommends (
        id TEXT PRIMARY KEY,
        title TEXT,
        coverUrl TEXT,
        score REAL,
        desc TEXT
      )
    `);

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

    db.get('SELECT count(*) as count FROM banners', async (err, row: any) => {
      if (err) {
        console.error(err);
        return;
      }

      if (row.count === 0) {
        console.log('Seeding initial data...');
        await seedData();
        console.log('Seeding completed.');
      } else {
        console.log('Database already seeded.');
      }
    });

  } catch (error) {
    console.error('Database initialization failed:', error);
  }
};

const seedData = async () => {
  const banners = [
      { id: "b1", title: "狂飙：全员飙戏，高能不断", imageUrl: "https://dummyimage.com/800x400/121212/fff&text=Banner+1", link: "/video/b1" },
      { id: "b2", title: "独行月球：沈腾马丽爆笑重逢", imageUrl: "https://dummyimage.com/800x400/1f1f1f/fff&text=Banner+2", link: "/video/b2" },
      { id: "b3", title: "乐队的夏天：重燃摇滚之魂", imageUrl: "https://dummyimage.com/800x400/333333/fff&text=Banner+3", link: "/video/b3" }
  ];
  for (const b of banners) {
      await run('INSERT INTO banners (id, title, imageUrl, link) VALUES (?, ?, ?, ?)', [b.id, b.title, b.imageUrl, b.link]);
  }

  const videos = [
      { id: "v1", title: "三体 (全集)", coverUrl: "https://dummyimage.com/300x400/1f1f1f/fff&text=Poster+1", playCount: 1540000, score: 8.9, isVip: 1, desc: "物理学不存在了？汪淼卧底科学边界", playUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", year: "2023", tags: JSON.stringify(["科幻", "悬疑", "高分"]), likeCount: 45000, commentCount: 12000 },
      { id: "v2", title: "长风渡", coverUrl: "https://dummyimage.com/300x400/222222/fff&text=Poster+2", playCount: 890000, score: 7.5, isVip: 1, desc: "先婚后爱，白敬亭宋轶携手搞事业", playUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", year: "2023", tags: JSON.stringify(["古装", "言情"]), likeCount: 20000, commentCount: 5000 },
      { id: "v3", title: "种地吧", coverUrl: "https://dummyimage.com/300x400/333333/fff&text=Poster+3", playCount: 200000, score: 9.0, isVip: 0, desc: "十个勤天，做大做强", playUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", year: "2023", tags: JSON.stringify(["综艺", "真人秀"]), likeCount: 15000, commentCount: 2000 },
      { id: "v4", title: "流浪地球2", coverUrl: "https://dummyimage.com/300x400/111111/fff&text=Poster+4", playCount: 5600000, score: 9.2, isVip: 1, desc: "硬核科幻，炸毁月球计划启动", playUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", year: "2023", tags: JSON.stringify(["科幻", "电影"]), likeCount: 100000, commentCount: 30000 },
      { id: "v5", title: "莲花楼", coverUrl: "https://dummyimage.com/300x400/444444/fff&text=Poster+5", playCount: 3400000, score: 8.5, isVip: 1, desc: "成毅化身神医李莲花探案", playUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", year: "2023", tags: JSON.stringify(["古装", "武侠", "悬疑"]), likeCount: 80000, commentCount: 25000 },
      { id: "v6", title: "中国说唱巅峰对决", coverUrl: "https://dummyimage.com/300x400/555555/fff&text=Poster+6", playCount: 1200000, score: 7.8, isVip: 0, desc: "巅峰 Rapper 齐聚一堂", playUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", year: "2023", tags: JSON.stringify(["综艺", "音乐"]), likeCount: 30000, commentCount: 8000 }
  ];
  for (const v of videos) {
      await run('INSERT INTO videos (id, title, coverUrl, playCount, score, isVip, desc, playUrl, year, tags, likeCount, commentCount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [v.id, v.title, v.coverUrl, v.playCount, v.score, v.isVip, v.desc, v.playUrl, v.year, v.tags, v.likeCount, v.commentCount]);
  }

  const shortVideos = [
      { id: "sv1", authorName: "影视解说老王", authorAvatar: "https://dummyimage.com/100x100/333/fff&text=Avatar+1", desc: "这部电影也太细节了吧，你发现了吗？", coverUrl: "https://dummyimage.com/720x1280/1a1a1a/fff&text=Short+Video+1", likeCount: 125000, commentCount: 4500, shareCount: 1200, isLiked: 0 },
      { id: "sv2", authorName: "搞笑小能手", authorAvatar: "https://dummyimage.com/100x100/444/fff&text=Avatar+2", desc: "今天也是被猫咪治愈的一天呢~", coverUrl: "https://dummyimage.com/720x1280/2b2b2b/fff&text=Short+Video+2", likeCount: 340000, commentCount: 12000, shareCount: 5600, isLiked: 1 },
      { id: "sv3", authorName: "美食探店", authorAvatar: "https://dummyimage.com/100x100/555/fff&text=Avatar+3", desc: "隐藏在街角的绝世美味，必须打卡！", coverUrl: "https://dummyimage.com/720x1280/3c3c3c/fff&text=Short+Video+3", likeCount: 89000, commentCount: 2300, shareCount: 450, isLiked: 0 }
  ];
  for (const sv of shortVideos) {
      await run('INSERT INTO short_videos (id, authorName, authorAvatar, desc, coverUrl, likeCount, commentCount, shareCount, isLiked) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [sv.id, sv.authorName, sv.authorAvatar, sv.desc, sv.coverUrl, sv.likeCount, sv.commentCount, sv.shareCount, sv.isLiked]);
  }

  const related = [
      { id: "r1", title: "开端", coverUrl: "https://dummyimage.com/300x169/222/fff&text=Related+1", playCount: 890000, duration: "45:00" },
      { id: "r2", title: "漫长的季节", coverUrl: "https://dummyimage.com/300x169/333/fff&text=Related+2", playCount: 1200000, duration: "52:10" }
  ];
  for (const r of related) {
      await run('INSERT INTO related_videos (id, title, coverUrl, playCount, duration) VALUES (?, ?, ?, ?, ?)', [r.id, r.title, r.coverUrl, r.playCount, r.duration]);
  }

  const vipPrivileges = [
      { icon: '🎬', name: '院线新片', desc: '全网首播' },
      { icon: '🚫', name: '广告特权', desc: '跳过广告' },
      { icon: '📺', name: '蓝光1080P', desc: '超清画质' }
  ];
  for (const vp of vipPrivileges) {
      await run('INSERT INTO vip_privileges (icon, name, desc) VALUES (?, ?, ?)', [vp.icon, vp.name, vp.desc]);
  }

  const vipRecommends = [
      { id: "vr1", title: "满江红", coverUrl: "https://dummyimage.com/300x400/111/D4AF37&text=VIP+1", score: 8.2, desc: "VIP专享巨制" }
  ];
  for (const vr of vipRecommends) {
      await run('INSERT INTO vip_recommends (id, title, coverUrl, score, desc) VALUES (?, ?, ?, ?, ?)', [vr.id, vr.title, vr.coverUrl, vr.score, vr.desc]);
  }

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
};

export default initDB;
"""

with open('iqiyi-backend/src/db/init.ts', 'w', encoding='utf-8') as f:
    f.write(content)
