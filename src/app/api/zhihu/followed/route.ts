import { NextRequest, NextResponse } from "next/server";
import { fetchFollowedUsers } from "@/lib/zhihu";

export async function GET(request: NextRequest) {
  const accessToken = request.cookies.get("access_token")?.value;
  if (!accessToken) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);

  const page = parseInt(searchParams.get("page") || "0", 0);
  const perPage = parseInt(searchParams.get("per_page") || "10", 10);

  try {
    const data = await fetchFollowedUsers(accessToken, page, perPage);
    return NextResponse.json(data);
  } catch (error) {
    console.error("Fetch followed users failed:", error);
    return NextResponse.json({ error: "Failed to fetch followed users" }, { status: 502 });
  }
}
