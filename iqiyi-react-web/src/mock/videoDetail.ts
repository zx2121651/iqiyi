import { MockMethod } from 'vite-plugin-mock';
import Mock from 'mockjs';

export default [
  {
    url: '/api/video/detail',
    method: 'get',
    response: (req: any) => {
      return {
        code: 200,
        message: 'success',
        data: Mock.mock({
          id: req.query?.id || '@id',
          title: '@ctitle(8, 20)',
          playUrl: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4', // 占位视频
          coverUrl: '@image("800x450", "#333", "#FFF", "Video Cover")',
          score: '@float(7, 9, 1, 1)',
          playCount: '@integer(10000, 9999999)',
          year: '2023',
          tags: ['悬疑', '犯罪', '高分'],
          desc: '这是一段关于该视频的详细剧情介绍。@cparagraph(2, 4)',
          likeCount: '@integer(1000, 99999)',
          commentCount: '@integer(500, 10000)',
        }),
      };
    },
  },
  {
    url: '/api/video/related',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: Mock.mock({
          'list|8-12': [
            {
              id: '@id',
              title: '@ctitle(5, 15)',
              coverUrl: '@image("300x169", "#222", "#FFF", "Related Video")',
              playCount: '@integer(1000, 1000000)',
              duration: '@time("mm:ss")',
            },
          ],
        }).list,
      };
    },
  },
] as MockMethod[];
