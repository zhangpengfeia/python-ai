import {
  AIMessageChunk
} from "@langchain/core/messages";
import { createAgent } from "langchain";
import { ChatAlibabaTongyiModel } from "@/agent/model/factory";
import { getFileContent } from '@/agent/utils/cos_file';
import agentMiddleware from "@/agent/createagent/tools/middleware";
import {
  fetchExternalData, fillContextForReport,
  getCurrentMonth,
  getUserId,
  getUserLocation,
  getWeather,
  ragSummarize
} from "@/agent/createagent/tools/agent_tools";
// 上下文类型
interface AgentContext {
  report: boolean;
  isImageGeneration: boolean;
}

export class ReactAgent {
  private agent: any;
  constructor() {
    this.init()
  }
  async init() {
    const systemPrompt = await getFileContent('main_prompt.txt');
    // 完全对齐你 Python 的 create_agent
    this.agent = createAgent({
      model: ChatAlibabaTongyiModel,
      systemPrompt: systemPrompt,
      tools: [
        ragSummarize,
        getWeather,
        getUserLocation,
        getUserId,
        getCurrentMonth,
        fetchExternalData,
        fillContextForReport
        // generateImageFromText
      ],
      middleware: [agentMiddleware]
    });
  }
  // 流式执行（1:1 对应你的 execute_stream）
  async *executeStream(
    query: string
  ): AsyncGenerator<string, void, unknown> {
    const inputDict = {
      messages: [{ role: "user", content: query }]
    };
    const fullContent: string[] = [];
    const context: AgentContext = {
      report: false,
      isImageGeneration: false
    };
    // 流式接收 chunk
    const stream = await this.agent.stream(inputDict, {
      streamMode: "messages",
      configurable: context
    });

    for await (const chunk of stream) {
      // streamMode: "messages" 返回的是 [message, metadata] 数组
      const [message] = Array.isArray(chunk) ? chunk : [chunk, null];
      if (message instanceof AIMessageChunk && message.content) {
        const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
        fullContent.push(content);
        yield content;
      }
    }
    // for await (const chunk of stream) {
    //   // streamMode: "messages" 返回的是 [message, metadata] 数组
    //   const [message, metadata] = Array.isArray(chunk) ? chunk : [chunk, null];
    //
    //   if (message instanceof AIMessageChunk && message.content) {
    //     const content = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);
    //     fullContent.push(content);
    //
    //     // 实时检测是否为图像生成
    //     if (!context.isImageGeneration) {
    //       const markdownMatch = content.match(MARKDOWN_IMAGE_PATTERN);
    //       const urlMatch = content.match(IMAGE_URL_PATTERN);
    //
    //       if (markdownMatch || urlMatch) {
    //         context.isImageGeneration = true;
    //         console.log("\n[检测到图像生成内容]");
    //       }
    //     }
    //   }
    // }
    //
    // const finalOutput = fullContent.join("").trim();
    // const isImageGeneration = context.isImageGeneration;
    // // 图像生成：返回纯 URL（和你逻辑完全一致）
    // // ==============================================
    // if (isImageGeneration) {
    //   console.log("\n[检测到图像生成工具被调用]");
    //
    //   const markdownMatch = finalOutput.match(MARKDOWN_IMAGE_PATTERN);
    //   if (markdownMatch) {
    //     console.log("[提取到 Markdown 图片链接]");
    //     yield markdownMatch[1];
    //     return;
    //   }
    //
    //   const urlMatch = finalOutput.match(IMAGE_URL_PATTERN);
    //   if (urlMatch) {
    //     console.log("[提取到普通图片链接]");
    //     yield urlMatch[0];
    //     return;
    //   }
    // }
    // console.log("\n[普通文本流式输出]");
    // for (const part of fullContent) {
    //   yield part;
    // }
  }
}
async function runTest() {
    const query = '你好,我在那个城市？';
    console.log(`\n用户输入: ${query}\n`);
    console.log('-'.repeat(60));
    const agent = new ReactAgent();
    const resultChunks: string[] = [];
    for await (const chunk of agent.executeStream(query)) {
      resultChunks.push(chunk);
      process.stdout.write(chunk);
    }
    console.log('\n\n完整输出:', resultChunks.join(''));
}
if (require.main === module) {
  runTest()
}
