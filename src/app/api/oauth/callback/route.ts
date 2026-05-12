import { NextRequest, NextResponse } from "next/server";
import { exchangeCodeForToken } from "@/lib/zhihu";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("authorization_code");

  // const state = searchParams.get("state");
  // const error = searchParams.get("error");

  // if (error) {
  //   return NextResponse.redirect(new URL(`/?error=${encodeURIComponent(error)}`, request.url));
  // }

  if (!code) {
    return NextResponse.redirect(new URL("/?error=missing_params", request.url));
  }

  // const savedState = request.cookies.get("oauth_state")?.value;
  // if (!savedState || savedState !== state) {
  //   return NextResponse.redirect(new URL("/?error=invalid_state", request.url));
  // }

  const clientId = process.env.ZHIHU_CLIENT_ID;
  const clientSecret = process.env.ZHIHU_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    return NextResponse.redirect(new URL("/?error=server_config", request.url));
  }

  const redirectUri = `${process.env.APP_BASE_URL || "http://localhost:8080"}/api/oauth/callback`;

  try {
    const tokenData = await exchangeCodeForToken(clientId, clientSecret, redirectUri, code, "authorization_code");
    console.log(`token data access token: ${tokenData.access_token}`)
    const dashboardUrl = new URL("/dashboard", process.env.APP_BASE_URL)
    const res = NextResponse.redirect(dashboardUrl);
    res.cookies.set("oauth_state", "", { path: "/", maxAge: 0 });
    res.cookies.set("access_token", tokenData.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: tokenData.expires_in,
      path: "/",
    });
    return res;
  } catch (err) {
    console.error("Token exchange failed:", err);
    return NextResponse.redirect(new URL("/?error=token_exchange_failed", request.url));
  }
}
