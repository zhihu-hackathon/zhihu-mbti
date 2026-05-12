const ZHIHU_BASE_URL = process.env.ZHIHU_BASE_URL;

export function getAuthUrl(appId: string, redirectUri: string) {
  const params = new URLSearchParams({
    app_id: appId,
    redirect_uri: redirectUri,
    response_type: "code"
  });
  return `${ZHIHU_BASE_URL}/authorize?${params.toString()}`;
}

export async function exchangeCodeForToken(
  appId: string,
  appKey: string,
  redirectUri: string,
  code: string,
  grantType: string
) {
  const res = await fetch(`${ZHIHU_BASE_URL}/access_token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: new URLSearchParams({
      app_id: appId,
      app_key: appKey,
      grant_type: grantType,
      redirect_uri: redirectUri,
      code: code
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Token exchange failed: ${res.status} ${text}`);
  }

  return res.json() as Promise<{
    access_token: string;
    token_type: string;
    expires_in: number;
  }>;
}

export async function fetchFollowedUsers(
  accessToken: string,
  username: string,
  offset = 0,
  limit = 20
) {
  const url = `${ZHIHU_BASE_URL}/members/${username}/followees?limit=${limit}&offset=${offset}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Fetch followed failed: ${res.status} ${text}`);
  }

  return res.json() as Promise<{
    data: ZhihuUser[];
    paging: { is_end: boolean; next: string; previous: string };
  }>;
}

export interface ZhihuUser {
  id: string;
  url_token: string;
  name: string;
  headline: string;
  avatar_url: string;
  follower_count: number;
  answer_count: number;
  articles_count: number;
}
