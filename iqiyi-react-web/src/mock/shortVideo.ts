import { MockMethod } from 'vite-plugin-mock';
import Mock from 'mockjs';

export default [
  {
    url: '/api/short-video/list',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: Mock.mock({
          'list|5-10': [
            {
              id: '@id',
              authorName: '@cname',
              authorAvatar: '@image("100x100", "@color", "#FFF", "Avatar")',
              desc: '@cparagraph(1, 3)',
              coverUrl: '@image("720x1280", "@color", "#FFF", "Short Video")',
              likeCount: '@integer(1000, 999999)',
              commentCount: '@integer(100, 99999)',
              shareCount: '@integer(10, 9999)',
              isLiked: '@boolean',
            },
          ],
        }).list,
      };
    },
  },
] as MockMethod[];
