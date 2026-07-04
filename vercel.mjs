/** @type {import('@vercel/config/v1').VercelConfig} */
const branch = process.env.VERCEL_GIT_COMMIT_REF || 'dev';
const isMaster = branch === 'master';

export const config = {
  $schema: 'https://openapi.vercel.sh/vercel.json',
  git: {
    deploymentEnabled: {
      dev: true,
      master: true,
    },
  },
  github: {
    silent: true,
  },
  services: {
    frontend: {
      root: 'frontend',
      framework: 'vite',
    },
    backend: {
      root: '.',
      framework: 'fastapi',
      entrypoint: 'vercel_app:app',
      installCommand: isMaster
        ? 'pip install -r requirements-vercel-prod.txt && bash scripts/vercel-prepare-data.sh'
        : 'pip install -r requirements-vercel.txt',
      functions: {
        'vercel_app.py': {
          maxDuration: isMaster ? 60 : 30,
        },
      },
    },
  },
  rewrites: [
    { source: '/api/:path*', destination: { service: 'backend' } },
    { source: '/(.*)', destination: { service: 'frontend' } },
  ],
};
