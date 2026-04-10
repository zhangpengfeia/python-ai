# 使用 Node.js 22 作为基础镜像
FROM node:22.8.0-alpine AS base

# 安装依赖阶段
FROM base AS deps
RUN apk add --no-cache libc-compat
WORKDIR /app

COPY package.json pnpm-lock.yaml* ./

# 👉 终极修复：直接用 npm 安装 pnpm，完全绕过坏掉的 corepack
RUN npm install -g pnpm && \
    pnpm config set registry https://registry.npmmirror.com/ && \
    pnpm i --frozen-lockfile

# 构建阶段
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

# 同样直接用 npm 装 pnpm，不碰 corepack
RUN npm install -g pnpm && pnpm build

# 生产运行阶段
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]