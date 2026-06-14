/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 * 注意:敏感信息(API Key)请通过项目根目录的 .env 文件注入,
 *       不要硬编码到源码中。参考 .env.example。
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI 兼容接口地址(阿里云 DashScope)
  apiEndpoint: import.meta.env.VITE_AI_API_ENDPOINT || 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',

  // API Key(从 .env 注入,切勿提交真实 key)
  apiKey: import.meta.env.VITE_AI_API_KEY || '',

  // 使用的模型
  model: import.meta.env.VITE_AI_MODEL || 'qwen3-max-preview',
}
