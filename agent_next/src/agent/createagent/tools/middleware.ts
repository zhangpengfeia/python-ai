// ✅ 全部从 langchain 根包导入（官方明确支持）
import {
    WrapToolCallHook,
  beforeModel,
  dynamicPrompt,
  ModelRequest,
  ToolCallRequest,
  Runtime,
  AgentState,
} from "langchain";
import { ToolMessage } from "@langchain/core/messages";
import { Command } from "langchain/types";
import { loadSystemPrompts, loadReportPrompts } from "@/utils/promptLoader";
import { logger } from "@/utils/loggerHandler";

// ==============================
// 工具执行监控中间件
// ==============================
export const monitorTool = wrapToolCall(
  async (
    request: ToolCallRequest,
    handler: (request: ToolCallRequest) => Promise<ToolMessage | Command>
  ): Promise<ToolMessage | Command> => {
    logger.info(`[tool monitor]执行工具：${request.toolCall.name}`);
    logger.info(`[tool monitor]传入参数：${JSON.stringify(request.toolCall.args)}`);

    try {
      const result = await handler(request);
      logger.info(`[tool monitor]工具${request.toolCall.name}调用成功`);

      // 确保 runtime context 存在
      const runtime = request.runtime as Runtime;
      if (!runtime.context) {
        runtime.context = {};
      }

      if (request.toolCall.name === "fill_context_for_report") {
        runtime.context.report = true;
      }

      if (request.toolCall.name === "generate_image_from_text") {
        runtime.context.is_image_generation = true;
      }

      return result;
    } catch (e) {
      logger.error(`工具${request.toolCall.name}调用失败，原因：${String(e)}`);
      throw e;
    }
  }
);

// ==============================
// 模型调用前日志中间件
// ==============================
export const logBeforeModel = beforeModel(
  (state: AgentState, runtime: Runtime): void => {
    logger.info(`[log_before_model]即将调用模型，带有${state.messages.length}条消息。`);

    const lastMessage = state.messages[state.messages.length - 1];
    if (lastMessage) {
      logger.debug(
        `[log_before_model]${lastMessage.constructor.name} | ${lastMessage.content.toString().trim()}`
      );
    }
  }
);

// ==============================
// 动态提示词切换中间件
// ==============================
export const reportPromptSwitch = dynamicPrompt(
  (request: ModelRequest): string => {
    const isReport = request.runtime?.context?.report ?? false;
    return isReport ? loadReportPrompts() : loadSystemPrompts();
  }
);

// ==============================
// 统一导出
// ==============================
export const middleware = [monitorTool, logBeforeModel, reportPromptSwitch];