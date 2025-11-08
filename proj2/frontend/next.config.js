/** @type {import('next').NextConfig} */
const nextConfig = {
    // Use a standard config structure (empty for now, unless you have other options)
};

// **Conditionally export the turbopack root only when using Turbopack**
if (process.env.TURBOPACK) {
    nextConfig.turbopack = {
        // Set the root to the current project directory where `npm run dev` is run
        root: __dirname,
    };
}

module.exports = nextConfig;