
import pRetry, { AbortError } from 'p-retry'

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
  const run = async (attempt: number) => {
    console.log(`[Token Exchange] Attempt ${attempt}...`);
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

    if (res.status === 429) {
      throw new Error(`Rate limited (${res.status})`);
    }
    if (!res.ok) {
      const text = await res.text();
      if (res.status === 400 && text.includes('invalid_grant')) {
        throw new AbortError('Invalid grant, aborting retries.');
      }
      throw new Error(`HTTP ${res.status}: ${text}`);
    }
      return res.json() as Promise<{ access_token: string; token_type: string; expires_in: number; }>;
    };

    return pRetry(run, {
      retries: 10,
      onFailedAttempt: (error) => {
        console.log(`Attempt ${error.attemptNumber} failed. ${error.retriesLeft} retries left.`);
      },
    });
  }

export async function fetchFollowedUsers(
  accessToken: string,
  page = 0,
  perPage = 20
) {
  const url = `${ZHIHU_BASE_URL}/user/followees?page=${page}&per_page=${perPage}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Fetch followed failed: ${res.status} ${text}`);
  }

  return res.json() as Promise<{
    data: ZhihuUser[]
  }>;
}

export interface ZhihuUser {
  uid: number;
  hash_id: string;
  fullname: string;
  gender: string;
  headline: string;
  description: string;
  avatar_path: string;
  url: string;
  email: string;
  phone_no: string;
}
