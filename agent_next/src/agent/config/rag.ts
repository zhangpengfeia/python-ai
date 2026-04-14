import {AlibabaTongyiEmbeddingsParams} from "@langchain/community/embeddings/alibaba_tongyi";

interface RagConfig {
  chat_model_name: string;
  embedding_model_name: "multimodal-embedding-v1" | "text-embedding-v1" | "text-embedding-v2" | "text-embedding-v3" | "text-embedding-v4";
}

const ragConfig: RagConfig = {
    chat_model_name: 'MiniMax-M2.1',
    embedding_model_name: 'text-embedding-v1'
};


export default ragConfig