import { useEffect, useState } from 'react';
import {
  FiChevronDown,
  FiChevronUp,
  FiDatabase,
  FiEdit,
  FiFileText,
  FiImage,
  FiMoon,
  FiSun,
  FiUsers
} from 'react-icons/fi';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';
import { useTheme } from '../context/ThemeContext';
import {
  adminLogout,
  clearCache,
  deleteChatAdmin,
  deleteLog,
  deleteMedia,
  disableUser,
  enableUser,
  getAdminAnalytics,
  getAllMedia,
  getAllMemories,
  getAllUsers,
  getSystemData,
  updateUser
} from '../middleware/adminMiddleware';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const adminData = JSON.parse(localStorage.getItem('admin_data'));
  const { theme, toggleTheme } = useTheme();
  const [showMoreGraphs, setShowMoreGraphs] = useState(false);
  const [openSection, setOpenSection] = useState({
    users: true,
    memories: false,
    media: false,
    data: false
  });

  /* backend data */

  const [analyticsData, setAnalyticsData] = useState(null);
  const [userData, setUserData] = useState([]);
  const [memoryData, setMemoryData] = useState([]);
  const [mediaData, setMediaData] = useState([]);
  const [dataControls, setDataControls] = useState([]);

  /* loading */

  const [loading, setLoading] = useState(false);
  const toggleSection = (section) => {
    setOpenSection((prev) => ({
      ...prev,
      [section]: !prev[section]
    }));
  };
  /* fetch analytics */

  const fetchAnalytics = async () => {
    try {
      const response = await getAdminAnalytics();
      setAnalyticsData(response);
    } catch (error) {
      console.error(error);
    }
  };

  /* fetch users */

  const fetchUsers = async () => {
    try {
      const response = await getAllUsers();
      setUserData(response?.users || []);
    } catch (error) {
      console.error(error);
    }
  };

  /* fetch memories */

  const fetchMemories = async () => {
    try {
      const response = await getAllMemories();
      setMemoryData(response?.memories || []);
    } catch (error) {
      console.error(error);
    }
  };

  /*user edit*/
  const [editingUserId, setEditingUserId] = useState(null);
  const [editForm, setEditForm] = useState({
    username: '',
    email: ''
  });

  const handleUpdateUser = async (userId) => {
    try {
      await updateUser(userId, editForm);
      setEditingUserId(null);
      fetchUsers();
    } catch (error) {
      console.error(error);
    }
  };

  /* fetch media */

  const fetchMedia = async () => {
    try {
      const response = await getAllMedia();
      setMediaData(response?.media || []);
    } catch (error) {
      console.error(error);
    }
  };

  /* fetch system data */

  const fetchSystemData = async () => {
    try {
      const response = await getSystemData();
      setDataControls(response?.data_controls || []);
    } catch (error) {
      console.error(error);
    }
  };

  /* initial load + auto refreshed */

  useEffect(() => {
    const loadDashboard = async () => {
      setLoading(true);
      await Promise.all([
        fetchAnalytics(),
        fetchUsers(),
        fetchMemories(),
        fetchMedia(),
        fetchSystemData()
      ]);
      setLoading(false);
    };
    loadDashboard();

    const interval = setInterval(() => {
      loadDashboard();
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  /* graph data */

  const userGraphData = analyticsData
    ? analyticsData.user_analytics.graph_data.labels.map((label, index) => ({
        name: label,
        value: analyticsData.user_analytics.graph_data.values[index]
      }))
    : [];

  const voiceGraphData = analyticsData
    ? analyticsData.ai_metrics.voice_ai.graph_data.labels.map((label, index) => ({
        name: label,
        value: analyticsData.ai_metrics.voice_ai.graph_data.values[index]
      }))
    : [];

  const textGraphData = analyticsData
    ? analyticsData.ai_metrics.text_ai.graph_data.labels.map((label, index) => ({
        name: label,
        value: analyticsData.ai_metrics.text_ai.graph_data.values[index]
      }))
    : [];

  const imageGraphData = analyticsData
    ? analyticsData.ai_metrics.image_ai.graph_data.labels.map((label, index) => ({
        name: label,
        value: analyticsData.ai_metrics.image_ai.graph_data.values[index]
      }))
    : [];

  const systemMetricsData = analyticsData
    ? [
        {
          name: 'CPU',
          value: analyticsData.system_metrics.cpu_usage_percent
        },
        {
          name: 'Memory',
          value: analyticsData.system_metrics.memory_usage_percent
        },
        {
          name: 'Disk',
          value: analyticsData.system_metrics.disk_usage_percent
        },
        {
          name: 'Uptime (sec)',
          value: analyticsData.system_metrics.backend_uptime_seconds
        }
      ]
    : [];

  const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981'];
  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="admin-header">
          <h1>Loading Dashboard...</h1>
        </div>
      </div>
    );
  }
  return (
    <div className="admin-dashboard">
      {/* theme toggle */}

      <div className="admin-theme-toggle" onClick={toggleTheme}>
        {theme === 'light' ? (
          <FiMoon className="admin-theme-icon" />
        ) : (
          <FiSun className="admin-theme-icon sun" />
        )}
      </div>

      {/* header */}

      <div className="admin-header">
        <h1>Welcome Back! {adminData?.name || 'Admin'}</h1>
        <p>Monitor ReMIND system analytics and controls.</p>
      </div>

      {/* analytics */}

      <div className="admin-section-title">Analytics</div>
      <div className="analytics-grid">
        {/* user analytics */}

        <div className="analytics-card">
          <h3>User Analytics</h3>

          <div
            style={{
              width: '100%',
              height: 260
            }}
          >
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={userGraphData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={90}
                  fill="#6366f1"
                  label
                >
                  {userGraphData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p
            style={{
              fontSize: '13px',
              opacity: 0.7,
              marginTop: '-6px',
              marginBottom: '10px'
            }}
          >
            Total Users: {analyticsData?.user_analytics?.total_users || 0}
          </p>
        </div>

        {/* system metrics */}

        <div className="analytics-card">
          <h3>System Metrics</h3>
          <div
            style={{
              width: '100%',
              height: 260
            }}
          >
            <ResponsiveContainer>
              <BarChart data={systemMetricsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* extra ai graphs */}

        {showMoreGraphs && (
          <>
            {/* voice ai metrics */}

            <div className="analytics-card">
              <h3>Voice AI Metrics</h3>
              <div
                style={{
                  width: '100%',
                  height: 260
                }}
              >
                <ResponsiveContainer>
                  <BarChart data={voiceGraphData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* text ai metrics */}

            <div className="analytics-card">
              <h3>Text AI Metrics</h3>

              <div
                style={{
                  width: '100%',
                  height: 260
                }}
              >
                <ResponsiveContainer>
                  <BarChart data={textGraphData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#06b6d4" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* image ai metrics */}

            <div className="analytics-card">
              <h3>Image AI Metrics</h3>
              <div
                style={{
                  width: '100%',
                  height: 260
                }}
              >
                <ResponsiveContainer>
                  <BarChart data={imageGraphData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#10b981" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}
      </div>

      {/* view more */}

      <button className="view-more-btn" onClick={() => setShowMoreGraphs(!showMoreGraphs)}>
        {showMoreGraphs ? 'View Less' : 'View More'}
      </button>

      {/* user panel */}

      <div className="admin-section-title">User Panel</div>

      {/* user controls */}

      <div className="panel-card">
        <div className="panel-header" onClick={() => toggleSection('users')}>
          <div className="panel-title">
            <FiUsers size={20} />
            User Controls
          </div>
          {openSection.users ? <FiChevronUp /> : <FiChevronDown />}
        </div>
        {openSection.users && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>USER ID</th>
                  <th>USERNAME</th>
                  <th>EMAIL</th>
                  <th>STATUS</th>
                  <th>STATE</th>
                  <th>UPTIME</th>
                  <th>CONTROL</th>
                </tr>
              </thead>
              <tbody>
                {[...userData]
                  .sort((a, b) => a.user_id - b.user_id)
                  .map((user, index) => (
                    <tr key={index}>
                      <td>{user.user_id}</td>

                      {/* username */}

                      <td>
                        {editingUserId === user.user_id ? (
                          <input
                            value={editForm.username}
                            onChange={(e) =>
                              setEditForm({
                                ...editForm,
                                username: e.target.value
                              })
                            }
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                handleUpdateUser(user.user_id);
                              }
                            }}
                            autoFocus
                          />
                        ) : (
                          <>
                            {user.username}
                            <FiEdit
                              size={15}
                              className="edit-icon"
                              onClick={() => {
                                setEditingUserId(user.user_id);
                                setEditForm({
                                  username: user.username,
                                  email: user.email
                                });
                              }}
                            />
                          </>
                        )}
                      </td>
                      {/* email */}
                      <td>
                        {editingUserId === user.user_id ? (
                          <input
                            value={editForm.email}
                            onChange={(e) =>
                              setEditForm({
                                ...editForm,
                                email: e.target.value
                              })
                            }
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                handleUpdateUser(user.user_id);
                              }
                            }}
                          />
                        ) : (
                          <>
                            {user.email}
                            <FiEdit
                              size={15}
                              className="edit-icon"
                              onClick={() => {
                                setEditingUserId(user.user_id);
                                setEditForm({
                                  username: user.username,
                                  email: user.email
                                });
                              }}
                            />
                          </>
                        )}
                      </td>
                      <td>
                        <span
                          className={user.status === 'active' ? 'status-active' : 'status-inactive'}
                        >
                          {user.status}
                        </span>
                      </td>
                      <td>{user.state}</td>
                      <td>{user.uptime}</td>
                      <td>
                        <button
                          className={
                            user.status?.toLowerCase() === 'inactive' ? 'enable-btn' : 'delete-btn'
                          }
                          onClick={async () => {
                            try {
                              if (user.status?.toLowerCase() === 'inactive') {
                                await enableUser(user.user_id);
                              } else {
                                await disableUser(user.user_id);
                              }
                              await fetchUsers();
                              await fetchAnalytics();
                            } catch (error) {
                              console.error(error);
                            }
                          }}
                        >
                          {user.status?.toLowerCase() === 'inactive' ? 'Enable' : 'Disable'}
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      {/* memory controls */}

      <div className="panel-card">
        <div className="panel-header" onClick={() => toggleSection('memories')}>
          <div className="panel-title">
            <FiDatabase size={20} />
            Memory Controls
          </div>
          {openSection.memories ? <FiChevronUp /> : <FiChevronDown />}
        </div>
        {openSection.memories && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Message ID</th>
                  <th>Chat ID</th>
                  <th>Message Count</th>
                  <th>Media Attached</th>
                  <th>Media ID</th>
                  <th>Pipeline Used</th>
                  <th>Latency</th>
                  <th>Cost</th>
                  <th>Ping</th>
                  <th>Control</th>
                </tr>
              </thead>
              <tbody>
                {[...memoryData]
                  .filter(
                    (memory) => memory.message_id && memory.chat_id && memory.message_count > 0
                  )
                  .sort((a, b) => (a.message_id || 0) - (b.message_id || 0))
                  .map((memory, index) => {
                    const renderValue = (value) => {
                      if (value === null || value === undefined || value === '') {
                        return '-';
                      }
                      if (typeof value === 'object') {
                        return JSON.stringify(value);
                      }
                      return value;
                    };

                    return (
                      <tr key={index}>
                        <td>{renderValue(memory.message_id)}</td>
                        <td>{renderValue(memory.chat_id)}</td>
                        <td>{renderValue(memory.message_count)}</td>
                        <td>
                          {memory.media_attached === true
                            ? 'True'
                            : memory.media_attached === false
                            ? 'False'
                            : '-'}
                        </td>
                        <td>{renderValue(memory.media_id)}</td>
                        <td>{renderValue(memory.pipeline_used)}</td>
                        <td>{renderValue(memory.latency)}</td>
                        <td>{renderValue(memory.cost)}</td>
                        <td>{renderValue(memory.ping)}</td>
                        <td>
                          <button
                            className="delete-btn"
                            disabled={!memory.chat_id}
                            onClick={async () => {
                              try {
                                await deleteChatAdmin(memory.chat_id);
                                fetchMemories();
                              } catch (error) {
                                console.error(error);
                                alert('Failed to delete message.');
                              }
                            }}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </div>
        )}
      </div>
      {/* media controls */}

      <div className="panel-card">
        <div className="panel-header" onClick={() => toggleSection('media')}>
          <div className="panel-title">
            <FiImage size={20} />
            Media Controls
          </div>
          {openSection.media ? <FiChevronUp /> : <FiChevronDown />}
        </div>
        {openSection.media && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Media ID</th>
                  <th>Attached Chat ID</th>
                  <th>Media Type</th>
                  <th>Media Format</th>
                  <th>Processed</th>
                  <th>Control</th>
                </tr>
              </thead>
              <tbody>
                {mediaData.map((media, index) => (
                  <tr key={index}>
                    <td>{media.media_id}</td>
                    <td>{media.attached_chat_id}</td>
                    <td>{media.media_type}</td>
                    <td>{media.media_format}</td>
                    <td>{media.processed ? 'True' : 'False'}</td>
                    <td>
                      <button
                        className="delete-btn"
                        onClick={async () => {
                          try {
                            await deleteMedia(media.media_id);

                            fetchMedia();
                          } catch (error) {
                            console.error(error);
                          }
                        }}
                      >
                        Delete
                      </button>{' '}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* data controls */}

      <div className="panel-card">
        <div className="panel-header" onClick={() => toggleSection('data')}>
          <div className="panel-title">
            <FiFileText size={20} />
            Data Controls
          </div>
          {openSection.data ? <FiChevronUp /> : <FiChevronDown />}
        </div>
        {openSection.data && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Log ID</th>
                  <th>Log Info</th>
                  <th>Cache Hit</th>
                  <th>Log Control</th>
                </tr>
              </thead>

              <tbody>
                {[...dataControls]
                  .sort((a, b) => a.log_id - b.log_id)
                  .map((data, index) => (
                    <tr key={index}>
                      {/* log id */}

                      <td>{data.log_id}</td>

                      {/* log info */}

                      <td>{data.log_info}</td>

                      {/* cache hit */}

                      <td>{data.cache_hit ? 'True' : 'False'}</td>

                      {/* delete log */}

                      <td>
                        <button
                          className="delete-btn"
                          onClick={async () => {
                            try {
                              await deleteLog(data.log_id);
                              fetchSystemData();
                            } catch (error) {
                              console.error(error);
                            }
                          }}
                        >
                          Delete Log
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      {/* bottom buttons */}

      <div className="admin-bottom-buttons">
        {/* clear cache */}

        <button
          className="cache-btn"
          onClick={async () => {
            try {
              await clearCache();
              alert('Cache cleared successfully.');
            } catch (error) {
              console.error(error);
              alert('Failed to clear cache.');
            }
          }}
        >
          Clear Cache
        </button>

        {/* logout button */}

        <button
          className="logout-btn"
          onClick={async () => {
            try {
              await adminLogout();
              localStorage.removeItem('admin_token');
              localStorage.removeItem('admin_data');
              window.location.href = '/admin-portal';
            } catch (error) {
              console.error(error);
            }
          }}
        >
          Log out
        </button>
      </div>
    </div>
  );
};
export default AdminDashboard;
