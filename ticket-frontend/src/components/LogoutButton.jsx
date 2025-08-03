import { useNavigate } from "react-router-dom";
import { setAuthToken, setRefreshToken } from "../api";
import { Button } from "antd";

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    setAuthToken(null);      // 清除 access token
    setRefreshToken(null);   // 清除 refresh token
    navigate("/login");      // 跳轉到登入頁
  };

  return (
    <Button onClick={handleLogout} type="link" danger>
      登出
    </Button>
  );
}

export default LogoutButton;
