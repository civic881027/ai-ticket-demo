import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, setAuthToken, setRefreshToken } from "../api";
import { Form, Input, Button, message } from "antd";
import { useEffect } from "react";

function Login() {
  useEffect(() => {
    document.title = "登入 - 我的工單系統";
  }, []);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

    const onFinish = async ({ username, password }) => {
    setLoading(true);
    try {
        const res = await api.post("/token/", { username, password });
        setAuthToken(res.data.access);
        setRefreshToken(res.data.refresh);
        message.success("登入成功！");
        navigate("/");
    } catch (err) {
        setAuthToken(null);
        setRefreshToken(null);
        const detail =
            err?.response?.data?.detail ||
            err?.response?.data?.non_field_errors?.[0] ||
            "登入失敗，請確認帳號密碼";
        // 自動改寫指定英文訊息
        const friendlyMsg =
            detail === "No active account found with the given credentials"
            ? "帳號或密碼錯誤，請重新輸入"
            : detail;
        message.error(friendlyMsg)
    }finally {
        setLoading(false);
    }
    };
  return (
    <div style={{ maxWidth: 400, margin: "60px auto" }}>
      <h2>會員登入</h2>
      <Form onFinish={onFinish}>
        <Form.Item label="帳號" name="username" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item label="密碼" name="password" rules={[{ required: true }]}>
          <Input.Password />
        </Form.Item>
        <Form.Item>
          <Button loading={loading} type="primary" htmlType="submit">
            登入
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default Login;
