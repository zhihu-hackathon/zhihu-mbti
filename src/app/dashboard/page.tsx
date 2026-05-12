"use client";

import { useEffect, useState, useCallback } from "react";

interface ZhihuUser {
  id: string;
  url_token: string;
  name: string;
  headline: string;
  avatar_url: string;
  follower_count: number;
  answer_count: number;
  articles_count: number;
}

interface LabelMap {
  [userId: string]: string[];
}

const LABEL_COLORS = [
  "bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300",
  "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300",
  "bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300",
  "bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300",
  "bg-pink-100 text-pink-700 dark:bg-pink-900/40 dark:text-pink-300",
  "bg-teal-100 text-teal-700 dark:bg-teal-900/40 dark:text-teal-300",
];

function getLabelColor(index: number) {
  return LABEL_COLORS[index % LABEL_COLORS.length];
}

export default function Dashboard() {
  const [users, setUsers] = useState<ZhihuUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [username, setUsername] = useState("");
  const [labels, setLabels] = useState<LabelMap>({});
  const [newLabel, setNewLabel] = useState("");
  const [activeLabelInput, setActiveLabelInput] = useState<string | null>(null);
  const [filterLabel, setFilterLabel] = useState<string | null>(null);
  const [allLabels, setAllLabels] = useState<string[]>([]);

  // Load labels from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("zhihu-labels");
    if (saved) {
      try {
        setLabels(JSON.parse(saved));
      } catch {}
    }
  }, []);

  // Save labels to localStorage
  useEffect(() => {
    if (Object.keys(labels).length > 0) {
      localStorage.setItem("zhihu-labels", JSON.stringify(labels));
    }
    // Collect all unique labels
    const labelSet = new Set<string>();
    Object.values(labels).forEach((arr) => arr.forEach((l) => labelSet.add(l)));
    setAllLabels(Array.from(labelSet).sort());
  }, [labels]);

  const fetchUsers = useCallback(async (offset = 0) => {
    if (!username) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(
        `/api/zhihu/followed?username=${encodeURIComponent(username)}&offset=${offset}&limit=20`
      );
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to fetch");
      }
      const data = await res.json();
      if (offset === 0) {
        setUsers(data.data || []);
      } else {
        setUsers((prev) => [...prev, ...(data.data || [])]);
      }
      // If there are more pages, we could auto-fetch, but for v1 let's keep it simple
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [username]);

  useEffect(() => {
    if (username) {
      fetchUsers();
    }
  }, [username, fetchUsers]);

  const addLabel = (userId: string, label: string) => {
    if (!label.trim()) return;
    setLabels((prev) => {
      const current = prev[userId] || [];
      if (current.includes(label.trim())) return prev;
      return { ...prev, [userId]: [...current, label.trim()] };
    });
    setNewLabel("");
    setActiveLabelInput(null);
  };

  const removeLabel = (userId: string, label: string) => {
    setLabels((prev) => {
      const current = prev[userId] || [];
      return { ...prev, [userId]: current.filter((l) => l !== label) };
    });
  };

  const filteredUsers = filterLabel
    ? users.filter((u) => (labels[u.id] || []).includes(filterLabel))
    : users;

  const handleLogout = async () => {
    // Clear cookie via a simple approach
    document.cookie = "access_token=; path=/; max-age=0";
    window.location.href = "/";
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="sticky top-0 z-20 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <h1 className="text-xl font-bold bg-gradient-to-r from-zhihu-blue to-indigo-600 bg-clip-text text-transparent">
            Zhihu Labeler
          </h1>
          <button
            onClick={handleLogout}
            className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
          >
            退出登录
          </button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-6">
        {/* Username Input */}
        {!username && (
          <div className="max-w-md mx-auto mt-20 text-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
              输入你的知乎用户名
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
              用户名是你的知乎个人主页 URL 中的部分，如 zhihu.com/people/<strong>xxx</strong>
            </p>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (username) fetchUsers();
              }}
              className="flex gap-3"
            >
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="输入知乎用户名"
                className="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-zhihu-blue focus:border-transparent outline-none transition-all"
              />
              <button
                type="submit"
                disabled={!username.trim()}
                className="px-6 py-3 bg-gradient-to-r from-zhihu-blue to-indigo-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-blue-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                获取关注
              </button>
            </form>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="max-w-md mx-auto mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-700 dark:text-red-300 text-sm">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-zhihu-blue border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {/* Filter bar */}
        {username && !loading && allLabels.length > 0 && (
          <div className="mb-6 flex flex-wrap items-center gap-2">
            <span className="text-sm text-gray-500 dark:text-gray-400 mr-1">筛选：</span>
            <button
              onClick={() => setFilterLabel(null)}
              className={`px-3 py-1 rounded-full text-sm transition-colors ${
                filterLabel === null
                  ? "bg-zhihu-blue text-white"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
            >
              全部
            </button>
            {allLabels.map((label, i) => (
              <button
                key={label}
                onClick={() => setFilterLabel(filterLabel === label ? null : label)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  filterLabel === label
                    ? "ring-2 ring-zhihu-blue ring-offset-1"
                    : ""
                } ${getLabelColor(i)}`}
              >
                {label}
              </button>
            ))}
          </div>
        )}

        {/* User list */}
        {username && !loading && users.length > 0 && (
          <div className="space-y-3">
            {filteredUsers.map((user) => (
              <div
                key={user.id}
                className="p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-4">
                  {/* Avatar */}
                  <img
                    src={user.avatar_url}
                    alt={user.name}
                    className="w-12 h-12 rounded-full flex-shrink-0"
                  />

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                        {user.name}
                      </h3>
                      <a
                        href={`https://www.zhihu.com/people/${user.url_token}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-zhihu-blue hover:underline text-sm"
                      >
                        @{user.url_token}
                      </a>
                    </div>
                    {user.headline && (
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5 truncate">
                        {user.headline}
                      </p>
                    )}
                    <div className="flex gap-3 mt-1 text-xs text-gray-400 dark:text-gray-500">
                      <span>{user.follower_count} 关注者</span>
                      <span>{user.answer_count} 回答</span>
                      <span>{user.articles_count} 文章</span>
                    </div>

                    {/* Labels */}
                    <div className="flex flex-wrap items-center gap-1.5 mt-2">
                      {(labels[user.id] || []).map((label, i) => (
                        <span
                          key={label}
                          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${getLabelColor(i)}`}
                        >
                          {label}
                          <button
                            onClick={() => removeLabel(user.id, label)}
                            className="hover:opacity-70 transition-opacity"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                      {activeLabelInput === user.id ? (
                        <form
                          onSubmit={(e) => {
                            e.preventDefault();
                            addLabel(user.id, newLabel);
                          }}
                          className="inline-flex"
                        >
                          <input
                            type="text"
                            value={newLabel}
                            onChange={(e) => setNewLabel(e.target.value)}
                            placeholder="标签名"
                            autoFocus
                            onBlur={() => {
                              if (newLabel.trim()) {
                                addLabel(user.id, newLabel);
                              } else {
                                setActiveLabelInput(null);
                              }
                            }}
                            className="w-20 px-2 py-0.5 text-xs rounded-full border border-gray-300 dark:border-gray-600 bg-transparent outline-none focus:ring-1 focus:ring-zhihu-blue"
                          />
                        </form>
                      ) : (
                        <button
                          onClick={() => {
                            setActiveLabelInput(user.id);
                            setNewLabel("");
                          }}
                          className="px-2 py-0.5 rounded-full text-xs border border-dashed border-gray-300 dark:border-gray-600 text-gray-400 hover:text-zhihu-blue hover:border-zhihu-blue transition-colors"
                        >
                          + 标签
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {filteredUsers.length === 0 && filterLabel && (
              <p className="text-center text-gray-500 dark:text-gray-400 py-10">
                没有带有「{filterLabel}」标签的用户
              </p>
            )}
          </div>
        )}

        {/* Empty state after loading */}
        {username && !loading && users.length === 0 && !error && (
          <p className="text-center text-gray-500 dark:text-gray-400 py-10">
            暂无关注用户数据
          </p>
        )}

        {/* Load more / Refresh controls */}
        {username && !loading && users.length > 0 && (
          <div className="flex justify-center gap-3 mt-6">
            <button
              onClick={() => fetchUsers(users.length)}
              className="px-5 py-2 text-sm border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              加载更多
            </button>
            <button
              onClick={() => fetchUsers(0)}
              className="px-5 py-2 text-sm border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              刷新
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
