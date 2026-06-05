import { useMemo, useState } from 'react';
import {
  FiChevronLeft,
  FiChevronRight,
  FiEdit2,
  FiMenu,
  FiPlus,
  FiSearch,
  FiTrash2,
  FiX
} from 'react-icons/fi';
import '../styles/Sidebar.css';

const Sidebar = ({
  chats,
  activeChatId,
  setActiveChatId,
  createNewChat,
  deleteChat,
  renameChat,
  searchTerm,
  setSearchTerm,
  isCollapsed,
  toggleSidebar,

  /* mobile view */
  isMobileOpen = false,
  closeMobileSidebar = () => {},
  toggleMobileSidebar = () => {}
}) => {
  const [editingId, setEditingId] = useState(null);
  const [tempTitle, setTempTitle] = useState('');
  const [chatToDelete, setChatToDelete] = useState(null);
  const filteredChats = useMemo(() => {
    const validChats = chats.filter((chat) => chat && typeof chat === 'object');
    if (!searchTerm) return validChats;
    return validChats.filter((chat) =>
      (chat.title || '').toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [chats, searchTerm]);

  const handleRename = (id) => {
    if (!tempTitle.trim()) return;
    renameChat(id, tempTitle.trim());
    setEditingId(null);
  };

  const handleChatSelect = (chatId) => {
    setActiveChatId(chatId);
    if (window.innerWidth <= 768) {
      closeMobileSidebar();
    }
  };

  const handleCreateChat = () => {
    createNewChat();
    if (window.innerWidth <= 768) {
      closeMobileSidebar();
    }
  };

  return (
    <>
      {/* mobile overlay */}

      {isMobileOpen && window.innerWidth <= 768 && (
        <div className="sidebar-mobile-overlay" onClick={closeMobileSidebar} />
      )}

      {/* sidebar */}

      <div
        className={`sidebar ${isCollapsed ? 'collapsed' : ''} ${isMobileOpen ? 'mobile-open' : ''}`}
      >
        {/* toggle button */}

        <div
          className="sidebar-toggle"
          onClick={() => {
            if (window.innerWidth <= 768) {
              toggleMobileSidebar();
            } else {
              toggleSidebar();
            }
          }}
        >
          {window.innerWidth <= 768 ? (
            isMobileOpen ? (
              <FiX />
            ) : (
              <FiMenu />
            )
          ) : isCollapsed ? (
            <FiChevronRight />
          ) : (
            <FiChevronLeft />
          )}
        </div>

        {/* collapsed mode */}

        {isCollapsed && window.innerWidth > 768 ? (
          <div className="sidebar-collapsed-icons">
            <div className="sidebar-icon tooltip-wrapper" onClick={handleCreateChat}>
              <FiPlus />
            </div>
          </div>
        ) : (
          <>
            {/* header */}

            <div className="sidebar-header">ReMIND</div>

            {/* search */}

            <div className="search-box">
              <FiSearch />

              <input
                placeholder="Search chats"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            {/* new chat button */}

            <button className="new-chat-btn" onClick={handleCreateChat}>
              <FiPlus />
              <span>New Chat</span>
            </button>

            {/* chat list */}

            <div className="chat-list">
              {filteredChats.map((chat) => (
                <div
                  key={chat.id}
                  className={`chat-item ${activeChatId === chat.id ? 'active' : ''}`}
                  onClick={() => handleChatSelect(chat.id)}
                >
                  {editingId === chat.id ? (
                    <input
                      value={tempTitle}
                      autoFocus
                      onChange={(e) => setTempTitle(e.target.value)}
                      onBlur={() => handleRename(chat.id)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          handleRename(chat.id);
                        }
                      }}
                    />
                  ) : (
                    <>
                      <span className="chat-title">{chat.title || 'New Chat'}</span>
                      <div className="chat-actions">
                        <FiEdit2
                          onClick={(e) => {
                            e.stopPropagation();
                            setEditingId(chat.id);
                            setTempTitle(chat.title);
                          }}
                        />
                        <FiTrash2
                          className="delete-icon"
                          onClick={(e) => {
                            e.stopPropagation();
                            setChatToDelete(chat.id);
                          }}
                        />
                      </div>
                    </>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* delete overlay */}

      {chatToDelete && (
        <div className="delete-modal-overlay" onClick={() => setChatToDelete(null)}>
          <div className="delete-modal" onClick={(e) => e.stopPropagation()}>
            <div className="delete-modal-header">
              <h3>Delete Chat</h3>
            </div>
            <div className="delete-modal-body">
              <p>Are you sure you want to delete this chat?</p>
              <span className="delete-warning">This action cannot be undone.</span>
            </div>
            <div className="delete-modal-actions">
              <button className="cancel-btn" onClick={() => setChatToDelete(null)}>
                Cancel
              </button>
              <button
                className="confirm-delete-btn"
                onClick={() => {
                  deleteChat(chatToDelete);
                  setChatToDelete(null);
                }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
export default Sidebar;
