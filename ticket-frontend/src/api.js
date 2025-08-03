import axios from 'axios';

// 建立 axios 實例
export const api = axios.create({
  baseURL: '/api/',
});

// 初始化時就嘗試從 localStorage 讀取 token 並設定 header
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// 設定 access token 並同步 localStorage
export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('token', token);
  } else {
    delete api.defaults.headers.common['Authorization'];
    localStorage.removeItem('token');
  }
}

// 設定 refresh token（只存 localStorage）
export function setRefreshToken(token) {
  if (token) {
    localStorage.setItem('refresh', token);
  } else {
    localStorage.removeItem('refresh');
  }
}

// 取得 refresh token
function getRefreshToken() {
  return localStorage.getItem('refresh');
}

// 自動攔截器，當 access token 失效(401)時，自動嘗試刷新token
api.interceptors.response.use(
  response => response, // 正常回應
  async error => {
    const originalRequest = error.config;

    if (originalRequest.url && originalRequest.url.includes('/token/')) {
      return Promise.reject(error); // 不處理登入 API 的 401
    }
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const refreshToken = getRefreshToken();

      if (refreshToken) {
        try {
          // 發送 refresh 請求取得新 access token
          const response = await axios.post('/api/token/refresh/', { refresh: refreshToken });

          const newAccessToken = response.data.access;

          // 更新本地存的 access token 和 axios headers
          setAuthToken(newAccessToken);

          // 更新原本的請求 headers
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

          // 重試原本的請求
          return api(originalRequest);
        } catch (refreshError) {
          // refresh token 失效，登出並跳轉登入頁（前端可自行改跳轉）
          setAuthToken(null);
          setRefreshToken(null);
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        // 沒有 refresh token，直接登出
        setAuthToken(null);
        setRefreshToken(null);
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);
