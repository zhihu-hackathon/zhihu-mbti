import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "pic1.zhimg.com" },
      { protocol: "https", hostname: "pic2.zhimg.com" },
      { protocol: "https", hostname: "pic3.zhimg.com" },
      { protocol: "https", hostname: "pic4.zhimg.com" },
    ],
  },
};

export default nextConfig;
