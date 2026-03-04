import { MockMethod } from 'vite-plugin-mock';
import Mock from 'mockjs';

export default [
  {
    url: '/api/home/banners',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: Mock.mock({
          'list|3-5': [
            {
              id: '@id',
              title: '@ctitle(10, 20)',
              imageUrl: '@image("800x400", "@color", "#FFF", "Banner")',
              link: '@url',
            },
          ],
        }).list,
      };
    },
  },
  {
    url: '/api/home/videos',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: Mock.mock({
          'list|10-20': [
            {
              id: '@id',
              title: '@ctitle(5, 15)',
              coverUrl: '@image("300x400", "@color", "#FFF", "Poster")',
              playCount: '@integer(1000, 1000000)',
              score: '@float(5, 9, 1, 1)',
              isVip: '@boolean',
              desc: '@cparagraph(1, 2)',
            },
          ],
        }).list,
      };
    },
  },
] as MockMethod[];
