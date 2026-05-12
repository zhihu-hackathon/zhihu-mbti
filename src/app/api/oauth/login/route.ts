import { NextResponse } from "next/server";
import { getAuthUrl } from "@/lib/zhihu";

export async function GET() {
  const clientId = process.env.ZHIHU_CLIENT_ID;
  if (!clientId) {
    return NextResponse.json({ error: "ZHIHU_CLIENT_ID not configured" }, { status: 500 });
  }

  const redirectUri = `${process.env.APP_BASE_URL || "http://localhost:8080"}/api/oauth/callback`;
  const state = crypto.randomUUID().replace(/-/g, "");

  const url = getAuthUrl(clientId, redirectUri);

  const res = NextResponse.redirect(url);
  res.cookies.set("oauth_state", state, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 600,
    path: "/",
  });
  return res;
}
