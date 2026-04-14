import { tool } from "@langchain/core/tools";
import { apiImageFromText } from "./apiImageGeneration";
import { RagSummarizeService } from "@/rag/ragService";
import { agentConf } from "@/utils/configHandler";
import { logger } from "@/utils/loggerHandler";
import { getAbsPath } from "@/utils/pathTool";
import { apiCity } from "./apiUserLocation";
import { apiWeather } from "./apiWeather";
import * as fs from "fs";
import * as path from "path";

// ==============================
// 类型定义
// ==============================
interface ExternalDataRecord {
  特征: string;
  效率: string;
  耗材: string;
  对比: string;
}

interface ExternalData {
  [userId: string]: {
    [month: string]: ExternalDataRecord;
  };
}

// ==============================
// 全局状态（和你 Python 完全一致）
// ==============================
const rag = new RagSummarizeService();
let externalData: ExternalData = {};

// ==============================
// 工具定义（1:1 对应 Python @tool）
// ==============================

/**
 * 从向量存储中检索参考资料
 */
export const ragSummarize = tool(
  async (query: string) => {
    return rag.ragSummarize(query);
  },
  {
    name: "rag_summarize",
    description: "从向量存储中检索参考资料",
  }
);

/**
 * 获取当前城市天气,消息字符串形式返回
 */
export const getWeather = tool(
  async () => {
    const cityInfo = await apiCity();
    const weather = await apiWeather(cityInfo.locationId);
    return weather;
  },
  {
    name: "get_weather",
    description: "获取当前城市天气,消息字符串形式返回",
  }
);

/**
 * 获取用户所在城市名称，字符串形式返回
 */
export const getUserLocation = tool(
  async () => {
    const cityInfo = await apiCity();
    return JSON.stringify(cityInfo);
  },
  {
    name: "get_user_location",
    description: "获取用户所在城市名称，字符串形式返回",
  }
);

/**
 * 获取用户id
 */
export const getUserId = tool(
  () => {
    return "1003";
  },
  {
    name: "get_user_id",
    description: "获取用户id",
  }
);

/**
 * 获取用户当前月份，字符串形式返回
 */
export const getCurrentMonth = tool(
  () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    return `${year}-${month}`;
  },
  {
    name: "get_current_month",
    description: "获取用户当前月份，字符串形式返回",
  }
);

// ==============================
// 外部数据生成（对应 generate_external_data）
// ==============================
function generateExternalData() {
  if (Object.keys(externalData).length === 0) {
    const externalDataPath = getAbsPath(agentConf.externalDataPath);
    if (!fs.existsSync(externalDataPath)) {
      throw new Error(`外部数据文件${externalDataPath}不存在`);
    }

    const fileContent = fs.readFileSync(externalDataPath, "utf-8");
    const lines = fileContent.split("\n").slice(1); // 跳过表头

    for (const line of lines) {
      if (!line.trim()) continue;
      const arr = line.trim().split(",");
      const userId = arr[0].replace(/"/g, "");
      const feature = arr[1].replace(/"/g, "");
      const efficiency = arr[2].replace(/"/g, "");
      const consumables = arr[3].replace(/"/g, "");
      const comparison = arr[4].replace(/"/g, "");
      const time = arr[5].replace(/"/g, "");

      if (!(userId in externalData)) {
        externalData[userId] = {};
      }
      externalData[userId][time] = {
        特征: feature,
        效率: efficiency,
        耗材: consumables,
        对比: comparison,
      };
    }
  }
}

/**
 * 从外部系统中获取指定用户指定月份的使用记录
 */
export const fetchExternalData = tool(
  (userId: string, month: string) => {
    generateExternalData();
    try {
      const data = externalData[userId][month];
      return JSON.stringify(data);
    } catch (error) {
      logger.warn(`[外部数据] 未找到用户${userId}的${month}月数据`);
      return "";
    }
  },
  {
    name: "fetch_external_data",
    description: "从外部系统中获取指定用户指定月份的使用记录，以字符串形式返回，未检索则返回空字符串",
  }
);

/**
 * 无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息
 */
export const fillContextForReport = tool(
  () => {
    return "fill_context_for_report已调用";
  },
  {
    name: "fill_context_for_report",
    description: "无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息",
  }
);

/**
 * 根据文本描述生成静态图像
 */
// export const generateImageFromText = tool(
//   async (prompt: string, negativePrompt: string = "", size: string = "2048*2048") => {
//     return apiImageFromText(prompt, negativePrompt, size);
//   },
//   {
//     name: "generate_image_from_text",
//     description: "根据文本描述生成静态图像(不支持视频/动图生成),size默认格式为2048*2048,只返回图片链接,不需要任何文字信息",
//   }
// );

// ==============================
// 测试入口（对应 __main__）
// ==============================
if (require.main === module) {
  (async () => {
    const result = await fetchExternalData.invoke({ userId: "1001", month: "2025-01" });
    console.log(result);
  })();
}