/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    styledComponents: true,
  },
  images: {
    domains: ['images.unsplash.com'], // Add any other domains you need
  },
  webpack: (config) => {
    // Add path aliases
    config.resolve.alias['@'] = __dirname + '/src';
    return config;
  },
};

module.exports = nextConfig;
