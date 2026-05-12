export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-950 dark:to-blue-950 relative overflow-hidden">
      {/* 装饰背景元素 */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-blue-200/30 dark:bg-blue-800/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-200/30 dark:bg-indigo-800/10 rounded-full blur-3xl translate-x-1/2 translate-y-1/2" />
      <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-purple-200/20 dark:bg-purple-800/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />

      <main className="relative z-10 text-center px-6 max-w-2xl mx-auto">
        {/* Logo */}
        <div className="mb-8 inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-zhihu-blue to-indigo-600 shadow-lg shadow-blue-500/25">
          <svg
            className="w-10 h-10 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
            />
          </svg>
        </div>

        {/* 标题 */}
        <h1 className="text-5xl font-bold bg-gradient-to-r from-zhihu-blue to-indigo-600 bg-clip-text text-transparent mb-4 tracking-tight">
          Zhihu Labeler
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 mb-2">
          给你的知乎关注列表打标签
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-500 mb-10 max-w-md mx-auto">
          通过标签分类管理你关注的人，让信息流更有序。授权登录后即可开始使用。
        </p>

        {/* 登录按钮 */}
        <a
          href="/api/auth/login"
          className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-zhihu-blue to-indigo-600 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5 transition-all duration-200 text-lg"
        >
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
            <path d="M5.721 0C2.251 0 0 2.25 0 5.719V18.28C0 21.751 2.252 24 5.721 24h12.56C21.751 24 24 21.75 24 18.281V5.72C24 2.249 21.75 0 18.281 0zm1.964 4.078h6.783c.058 0 .104.047.104.104v1.178c0 .058-.046.104-.104.104H9.283a.234.234 0 00-.234.234v4.832h5.419c.058 0 .104.047.104.104v1.178a.104.104 0 01-.104.104H9.049v5.268a.234.234 0 01-.234.234H7.685a.234.234 0 01-.234-.234V4.312a.234.234 0 01.234-.234z" />
          </svg>
          使用知乎登录
        </a>

        {/* 功能介绍 */}
        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6 text-left">
          <div className="p-5 rounded-xl bg-white/60 dark:bg-gray-800/40 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-3">
              <svg className="w-5 h-5 text-zhihu-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">获取关注列表</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">一键同步你的知乎关注</p>
          </div>
          <div className="p-5 rounded-xl bg-white/60 dark:bg-gray-800/40 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mb-3">
              <svg className="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">自定义标签</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">按你的方式分类关注</p>
          </div>
          <div className="p-5 rounded-xl bg-white/60 dark:bg-gray-800/40 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-3">
              <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">筛选过滤</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">按标签快速筛选查看</p>
          </div>
        </div>
      </main>
    </div>
  );
}
