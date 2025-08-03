import { useState, useEffect } from "react";
import { api } from "../api";
import { useNavigate } from "react-router-dom";
import { Form, Input, Button, Select, message, Modal } from "antd";
import { jwtDecode } from "jwt-decode";

const { Option } = Select;


function TicketCreate() {
  const [users, setUsers] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        // 根據你的 JWT 結構取用戶 id 欄位名稱
        setCurrentUserId(decoded.user_id);
      } catch (e) {
        console.warn("Decode token failed:", e);
      }
    }
  }, []);
  // 讀取使用者資料
  useEffect(() => {
    document.title = "建立工單 - 我的工單系統";
    const fetchUsers = async () => {
      try {
        const res = await api.get("users/");
        setUsers(res.data['results']); 
      } catch (e) {
        message.error("載入使用者列表失敗");
      }
    };

    fetchUsers();
  }, []);

  const [form] = Form.useForm();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  


  useEffect(() => {
  if (users.length > 0 && currentUserId) {
    const exists = users.find(u => u.id === currentUserId);
    if (exists) {
      form.setFieldsValue({ assigned_to: currentUserId });
    }
  }
}, [users, currentUserId, form]);
  // 當用戶送出表單
  const onFinish = async (values) => {
    // 判斷可空欄位是否皆空，決定是否呈現 AI 使用提示
    const isCategoryEmpty = !values.category || values.category.trim() === "";
    const isPriorityEmpty = !values.priority || values.priority === "";

    if (isCategoryEmpty || isPriorityEmpty) {
      // 提示用戶 AI 生成中，並確認是否繼續
      Modal.confirm({
        title: "未指定分類或優先級",
        content: "您未指定分類及優先級，系統將使用 AI 生成。是否繼續？",
        okText: "是，開始使用 AI",
        cancelText: "否，返回修改",
        onOk: () => submitWithAILoading(values),
      });
    } else {
      // 有任一欄非空，直接提交
      submitWithAILoading(values);
    }
  };

  // 包裝提交函式，同時帶有 loading 與異常處理
  const submitWithAILoading = async (values) => {
    try {
      setLoading(true);
      message.loading({ content: "正在使用 AI 創建中...", key: "createAI", duration: 0 });
      const res = await api.post("tickets/", values);
      message.success({ content: "建立成功！", key: "createAI" });
      navigate(`/tickets/${res.data.id}`);
    } catch (error) {
      message.error({ content: "建立失敗，請確認欄位。", key: "createAI" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 600, margin: "auto" }}>
      <h2>新建工單</h2>
      <Form form={form} onFinish={onFinish} layout="vertical">
        {/* 標題必填，使用中文提示 */}
        <Form.Item
          label="標題"
          name="title"
          rules={[{ required: true, message: "請輸入標題" }]}
          validateTrigger={["onBlur", "onSubmit"]}
        >
          <Input />
        </Form.Item>

        {/* 描述必填，使用中文提示 */}
        <Form.Item
          label="描述"
          name="description"
          rules={[{ required: true, message: "請輸入描述" }]}
          validateTrigger={["onBlur", "onSubmit"]}
        >
          <Input.TextArea rows={4} />
        </Form.Item>

        {/* 人工分類 可空 */}
        <Form.Item label="人工分類（可空）" name="category">
          <Input />
        </Form.Item>

        {/* 優先級 可空 */}
        <Form.Item label="優先級（可空）" name="priority">
          <Select allowClear placeholder="請選擇優先級">
            <Option value="low">低</Option>
            <Option value="medium">中</Option>
            <Option value="high">高</Option>
            <Option value="urgent">緊急</Option>
          </Select>
        </Form.Item>

        <Form.Item label="負責人" name="assigned_to" >
          <Select
            allowClear
            placeholder="請選擇負責人"
            loading={users.length === 0} // 用戶沒載入完成時顯示等待
            optionFilterProp="children"
            showSearch
            filterOption={(input, option) =>
              option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
            }
          >
            {users.map(user => (
              <Option key={user.id} value={user.id}>
                {user.username}
              </Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            建立
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate(-1)} disabled={loading}>
            取消
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default TicketCreate;
