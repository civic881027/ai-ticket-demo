import { useEffect, useState } from "react";
import { api } from "../api";
import { useParams, useNavigate } from "react-router-dom";
import { Button, Input, List, Tag, message, Card, Space, Divider, Row, Col } from "antd";

function TicketDetail() {
  const [ticket, setTicket] = useState(null);
  const [reply, setReply] = useState("");
  const [aiLoading, setAILoading] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();

  // 讀取工單資料
  useEffect(() => {
    document.title = "工單詳情 - 我的工單系統";
    api.get(`tickets/${id}/`).then(res => setTicket(res.data));
  }, [id]);

  // 人工回覆
  const handleManualReply = () => {
    if (!reply.trim()) {
      message.warning("回覆不得為空");
      return;
    }
    api.post(`tickets/${id}/reply/`, { response_text: reply }).then(() => {
      setReply("");
      api.get(`tickets/${id}/`).then(res => setTicket(res.data));
      message.success("回覆完成！");
    });
  };

  // AI回覆
  const handleAIReply = () => {
    setAILoading(true);  // 按下時設 loading true
    api.post(`tickets/${id}/ai-response/`)
      .then(() => {
        api.get(`tickets/${id}/`).then(res => setTicket(res.data));
        message.success("AI 回覆完成！");
      })
      .catch(() => {
        message.error("AI 回覆失敗，請稍後再試");
      })
      .finally(() => {
        setAILoading(false);  // 完成後取消 loading
      });
  };

  if (!ticket) return <div>讀取中...</div>;

  return (
    <div style={{ maxWidth: 750, margin: "40px auto", padding: "24px", background: "#fff", borderRadius: "12px", boxShadow: "0 3px 18px rgba(0,0,0,0.04)" }}>
      {/* 工單主資訊 */}
      <Card bordered={false} style={{ marginBottom: 32 }}>
        <Row>
          <Col flex="auto">
            <h2 style={{ margin: 0 }}>{ticket.title}</h2>
            <Space>
              <Tag color="blue">{ticket.status}</Tag>
              <Tag color="magenta">{ticket.priority}</Tag>
              <Tag color="volcano">{ticket.category}</Tag>
            </Space>
            <div style={{ fontSize: 14, color: "#808080", margin: "8px 0" }}>
              建立時間：{new Date(ticket.created_at).toLocaleString()}
            </div>
          </Col>
          <Col flex="none">
            <Button onClick={() => navigate('/tickets')}>回列表</Button>
          </Col>
        </Row>
        <Divider style={{ margin: "10px 0" }} />
        <div><b>描述：</b>{ticket.description}</div>
        {(ticket.ai_suggested_category || ticket.ai_suggested_priority) && (
          <div style={{ color: "#868686", marginTop: 8 }}>
            AI 建議：{ticket.ai_suggested_category || "-"}（優先級 {ticket.ai_suggested_priority || "-" }）
          </div>
        )}
      </Card>

      {/* 所有回覆 */}
      <Card
        title={<span style={{ fontWeight: 600 }}>回覆紀錄</span>}
        style={{ marginBottom: 32 }}
        bodyStyle={{ paddingTop: 0 }}
      >
        <List
          dataSource={ticket.responses}
          locale={{emptyText: "目前尚無回覆"}}
          renderItem={res => (
            <List.Item>
              <Space align="baseline">
                {res.is_ai_generated
                  ? <Tag color="purple">AI</Tag>
                  : <Tag color="green">人工</Tag>
                }
                <b>{res.created_by.username}</b>
                <span style={{color:"#888"}}>{new Date(res.created_at).toLocaleString()}</span>
              </Space>
              <div style={{ marginLeft: "12px", flex: 1 }}>{res.response_text}</div>
            </List.Item>
          )}
        />
      </Card>

      {/* 回覆輸入框與操作 */}
      <Card
        title="新增回覆"
        bordered={false}
        bodyStyle={{ paddingTop: 0 }}
      >
        <Input.TextArea
          rows={3}
          placeholder="請輸入回覆內容"
          value={reply}
          onChange={e => setReply(e.target.value)}
        />
        <Space style={{ marginTop: 16 }}>
          <Button onClick={handleManualReply} type="primary" shape="round">
            發送人工回覆
          </Button>
          <Button onClick={handleAIReply} shape="round" loading={aiLoading} disabled={aiLoading}>
            {aiLoading ? "產生中..." : "產生 AI 回覆"}
          </Button>
        </Space>
      </Card>
    </div>
  );
}

export default TicketDetail;
