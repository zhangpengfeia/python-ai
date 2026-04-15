import {AlibabaTongyiEmbeddingsParams} from "@langchain/community/embeddings/alibaba_tongyi";

interface RagConfig {
  chat_model_name: string;
  embedding_model_name: "multimodal-embedding-v1" | "text-embedding-v1" | "text-embedding-v2" | "text-embedding-v3" | "text-embedding-v4";
}

const ragConfig: RagConfig = {
    chat_model_name: 'qwen3-max-2026-01-23',
    embedding_model_name: 'text-embedding-v1'
};


export default ragConfig