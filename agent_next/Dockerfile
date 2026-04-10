# 使用 Node.js 22.8.0 作为基础镜像
FROM node:22.8.0-alpine AS base

RUN corepack enable && corepack prepare pnpm@latest --activate

# 设置 pnpm 镜像源为国内镜像
ENV PNPM_REGISTRY=https://registry.npmmirror.com

# 安装依赖阶段
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# 复制 package.json 和 lock 文件
COPY package.json pnpm-lock.yaml* ./

# 使用国内镜像源安装依赖
RUN pnpm config set registry https://registry.npmmirror.com && \
    pnpm i --frozen-lockfile

# 构建阶段
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 设置环境变量
ENV NEXT_TELEMETRY_DISABLED=1
ENV PNPM_REGISTRY=https://registry.npmmirror.com

# 构建应用
RUN pnpm config set registry https://registry.npmmirror.com && \
    pnpm build

# 生产运行阶段
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# 复制构建产物
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
