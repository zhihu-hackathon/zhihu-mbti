
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

type RetryOptions = {
  retries?: number;
  retryDelay?: number;
  backoff?: 'fixed' | 'exponential';
  retryOn?: (response: Response) => boolean;
};

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function fetchWithRetry(
  input: RequestInfo | URL,
  init?: RequestInit,
  options: RetryOptions = {}
): Promise<Response> {
  const {
    retries = 3,
    retryDelay = 1000,
    backoff = 'exponential',
    retryOn = (res) => !res.ok,
  } = options;

  let attempt = 0;

  while (true) {
    try {
      const response = await fetch(input, init);

      if (!retryOn(response) || attempt >= retries) {
        return response;
      }
    } catch (err) {
      // 网络错误（断网、DNS 失败等）也触发重试
      if (attempt >= retries) throw err;
    }

    const delay =
      backoff === 'exponential'
        ? retryDelay * 2 ** attempt
        : retryDelay;

    await sleep(delay);
    attempt++;
  }

}

export async function exchangeCodeForToken(
  appId: string,
  appKey: string,
  redirectUri: string,
  code: string,
  grantType: string
) {

    const res = await fetchWithRetry(`${ZHIHU_BASE_URL}/access_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: new URLSearchParams({
        app_id: appId,
        app_key: appKey,
        grant_type: grantType,
        redirect_uri: redirectUri,
        code: code
      }),
    }, {
      retries: 10,
      retryDelay: 2000,
      backoff: 'fixed',
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
