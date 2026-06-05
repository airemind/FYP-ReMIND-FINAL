import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ChatArea from '../components/ChatArea';
import MessageInput from '../components/MessageInput';
import Sidebar from '../components/Sidebar';
import Topbar from '../components/Topbar';
import { useAuth } from '../context/AuthContext';
import { createChat, deleteChatById, getChats, renameChatById } from '../middleware/chatMiddleware';
import { processMemory } from '../middleware/memoryMiddleware';
import { getMessages } from '../middleware/messageMiddleware';
import { enhanceImage } from '../middleware/imageEnhancementMiddleware';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const pathParts = location.pathname.split('/');
  const routeChatId = pathParts[3] ? Number(pathParts[3]) : null;
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [chatsLoaded, setChatsLoaded] = useState(false);
  const [error, setError] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const toggleMobileSidebar = () => {
    setIsMobileSidebarOpen((prev) => !prev);
  };

  /* normalize chat */

  const normalizeChat = (chat) => ({
    ...chat,
    id: chat?.id || chat?.chat_id || chat?._id,
    messages: Array.isArray(chat?.messages) ? chat.messages : []
  });

  /* normalize message */

  const normalizeMessage = (message) => ({
    ...message,
    id: message?.id || message?.message_id || message?._id,
    content: message?.content || '',
    sender: message?.sender || 'user',
    role: message?.sender || 'user',
    type: message?.message_type || 'text',
    caption: message?.caption || '',
    enhancedImage: message?.enhanced_image || '',
    generatedAudio: message?.generated_audio || '',
    transcript: message?.transcript || '',
    emotion: message?.emotion || '',
    tones: message?.tones || [],
    retrievedContext: message?.retrieved_context || [],
    isEnhanced: !!message?.enhanced_image,
    enhancedDownloadUrl: message?.enhanced_image || null
  });

  /* Load chats on mount */
  useEffect(() => {
    const fetchChats = async () => {
      try {
        setLoading(true);
        setError('');

        const data = await getChats();
        const safeChats = Array.isArray(data) ? data : [];
        const normalizedChats = safeChats.map(normalizeChat);

        setChats(normalizedChats);
        setChatsLoaded(true);
        if (!routeChatId && normalizedChats.length > 0) {
          const firstChatId = normalizedChats[0].id;
          setActiveChatId(firstChatId);
          navigate(
            `/dashboard/chat/${firstChatId}?name=${encodeURIComponent(
              normalizedChats[0].title || 'Chat'
            )}`
          );
        }
      } catch (error) {
        console.error(error);
        setError('Failed to load chats.');
      } finally {
        setLoading(false);
      }
    };

    fetchChats();
  }, [navigate, routeChatId]);

  /* sync route chat */

  useEffect(() => {
    if (routeChatId && routeChatId !== activeChatId) {
      setActiveChatId(routeChatId);
    }
  }, [routeChatId, activeChatId]);

  useEffect(() => {
    const loadMessages = async () => {
      if (!chatsLoaded) return;
      if (!activeChatId) return;
      try {
        const data = await getMessages(activeChatId);
        const safeMessages = Array.isArray(data) ? data : [];
        const normalizedMessages = safeMessages.map(normalizeMessage);
        setChats((prev) =>
          prev.map((chat) =>
            Number(chat.id) === Number(activeChatId)
              ? {
                  ...chat,
                  messages: normalizedMessages
                }
              : chat
          )
        );
      } catch (error) {
        console.error('Failed to load messages:', error);
      }
    };
    loadMessages();
  }, [activeChatId, chatsLoaded]);

  /* create new chat */

  const createNewChat = async () => {
    try {
      const newChat = await createChat();
      if (!newChat) {
        throw new Error('Invalid chat response.');
      }
      const normalizedChat = normalizeChat(newChat);
      setChats((prev) => [normalizedChat, ...prev]);
      setActiveChatId(normalizedChat.id);
      navigate(
        `/dashboard/chat/${normalizedChat.id}?name=${encodeURIComponent(
          normalizedChat.title || 'New Chat'
        )}`
      );
    } catch (error) {
      console.error(error);
      alert('Failed to create chat.');
    }
  };

  /* delete chat */

  const deleteChat = async (id) => {
    try {
      await deleteChatById(id);
      const updated = chats.filter((chat) => chat.id !== id);
      setChats(updated);
      if (updated.length > 0) {
        setActiveChatId(updated[0].id);
        navigate(
          `/dashboard/chat/${updated[0].id}?name=${encodeURIComponent(updated[0].title || 'Chat')}`
        );
      } else {
        setActiveChatId(null);
        navigate('/dashboard');
      }
    } catch (error) {
      console.error(error);
      alert('Failed to delete chat.');
    }
  };

  /* rename chat */

  const renameChat = async (id, newTitle) => {
    try {
      const response = await renameChatById(id, {
        title: newTitle
      });

      if (!response?.success) return;

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === id
            ? {
                ...chat,
                title: newTitle
              }
            : chat
        )
      );
    } catch (error) {
      console.error(error);

      alert('Failed to rename chat.');
    }
  };

  /* send message */

  const sendMessage = async (payload) => {
    try {
      setIsThinking(true);

      /* attachments */

      const imageAttachment = payload.files?.find((f) => f.fileType === 'image');
      const audioAttachment = payload.files?.find((f) => f.fileType === 'audio');

      /* show user message */

      const userMessage = {
        id: Date.now(),
        role: 'user',
        type: payload.files?.length > 0 ? 'memory' : 'text',
        content: payload.text || '',

        /* image */

        ...(imageAttachment && {
          enhancedImage: URL.createObjectURL(imageAttachment.file),
          originalImageUrl: URL.createObjectURL(imageAttachment.file),
          originalImageFile: imageAttachment.file,
          isEnhancing: false,
          isEnhanced: false,
          enhancedDownloadUrl: null
        }),

        /* audio */

        ...(audioAttachment && {
          generatedAudio: URL.createObjectURL(audioAttachment.file)
        })
      };

      /* show user message */

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: [...(chat.messages || []), userMessage]
              }
            : chat
        )
      );

      /* Memory api */

      const response = await processMemory({
        userId: user?.id,
        userPrompt: payload.text || '',
        chatId: activeChatId,
        imageFile: imageAttachment?.file || null,
        audioFile: audioAttachment?.file || null
      });

      /* assistant response */

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        type: 'memory',
        content:
          response?.final_memory_response ||
          response?.text_ai?.response ||
          'Memory reconstructed successfully.',

        /* image */

        caption: response?.image_ai?.caption || '',
        enhancedImage: response?.image_ai?.enhanced_url || response?.image_ai?.original_url || '',
        originalImageUrl: response?.image_ai?.original_url || '',
        originalImageFile: imageAttachment?.file || null,
        isEnhancing: false,
        isEnhanced: false,
        enhancedDownloadUrl: null,

        /* audio */

        transcript: response?.voice_ai?.transcript || '',
        emotion: response?.voice_ai?.emotion || '',
        tones: response?.voice_ai?.tones || [],
        generatedAudio: response?.voice_ai?.generated_audio_url || '',

        /* memory */

        retrievedContext:
          response?.text_ai?.retrieved_context ||
          response?.voice_ai?.retrieved_context ||
          response?.image_ai?.retrieved_context ||
          []
      };

      /* add ai response */

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: [...(chat.messages || []), assistantMessage]
              }
            : chat
        )
      );
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.error ||
          error?.response?.data?.detail ||
          error?.message ||
          'Memory reconstruction failed.'
      );
    } finally {
      setIsThinking(false);
    }
  };

  /* enhance image */

  const handleEnhanceImage = async (messageId) => {
    try {
      /* loading */
      setChats((prev) =>
        prev.map((chat) => ({
          ...chat,
          messages: chat.messages.map((msg) =>
            msg.id === messageId
              ? {
                  ...msg,
                  isEnhancing: true
                }
              : msg
          )
        }))
      );

      /* find message */

      const currentChat = chats.find((chat) => Number(chat.id) === Number(activeChatId));
      const targetMessage = currentChat?.messages.find((msg) => msg.id === messageId);

      if (!targetMessage?.originalImageFile) {
        throw new Error('Original image not found.');
      }

      /* api */

      const result = await enhanceImage(targetMessage.originalImageFile);
      console.log('Enhancement result:', result);

      /* update */

      setChats((prev) =>
        prev.map((chat) => ({
          ...chat,
          messages: chat.messages.map((msg) =>
            msg.id === messageId
              ? {
                  ...msg,
                  isEnhancing: false,
                  isEnhanced: true,
                  /* show enhance image in chat */
                  enhancedImage:
                    result?.enhanced_url || result?.enhanced_image || msg.enhancedImage,
                  /* downlaod enhance image */
                  enhancedDownloadUrl: result?.enhanced_url || result?.enhanced_image || null
                }
              : msg
          )
        }))
      );
    } catch (error) {
      console.error(error);

      /* reset */

      setChats((prev) =>
        prev.map((chat) => ({
          ...chat,
          messages: chat.messages.map((msg) =>
            msg.id === messageId
              ? {
                  ...msg,
                  isEnhancing: false
                }
              : msg
          )
        }))
      );

      alert('Image enhancement failed.');
    }
  };

  /*chat selection */

  const handleChatSelect = (id) => {
    if (id !== activeChatId) {
      setActiveChatId(id);
    }

    const selectedChat = chats.find((chat) => chat.id === id);
    navigate(`/dashboard/chat/${id}?name=${encodeURIComponent(selectedChat?.title || 'Chat')}`);
  };
  /* active chat */

  const activeChat = chats.find((chat) => Number(chat.id) === Number(activeChatId));

  /* loading */

  if (loading) {
    return <div className="dashboard-loading">Loading chats...</div>;
  }

  /*error */

  if (error) {
    return <div className="dashboard-error">{error}</div>;
  }

  /* main ui*/

  return (
    <div className="dashboard">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        setActiveChatId={handleChatSelect}
        createNewChat={createNewChat}
        deleteChat={deleteChat}
        renameChat={renameChat}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        isCollapsed={isSidebarCollapsed}
        toggleSidebar={() => setIsSidebarCollapsed((prev) => !prev)}
        isMobileOpen={isMobileSidebarOpen}
        closeMobileSidebar={() => setIsMobileSidebarOpen(false)}
        toggleMobileSidebar={toggleMobileSidebar}
      />
      <div className="main-area">
        <Topbar toggleMobileSidebar={toggleMobileSidebar} />
        <ChatArea
          activeChat={activeChat}
          isThinking={isThinking}
          handleEnhanceImage={handleEnhanceImage}
        />
        <MessageInput sendMessage={sendMessage} activeChat={activeChat} />
        <div className="dashboard-disclaimer">
          ReMIND can make mistakes. Verify important information and uploaded content before relying
          on AI-generated responses.
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
