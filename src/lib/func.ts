
const ZHIHU_BASE_URL = process.env.ZHIHU_BASE_URL;

export interface PaginatedResponse<T> {
  data: T[];
  paging: {
    is_end: boolean;
    is_start: boolean;
    next: string;
    previous: string;
    totals: number;
  };
}

export interface Follow {
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

export interface User {
  uid: number;
  fullname: string;
  gender: string;
  headline: string;
  description: string;
  avatar_path: string;
  phone_no: string;
  email: string;
}

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
        throw new Error('Invalid grant, aborting retries.');
      }
      throw new Error(`HTTP ${res.status}: ${text}`);
    }
    return res.json() as Promise<{ access_token: string; token_type: string; expires_in: number; }>;
  }

// 获取用户信息
export async function fetchUserInfo(
  accessToken: string
) {
  const url = `${ZHIHU_BASE_URL}/user`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  return res.json() as Promise<User>;
}


// 粉丝列表
export async function fetchFollowers(
  accessToken: string, 
  page: number = 0, 
  perPage: number = 10): Promise<PaginatedResponse<Follow>> {
  const url = `${ZHIHU_BASE_URL}/user/followers?page=${page}&per_page=${perPage}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  return res.json() as Promise<PaginatedResponse<Follow>>;
}

// 关注列表
export async function fetchFollowed(
  accessToken: string, 
  page: number = 0, 
  perPage: number = 10): Promise<PaginatedResponse<Follow>> {

  const url = `${ZHIHU_BASE_URL}/user/followed?page=${page}&per_page=${perPage}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  return res.json() as Promise<PaginatedResponse<Follow>>;

}

// 关注动态
export async function fetchMoments(
  accessToken: string
) {

  const url = `${ZHIHU_BASE_URL}/user/moments`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  
  return res.json();
}
