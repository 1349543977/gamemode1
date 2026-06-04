export default defineAppConfig({
  pages: [
    'pages/index/index',
    'pages/login/index',
    'pages/character-create/index',
    'pages/game/index',
    'pages/year-summary/index',
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#6366F1',
    navigationBarTitleText: '人生模拟器',
    navigationBarTextStyle: 'white',
  },
});
