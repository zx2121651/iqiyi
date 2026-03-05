import { MockMethod } from 'vite-plugin-mock';
import Mock from 'mockjs';

export default [
  {
    url: '/api/vip/privileges',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: [
          { icon: '🎬', name: '院线新片', desc: '全网首播' },
          { icon: '🚫', name: '广告特权', desc: '跳过广告' },
          { icon: '📺', name: '蓝光1080P', desc: '超清画质' },
          { icon: '🔊', name: '杜比音效', desc: '影院体验' },
          { icon: '🎟️', name: '观影券', desc: '每月两张' },
          { icon: '🎁', name: '专属活动', desc: '周边好礼' },
        ]
      };
    },
  },
  {
    url: '/api/vip/recommends',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: Mock.mock({
          'list|6-10': [
            {
              id: '@id',
              title: '@ctitle(4, 12)',
              coverUrl: '@image("300x400", "#111", "#D4AF37", "VIP Only")',
              score: '@float(7, 9, 1, 1)',
              desc: 'VIP专享巨制',
            },
          ],
        }).list,
      };
    },
  },
] as MockMethod[];
