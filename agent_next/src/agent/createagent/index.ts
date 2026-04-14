import {
  BaseMessage,
  AIMessageChunk,
} from "@langchain/core/messages";
import { createAgent } from "langchain";
import { chatModel } from "@/agent/model/factory";
import { getFileContent } from '@/agent/utils/cos_file';
import {
  ragSummarize,
  getWeather,
  getUserLocation,
  getUserId,
  fetchExternalData,
  fillContextForReport,
  getCurrentMonth,
  generateImageFromText
} from "@/agent/createagent/tools/agent_tools";
import {
  monitorTool,
  logBeforeModel,
  reportPromptSwitch
} from "@/agent/tools/middleware";

// 图片正则（和你 Python 完全一样）
const IMAGE_URL_PATTERN = /https?:\/\/[^\s)]+?\.(png|jpg|jpeg|gif|bmp|webp)(\?[^\s)]*)?/i;
const MARKDOWN_IMAGE_PATTERN = /!\[.*?\]\((https?:\/\/[^\s)]+?\.(png|jpg|jpeg|gif|bmp|webp)(\?[^\s)]*)?\)/i;

// 上下文类型
interface AgentContext {
  report: boolean;
  isImageGeneration: boolean;
  [key: string]: any;
}

export class ReactAgent {
  private agent: any;

  async init() {
    const systemPrompt = await getFileContent('main_prompt.txt');

    // 完全对齐你 Python 的 create_agent
    this.agent = createAgent({
      model: chatModel,
      systemPrompt: systemPrompt,
      tools: [
        ragSummarize,
        getWeather,
        getUserLocation,
        getUserId,
        getCurrentMonth,
        fetchExternalData,
        fillContextForReport,
        generateImageFromText
      ],
      middleware: [monitorTool, logBeforeModel, reportPromptSwitch]
    });
  }

  // 流式执行（1:1 对应你的 execute_stream）
  async *executeStream(
    query: string
  ): AsyncGenerator<string, void, unknown> {
    const inputDict = {
      messages: [{ role: "user", content: query }] as BaseMessage[]
    };

    const fullContent: string[] = [];
    const context: AgentContext = {
      report: false,
      isImageGeneration: false
    };

    // 流式接收 chunk
    const stream = await this.agent.stream(inputDict, {
      streamMode: "messages",
      context
    });

    for await (const chunk of stream) {
      const token = chunk;

      if (token instanceof AIMessageChunk && token.content) {
        fullContent.push(token.content);
      }
    }

    const finalOutput = fullContent.join("").trim();
    const isImageGeneration = context.isImageGeneration;

    // ==============================================
    // 图像生成：返回纯 URL（和你逻辑完全一致）
    // ==============================================
    if (isImageGeneration) {
      console.log("\n[检测到图像生成工具被调用]");

      const markdownMatch = finalOutput.match(MARKDOWN_IMAGE_PATTERN);
      if (markdownMatch) {
        console.log("[提取到 Markdown 图片链接]");
        yield markdownMatch[1];
        return;
      }

      const urlMatch = finalOutput.match(IMAGE_URL_PATTERN);
      if (urlMatch) {
        console.log("[提取到普通图片链接]");
        yield urlMatch[0];
        return;
      }
    }

    // ==============================================
    // 普通文本流式返回
    // ==============================================
    console.log("\n[普通文本流式输出]");
    for (const part of fullContent) {
      yield part;
    }
  }
}