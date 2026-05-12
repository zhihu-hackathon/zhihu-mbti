
const ZHIHU_API_BASE = process.env.ZHIHU_API_BASE
const ZHIHU_TOKEN_URL = `${ZHIHU_API_BASE}/access_token`;

export function getAuthUrl(clientId: string, redirectUri: string, state: string) {
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: "code",
    state,
    scope: "relationships_read",
  });
  return `${ZHIHU_API_BASE}?${params.toString()}`;
}

export async function exchangeCodeForToken(
  code: string,
  clientId: string,
  clientSecret: string,
  redirectUri: string
) {
  const res = await fetch(ZHIHU_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: clientId,
      client_secret: clientSecret,
      grant_type: "authorization_code",
      code,
      redirect_uri: redirectUri,
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
    refresh_token: string;
  }>;
}

export async function fetchFollowedUsers(
  accessToken: string,
  username: string,
  offset = 0,
  limit = 20
) {
  const url = `${ZHIHU_API_BASE}/members/${username}/followees?limit=${limit}&offset=${offset}`;
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
