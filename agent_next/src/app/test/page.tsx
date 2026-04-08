"use client"
import {
  AppstoreAddOutlined,
  CloudUploadOutlined,
  CommentOutlined,
  DeleteOutlined,
  EditOutlined,
  EllipsisOutlined,
  FileSearchOutlined,
  GlobalOutlined,
  HeartOutlined,
  PaperClipOutlined,
  ProductOutlined,
  QuestionCircleOutlined,
  ScheduleOutlined,
  ShareAltOutlined,
  SmileOutlined,
  SyncOutlined,
} from '@ant-design/icons';
import type { ActionsFeedbackProps, BubbleListProps, ThoughtChainItemProps } from '@ant-design/x';
import {
  Actions,
  Attachments,
  Bubble,
  Conversations,
  Prompts,
  Sender,
  Think,
  ThoughtChain,
  Welcome,
  XProvider,
} from '@ant-design/x';
import type { ComponentProps } from '@ant-design/x-markdown';
import XMarkdown from '@ant-design/x-markdown';
import {
  useXChat,
  useXConversations,
  XModelMessage,
  XRequest,
  AbstractChatProvider, DefaultMessageInfo, XRequestOptions
} from '@ant-design/x-sdk';
import { Avatar, Button, Flex, type GetProp, message, Pagination, Space } from 'antd';
import { createStyles } from 'antd-style';
import dayjs from 'dayjs';
import React, { useRef, useState } from 'react';
import '@ant-design/x-markdown/themes/light.css';
import '@ant-design/x-markdown/themes/dark.css';
import { BubbleListRef } from '@ant-design/x/es/bubble';
import { useMarkdownTheme } from './Xmarkdown/utils';
import locale from '@/app/utils/locale';

// ==================== Style ====================
const useStyle = createStyles(({ token, css }) => {
  return {
    layout: css`
      width: 100%;
      //height: calc(100vh - 260px);
      height: 100%;
      display: flex;
      background: ${token.colorBgContainer};
      font-family: AlibabaPuHuiTi, ${token.fontFamily}, sans-serif;
    `,
    // side 样式
    side: css`
      background: ${token.colorBgLayout}80;
      width: 280px;
      height: 100%;
      display: flex;
      flex-direction: column;
      padding: 0 12px;
      box-sizing: border-box;
    `,
    logo: css`
      display: flex;
      align-items: center;
      justify-content: start;
      padding: 0 24px;
      box-sizing: border-box;
      gap: 8px;
      margin: 24px 0;

      span {
        font-weight: bold;
        color: ${token.colorText};
        font-size: 16px;
      }
    `,
    conversations: css`
      overflow-y: auto;
      margin-top: 12px;
      padding: 0;
      flex: 1;
      .ant-conversations-list {
        padding-inline-start: 0;
      }
    `,
    sideFooter: css`
      border-top: 1px solid ${token.colorBorderSecondary};
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    `,
    // chat list 样式
    chat: css`
      height: 100%;
      width: calc(100% - 280px);
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      .ant-bubble-content-updating {
        background-image: linear-gradient(90deg, #ff6b23 0%, #af3cb8 31%, #53b6ff 89%);
        background-size: 100% 2px;
        background-repeat: no-repeat;
        background-position: bottom;
      }
    `,
    chatPrompt: css`
      .ant-prompts-label {
        color: #000000e0 !important;
      }
      .ant-prompts-desc {
        color: #000000a6 !important;
        width: 100%;
      }
      .ant-prompts-icon {
        color: #000000a6 !important;
      }
    `,
    chatList: css`
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
    `,
    placeholder: css`
      width: 100%;
      padding: ${token.paddingLG}px;
      box-sizing: border-box;
    `,
    // sender 样式
    sender: css`
      width: 100%;
      max-width: 840px;
    `,
    speechButton: css`
      font-size: 18px;
      color: ${token.colorText} !important;
    `,
    senderPrompt: css`
      width: 100%;
      max-width: 840px;
      margin: 0 auto;
      color: ${token.colorText};
    `,
  };
});

// ==================== Static Config ====================
const HISTORY_MESSAGES: {
  [key: string]: DefaultMessageInfo<ChatMessage>[];
} = {
  'default-1': [
    {
      message: { role: 'user', content: locale.howToQuicklyInstallAndImportComponents },
      status: 'success',
    },
    {
      message: {
        role: 'assistant',
        content: locale.aiMessage_2,
      },
      status: 'success',
    },
  ],
  'default-2': [
    { message: { role: 'user', content: locale.newAgiHybridInterface }, status: 'success' },
    {
      message: {
        role: 'assistant',
        content: locale.aiMessage_1,
      },
      status: 'success',
    },
  ],
};

const DEFAULT_CONVERSATIONS_ITEMS = [
  {
    key: 'default-0',
    label: locale.whatIsAntDesignX,
    group: locale.today,
  }
];

const HOT_TOPICS = {
  key: '1',
  label: locale.hotTopics,
  children: [
    {
      key: '1-1',
      description: locale.whatComponentsAreInAntDesignX,
      icon: <span style={{ color: '#f93a4a', fontWeight: 700 }}>1</span>,
    },
    {
      key: '1-2',
      description: locale.newAgiHybridInterface,
      icon: <span style={{ color: '#ff6565', fontWeight: 700 }}>2</span>,
    },
    {
      key: '1-3',
      description: locale.whatComponentsAreInAntDesignX,
      icon: <span style={{ color: '#ff8f1f', fontWeight: 700 }}>3</span>,
    },
    {
      key: '1-4',
      description: locale.comeAndDiscoverNewDesignParadigm,
      icon: <span style={{ color: '#00000040', fontWeight: 700 }}>4</span>,
    },
    {
      key: '1-5',
      description: locale.howToQuicklyInstallAndImportComponents,
      icon: <span style={{ color: '#00000040', fontWeight: 700 }}>5</span>,
    },
  ],
};

const DESIGN_GUIDE = {
  key: '2',
  label: locale.designGuide,
  children: [
    {
      key: '2-1',
      icon: <HeartOutlined />,
      label: locale.intention,
      description: locale.aiUnderstandsUserNeedsAndProvidesSolutions,
    },
    {
      key: '2-2',
      icon: <SmileOutlined />,
      label: locale.role,
      description: locale.aiPublicPersonAndImage,
    },
    {
      key: '2-3',
      icon: <CommentOutlined />,
      label: locale.chat,
      description: locale.howAICanExpressItselfWayUsersUnderstand,
    },
    {
      key: '2-4',
      icon: <PaperClipOutlined />,
      label: locale.interface,
      description: locale.aiBalances,
    },
  ],
};

const SENDER_PROMPTS: GetProp<typeof Prompts, 'items'> = [
  {
    key: '1',
    description: locale.upgrades,
    icon: <ScheduleOutlined />,
  },
  {
    key: '2',
    description: locale.components,
    icon: <ProductOutlined />,
  },
  {
    key: '3',
    description: locale.richGuide,
    icon: <FileSearchOutlined />,
  },
  {
    key: '4',
    description: locale.installationIntroduction,
    icon: <AppstoreAddOutlined />,
  },
];

const THOUGHT_CHAIN_CONFIG = {
  loading: {
    title: locale.modelIsRunning,
    status: 'loading',
  },
  updating: {
    title: locale.modelIsRunning,
    status: 'loading',
  },
  success: {
    title: locale.modelExecutionCompleted,
    status: 'success',
  },
  error: {
    title: locale.executionFailed,
    status: 'error',
  },
  abort: {
    title: locale.aborted,
    status: 'abort',
  },
};

// ==================== Context ====================
const ChatContext = React.createContext<{
  onReload?: ReturnType<typeof useXChat>['onReload'];
  setMessage?: ReturnType<typeof useXChat<ChatMessage>>['setMessage'];
}>({});

// ==================== Sub Component ====================

const ThinkComponent = React.memo((props: ComponentProps) => {
  const [title, setTitle] = React.useState(`${locale.deepThinking}...`);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (props.streamStatus === 'done') {
      setTitle(locale.completeThinking);
      setLoading(false);
    }
  }, [props.streamStatus]);

  return (
    <Think title={title} loading={loading}>
      {props.children}
    </Think>
  );
});

const Footer: React.FC<{
  id?: string | number;
  content: string;
  status?: string;
  extraInfo?: ChatMessage['extraInfo'];
}> = ({ id, content, extraInfo, status }) => {
  const context = React.useContext(ChatContext);
  const Items = [
    {
      key: 'pagination',
      actionRender: <Pagination simple total={1} pageSize={1} />,
    },
    {
      key: 'retry',
      label: locale.retry,
      icon: <SyncOutlined />,
      onItemClick: () => {
        if (id) {
          context?.onReload?.(id, {
            userAction: 'retry',
          });
        }
      },
    },
    {
      key: 'copy',
      actionRender: <Actions.Copy text={content} />,
    },
    {
      key: 'audio',
      actionRender: (
        <Actions.Audio
          onClick={() => {
            message.info(locale.isMock);
          }}
        />
      ),
    },
    {
      key: 'feedback',
      actionRender: (
        <Actions.Feedback
          styles={{
            liked: {
              color: '#f759ab',
            },
          }}
          value={extraInfo?.feedback || 'default'}
          key="feedback"
          onChange={(val) => {
            if (id) {
              context?.setMessage?.(id, () => ({
                extraInfo: {
                  feedback: val,
                },
              }));
              message.success(`${id}: ${val}`);
            } else {
              message.error('has no id!');
            }
          }}
        />
      ),
    },
  ];
  return status !== 'updating' && status !== 'loading' ? (
    <div style={{ display: 'flex' }}>{id && <Actions items={Items} />}</div>
  ) : null;
};

// 类型定义：自定义聊天系统的输入输出和消息结构
// Type definitions: custom chat system input/output and message structure
interface CustomInput {
  messages: Array<{
    role: 'user' | 'assistant' | 'system';
    content: string;
  }>;
  stream?: boolean;
  model?: string;
}

interface CustomOutput {
  data: {
    content: string;
    attachments?: {
      name: string;
      url: string;
      type: string;
      size?: number;
    }[];
  };
}
// ==================== Type ====================
interface ChatMessage extends CustomMessage {
  extraInfo?: {
    feedback: ActionsFeedbackProps['value'];
  };
}

interface CustomMessage extends XModelMessage{
  content: string;
  role: 'user' | 'assistant' | 'system';
}

// 自定义Provider实现：继承AbstractChatProvider实现自定义聊天逻辑
class CustomProvider<
  ChatMessage extends CustomMessage = CustomMessage,
  Input extends CustomInput = CustomInput,
  Output extends CustomOutput = CustomOutput,
> extends AbstractChatProvider<ChatMessage, Input, Output> {
  // 转换请求参数：将用户输入消息，转换为参数标准格式
  transformParams(
    requestParams: Partial<Input>,
    options: XRequestOptions<Input, Output, ChatMessage>,
  ): Input {
    if (typeof requestParams !== 'object') {
      throw new Error('requestParams must be an object');
    }
    return {
      messages: requestParams.messages || [],
      stream: requestParams.stream ?? options?.params?.stream ?? true,
      model: requestParams.model ?? options?.params?.model ?? 'qwen2.5-7b-instruct',
    } as Input;
  }

  // 转换本地消息：将请求参数转换为本地消息格式
  // Transform local message: convert request parameters to local message format
  transformLocalMessage(requestParams: Partial<Input>): ChatMessage {
    const lastMessage = requestParams.messages?.[requestParams.messages.length - 1];
    return {
      content: lastMessage?.content || '',
      role: lastMessage?.role || 'user',
    } as ChatMessage;
  }

  // 转换消息：处理流式响应数据
  // Transform message: process streaming response data
  transformMessage(info: any): ChatMessage {
    const { originMessage, chunk } = info || {};
    // 处理完成标记或空数据
    // Handle completion marker or empty data
    if (!chunk || !chunk?.data || chunk?.data?.includes('[DONE]')) {
      return {
        content: originMessage?.content || '',
        role: 'assistant'
      } as ChatMessage;
    }

    try {
      // 处理流式数据：解析JSON格式
      // Process streaming data: parse JSON format
      const data = JSON.parse(chunk.data);
      const content = originMessage?.content || '';

      // 合并附件信息，避免数据丢失
      // Merge attachment information to avoid data loss
      const existingAttachments = originMessage?.attachments || [];
      const newAttachments: CustomMessage['attachments'] = data.attachments || [];
      const mergedAttachments = [...existingAttachments];

      // 只添加新的附件，避免重复
      // Only add new attachments to avoid duplicates
      newAttachments?.forEach((newAttach: NonNullable<CustomMessage['attachments']>[0]) => {
        if (!mergedAttachments.some((existing) => existing.url === newAttach.url)) {
          mergedAttachments.push(newAttach);
        }
      });

      return {
        content: `${content}${data.content || ''}`,
        role: 'assistant'
      } as ChatMessage;
    } catch (_error) {
      // 如果解析失败，直接使用原始数据
      // If parsing fails, use raw data directly
      return {
        content: `${originMessage?.content || ''}${chunk.data || ''}`,
        role: 'assistant'
      } as ChatMessage;
    }
  }
}

// 从后端获取会话历史消息
const getApiHistoryMessages = async (conversationKey: string): Promise<DefaultMessageInfo<ChatMessage>[]> => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/chat/message/history/${conversationKey}?limit=50`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('获取历史消息失败');
    }

    const data = await response.json();
    
    // 后端返回格式为 { code: 200, data: { messages: [...], total: number } }
    if (data.code === 200 && data.data?.messages && Array.isArray(data.data.messages)) {
      console.log(data.data.messages)
      return data.data.messages.map((msg: any) => ({
        message: {
          role: msg.role as 'user' | 'assistant',
          content: msg.content,
        },
        status: 'success' as const,
      }));
    }
  } catch (error) {
    console.error('获取历史消息失败:', error);
  }
  return [];
};

const getRole = (className: string): BubbleListProps['role'] => ({
  assistant: {
    placement: 'start',
    header: (_, { status }) => {
      const config = THOUGHT_CHAIN_CONFIG[status as keyof typeof THOUGHT_CHAIN_CONFIG];
      return config ? (
        <ThoughtChain.Item
          style={{
            marginBottom: 8,
          }}
          status={config.status as ThoughtChainItemProps['status']}
          variant="solid"
          icon={<GlobalOutlined />}
          title={config.title}
        />
      ) : null;
    },
    footer: (content, { status, key, extraInfo }) => (
      <Footer
        content={content}
        status={status}
        extraInfo={extraInfo as ChatMessage['extraInfo']}
        id={key as string}
      />
    ),
    contentRender: (content: any, { status }) => {
      const newContent = content.replace(/\n\n/g, '<br/><br/>');
      return (
        <XMarkdown
          paragraphTag="div"
          components={{
            think: ThinkComponent,
          }}
          className={className}
          streaming={{
            hasNextChunk: status === 'updating',
            enableAnimation: true,
          }}
        >
          {newContent}
        </XMarkdown>
      );
    },
  },
  user: { placement: 'end' },
});

const Independent: React.FC = () => {
  const { styles } = useStyle();
  // ==================== State ====================

  // 使用自定义Provider：创建自定义聊天提供者实例
  // Use custom provider: create custom chat provider instance
  const [provider] = React.useState(
    new CustomProvider<CustomMessage, CustomInput, CustomOutput>({
      request: XRequest('http://127.0.0.1:8000/api/v1/chat/stream', {
        manual: true,
        params: {
          messages: [],
          stream: true,
          session_id: '',
          model: 'qwen2.5-7b-instruct',
        },
      }),
    }),
  );
  const {
    conversations,
    activeConversationKey,
    setActiveConversationKey,
    addConversation,
    setConversations,
  } = useXConversations({
    defaultConversations: DEFAULT_CONVERSATIONS_ITEMS,
    defaultActiveConversationKey: DEFAULT_CONVERSATIONS_ITEMS[0].key,
  });

  const getApiDefaultConversations = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/chat/session/list?limit=50', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('获取会话列表失败');
    }

    const data = await response.json();

    // 后端返回格式为 { code: 200, data: { sessions: [...], total: number } }
    if (data.code === 200 && data.data?.sessions && Array.isArray(data.data.sessions)) {
      const conversations = data.data.sessions.map((item: any) => ({
        key: item.session_id,
        label: item.session_name || '未命名会话',
        group: item.group || locale.today,
      }));
      setConversations(conversations);
      // 设置默认激活的会话
      if (conversations.length > 0 && !activeConversationKey) {
        setActiveConversationKey(conversations[0].key);
      }
      return conversations;
    }
  } catch (error) {
    console.error('获取会话列表失败:', error);
    messageApi.error('获取会话列表失败，请稍后重试');
  }
  return [];
};

  // 创建新会话
  const handleCreateNewConversation = async () => {
    try {
      // 如果当前有未保存的消息，提示用户
      if (messages.length === 0) {
        messageApi.error(locale.itIsNowANewConversation);
        return;
      }

      // 调用后端接口创建新会话
      const response = await fetch('http://127.0.0.1:8000/api/v1/chat/session/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_name: `${locale.newConversation} ${conversations.length + 1}`,
        }),
      });

      if (!response.ok) {
        throw new Error('创建会话失败');
      }

      const data = await response.json();
      
      if (data.code === 200 && data.data?.session_id) {
        const newSessionId = data.data.session_id;
        
        // 添加新会话到列表
        addConversation({
          key: newSessionId,
          label: data.data.session_name || `${locale.newConversation} ${conversations.length + 1}`,
          group: locale.today,
        });
        
        // 激活新会话
        setActiveConversationKey(newSessionId);
        
        messageApi.success('创建新会话成功');
      } else {
        throw new Error('创建会话失败');
      }
    } catch (error) {
      console.error('创建新会话失败:', error);
      messageApi.error('创建新会话失败，请稍后重试');
    }
  };

  // 组件挂载时加载会话列表
  React.useEffect(() => {
    getApiDefaultConversations();
  }, []);

  const [className] = useMarkdownTheme();
  const [messageApi, contextHolder] = message.useMessage();
  const [attachmentsOpen, setAttachmentsOpen] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState<GetProp<typeof Attachments, 'items'>>([]);

  const [inputValue, setInputValue] = useState('');

  const listRef = useRef<BubbleListRef>(null);
  const senderRef = useRef<GetProp<typeof Sender>>(null);

  // ==================== Runtime ====================

  // 获取历史消息列表：从服务器加载历史聊天记录
  const getDefaultMessages: (info: {
    conversationKey?: string;
  }) => Promise<DefaultMessageInfo<ChatMessage>[]> = async ({ conversationKey }) => {
    if (!conversationKey) return [];
    
    // 如果是默认会话，使用本地数据
    if (conversationKey.startsWith('default-')) {
      return HISTORY_MESSAGES[conversationKey] || [];
    }
    
    // 否则从后端异步获取历史消息
    try {
      const historyMessages = await getApiHistoryMessages(conversationKey);
      return historyMessages;
    } catch (error) {
      console.error('加载历史消息失败:', error);
      return [];
    }
  };

  const { onRequest, messages, isDefaultMessagesRequesting, isRequesting, abort, onReload, setMessage } = useXChat({
    provider: provider,
    conversationKey: activeConversationKey,
    defaultMessages: getDefaultMessages,
    requestPlaceholder: {
        content: locale.noData,
        role: 'assistant' as const,
    },
    requestFallback:  (_, { error, errorInfo, messageInfo }) => {
      if (error.name === 'AbortError') {
        return {
          content: messageInfo?.message?.content || locale.requestAborted,
          role: 'assistant' as const,
        };
      }
      return {
        content: errorInfo?.error?.message || locale.requestFailed,
        role: 'assistant' as const,
      };
    },
  });

  // 当会话切换时，清空输入框
  React.useEffect(() => {
    senderRef.current?.clear();
  }, [activeConversationKey]);

  // ==================== Event ====================
  const onSubmit = (val: string) => {
    if (!val) return;
    onRequest({
      messages: [{ role: 'user', content: val }],
    });
    listRef.current?.scrollTo({ top: 'bottom' });
  };

  // ==================== Nodes ====================
  const chatSide = (
    <div className={styles.side}>
      {/* 🌟 Logo */}
      <div className={styles.logo}>
        <img
          src="https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*eco6RrQhxbMAAAAAAAAAAAAADgCCAQ/original"
          draggable={false}
          alt="logo"
          width={24}
          height={24}
        />
        <span>Ai智能教育助手</span>
      </div>
      {/* 🌟 会话管理 */}
      <Conversations
        creation={{
          onClick: handleCreateNewConversation,
        }}
        items={conversations.map(({ key, label, ...other }) => ({
          key,
          label: key === activeConversationKey ? `[${locale.curConversation}]${label}` : label,
          ...other,
        }))}
        className={styles.conversations}
        activeKey={activeConversationKey}
        onActiveChange={(key) => {
          setActiveConversationKey(key);
        }}
        groupable
        styles={{ item: { padding: '0 8px' } }}
        menu={(conversation) => ({
          items: [
            {
              label: locale.rename,
              key: 'rename',
              icon: <EditOutlined />,
              onClick: async () => {
                try {
                  const response = await fetch(`http://127.0.0.1:8000/api/v1/chat/session/${conversation.key}/rename`, {
                    method: 'PUT',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                      session_name: conversation.label.replace(/^\[.*?\]/, ''), // 移除前缀标签
                    }),
                  });

                  if (!response.ok) {
                    throw new Error('重命名失败');
                  }

                  const data = await response.json();
                  if (data.code === 200) {
                    messageApi.success('重命名成功');
                    // 刷新会话列表
                    getApiDefaultConversations();
                  }
                } catch (error) {
                  console.error('重命名失败:', error);
                  messageApi.error('重命名失败，请稍后重试');
                }
              },
            },
            {
              label: locale.delete,
              key: 'delete',
              icon: <DeleteOutlined />,
              danger: true,
              onClick: async () => {
                try {
                  // 调用后端删除接口
                  const response = await fetch(`http://127.0.0.1:8000/api/v1/chat/session/${conversation.key}`, {
                    method: 'DELETE',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                  });

                  if (!response.ok) {
                    throw new Error('删除失败');
                  }

                  const data = await response.json();
                  if (data.code === 200) {
                    // 从前端列表中移除
                    const newList = conversations.filter((item) => item.key !== conversation.key);
                    const newKey = newList?.[0]?.key;
                    setConversations(newList);
                    
                    if (conversation.key === activeConversationKey) {
                      setActiveConversationKey(newKey);
                    }
                    
                    messageApi.success('删除成功');
                  }
                } catch (error) {
                  console.error('删除失败:', error);
                  messageApi.error('删除失败，请稍后重试');
                }
              },
            },
          ],
        })}
      />

      <div className={styles.sideFooter}>
        <Avatar size={24} />
        <Button type="text" icon={<QuestionCircleOutlined />} />
      </div>
    </div>
  );

  const chatList = (
    <div className={styles.chatList}>
      {messages?.length ? (
        /* 🌟 消息列表 */
        <Bubble.List
          ref={listRef}
          items={messages?.map((i) => ({
            ...i.message,
            key: i.id,
            status: i.status,
            loading: i.status === 'loading',
            extraInfo: i.extraInfo,
          }))}
          styles={{
            root: {
              maxWidth: 940,
            },
          }}
          role={getRole(className)}
        />
      ) : (
        <Flex
          vertical
          style={{
            maxWidth: 840,
          }}
          gap={16}
          align="center"
          className={styles.placeholder}
        >
          <Welcome
            style={{
              width: '100%',
            }}
            variant="borderless"
            icon="https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*s5sNRo5LjfQAAAAAAAAAAAAADgCCAQ/fmt.webp"
            title={locale.welcome}
            description={locale.welcomeDescription}
            extra={
              <Space>
                <Button icon={<ShareAltOutlined />} />
                <Button icon={<EllipsisOutlined />} />
              </Space>
            }
          />
          <Flex
            gap={16}
            justify="center"
            style={{
              width: '100%',
            }}
          >
            <Prompts
              items={[HOT_TOPICS]}
              styles={{
                list: { height: '100%' },
                item: {
                  flex: 1,
                  backgroundImage: 'linear-gradient(123deg, #e5f4ff 0%, #efe7ff 100%)',
                  borderRadius: 12,
                  border: 'none',
                },
                subItem: { padding: 0, background: 'transparent' },
              }}
              onItemClick={(info) => {
                console.log(222)
                onSubmit(info.data.description as string);
              }}
              className={styles.chatPrompt}
            />

            <Prompts
              items={[DESIGN_GUIDE]}
              styles={{
                item: {
                  flex: 1,
                  backgroundImage: 'linear-gradient(123deg, #e5f4ff 0%, #efe7ff 100%)',
                  borderRadius: 12,
                  border: 'none',
                },
                subItem: { background: '#ffffffa6' },
              }}
              onItemClick={(info) => {
                console.log(111)
                onSubmit(info.data.description as string);
              }}
              className={styles.chatPrompt}
            />
          </Flex>
        </Flex>
      )}
    </div>
  );
  const senderHeader = (
    <Sender.Header
      title={locale.uploadFile}
      open={attachmentsOpen}
      onOpenChange={setAttachmentsOpen}
      styles={{ content: { padding: 0 } }}
    >
      <Attachments
        beforeUpload={() => false}
        items={attachedFiles}
        onChange={(info) => setAttachedFiles(info.fileList)}
        placeholder={(type) =>
          type === 'drop'
            ? { title: locale.dropFileHere }
            : {
                icon: <CloudUploadOutlined />,
                title: locale.uploadFiles,
                description: locale.clickOrDragFilesToUpload,
              }
        }
      />
    </Sender.Header>
  );
  const chatSender = (
    <Flex
      vertical
      gap={12}
      align="center"
      style={{
        margin: 8,
      }}
    >
      {/* 🌟 提示词 */}
      {!attachmentsOpen && (
        <Prompts
          items={SENDER_PROMPTS}
          onItemClick={(info) => {
            onSubmit(info.data.description as string);
          }}
          styles={{
            item: { padding: '6px 12px' },
          }}
          className={styles.senderPrompt}
        />
      )}
      {/* 🌟 输入框 */}
      <Sender
        ref={senderRef}
        value={inputValue}
        header={senderHeader}
        onSubmit={() => {
          onSubmit(inputValue);
          setInputValue('');
        }}
        onChange={setInputValue}
        onCancel={() => {
          abort();
        }}
        prefix={
          <Button
            type="text"
            icon={<PaperClipOutlined style={{ fontSize: 18 }} />}
            onClick={() => setAttachmentsOpen(!attachmentsOpen)}
          />
        }
        loading={isRequesting}
        className={styles.sender}
        allowSpeech
        placeholder={locale.askOrInputUseSkills}
      />
    </Flex>
  );

  // ==================== Render =================

  return (
    <XProvider locale={locale}>
      <ChatContext.Provider value={{ onReload, setMessage }}>
        {contextHolder}
        <div className={styles.layout}>
          {chatSide}
          <div className={styles.chat}>
            {chatList}
            {chatSender}
          </div>
        </div>
      </ChatContext.Provider>
    </XProvider>
  );
};

export default Independent;