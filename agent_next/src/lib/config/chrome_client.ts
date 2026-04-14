import { ChromaClient } from 'chromadb';

const chromaConfig = {
  host: process.env.CHROMA_HOST || 'localhost',
  port: parseInt(process.env.CHROMA_PORT || '8000'),
  path: process.env.CHROMA_PATH || '/api/v1',
  authProvider: process.env.CHROMA_AUTH_PROVIDER || 'token',
  authCredentials: process.env.CHROMA_AUTH_CREDENTIALS || '',
};

let client: ChromaClient | null = null;

export async function getChromaClient() {
  if (!client) {
    try {
      client = new ChromaClient({
        path: `http://${chromaConfig.host}:${chromaConfig.port}${chromaConfig.path}`,
        auth: {
          provider: chromaConfig.authProvider,
          credentials: chromaConfig.authCredentials,
        },
      });

      await client.heartbeat();
      console.log('ChromaDB 连接成功');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '未知错误';
      console.error('ChromaDB 连接失败:', errorMessage);
      throw new Error('ChromaDB 连接失败: ' + errorMessage);
    }
  }
  
  return client;
}

export async function closeChromaClient() {
  client = null;
  console.log('ChromaDB 客户端已重置');
}
