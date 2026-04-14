import { BaseChatModel } from "@langchain/core/language_models/chat_models";
import {Embeddings} from "@langchain/core/embeddings";
import { ChatAlibabaTongyi } from "@langchain/community/chat_models/alibaba_tongyi";
import { AlibabaTongyiEmbeddings } from "@langchain/community/embeddings/alibaba_tongyi";
import ragConfig from "@/agent/config/rag";

// ==============================
// 抽象工厂基类（对应 ABC 抽象类）
// ==============================
export abstract class BaseModelFactory {
  abstract generator(): Embeddings | BaseChatModel | null;
}

// ==============================
// 通义千问聊天模型工厂
// ==============================
export class ChatModelFactory extends BaseModelFactory {
  generator(): BaseChatModel {
    const apiKey = process.env.DASHSCOPE_API_KEY;
    
    if (!apiKey) {
      throw new Error('DASHSCOPE_API_KEY 环境变量未配置');
    }
    return new ChatAlibabaTongyi({
      model: ragConfig.chat_model_name,
      streaming: true,
      alibabaApiKey: apiKey,
    });
  }
}

// ==============================
// Ollama 聊天模型工厂
// ==============================
// export class ChatOllamaModelFactory extends BaseModelFactory {
//   generator(): BaseChatModel {
//     return new ChatOllama({
//       model: ragConf.chatOllModelName,
//       streaming: true,
//     });
//   }
// }

// ==============================
// 嵌入模型工厂
// ==============================
export class EmbeddingFactory extends BaseModelFactory {
  generator(): Embeddings {
    const apiKey = process.env.DASHSCOPE_API_KEY;
    
    if (!apiKey) {
      throw new Error('DASHSCOPE_API_KEY 环境变量未配置');
    }
    
    return new AlibabaTongyiEmbeddings({
      modelName: ragConfig.embedding_model_name,
      apiKey: apiKey,
    });
  }
}

// ==============================
// 单例导出（和你 Python 完全一致）
// ==============================
export const chatModel = new ChatModelFactory().generator();
// export const chatOllModel = new ChatOllamaModelFactory().generator();
export const embedModel = new EmbeddingFactory().generator();