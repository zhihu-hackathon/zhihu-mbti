import { NextRequest, NextResponse } from "next/server";
import { fetchFollowedUsers } from "@/lib/zhihu";

export async function GET(request: NextRequest) {
  const accessToken = request.cookies.get("access_token")?.value;
  if (!accessToken) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const username = searchParams.get("username");
  if (!username) {
    return NextResponse.json({ error: "username parameter required" }, { status: 400 });
  }

  const offset = parseInt(searchParams.get("offset") || "0", 10);
  const limit = parseInt(searchParams.get("limit") || "20", 10);

  try {
    const data = await fetchFollowedUsers(accessToken, username, offset, limit);
    return NextResponse.json(data);
  } catch (error) {
    console.error("Fetch followed users failed:", error);
    return NextResponse.json({ error: "Failed to fetch followed users" }, { status: 502 });
  }
}
