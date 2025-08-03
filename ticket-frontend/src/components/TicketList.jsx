import { useEffect, useState } from "react";
import { api } from "../api";
import { Table, Button } from "antd";
import { useNavigate } from "react-router-dom";
import LogoutButton from "./LogoutButton";



function TicketList() {
  const [tickets, setTickets] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "工單列表 - 我的工單系統";
    api.get("tickets/")
      .then(res => {
        // 如果有分頁資料就用 results，否則直接用陣列
        const data = Array.isArray(res.data)
          ? res.data
          : res.data.results || [];
        setTickets(data);
      })
      .catch(() => setTickets([]));
  }, []);


const columns = [
  {
    title: '標題',
    dataIndex: 'title',
    sorter: (a, b) => a.title.localeCompare(b.title),
  },
  {
    title: '分類',
    dataIndex: 'category',
    sorter: (a, b) => a.category.localeCompare(b.category),
  },
  {
    title: '優先級',
    dataIndex: 'priority',
    sorter: (a, b) => a.priority.localeCompare(b.priority),
  },
  {
    title: '狀態',
    dataIndex: 'status',
    sorter: (a, b) => a.status.localeCompare(b.status),
  },
  {
    title: '建立時間',
    dataIndex: 'created_at',
    sorter: (a, b) => new Date(a.created_at) - new Date(b.created_at),
    render: d => new Date(d).toLocaleString()
  },
  {
    title: '檢視',
    render: (_, row) => (
      <Button onClick={() => navigate(`/tickets/${row.id}`)}>詳情</Button>
    )
  }
];

  return (
    <>
      <div style={{ textAlign: "right" }}>
        <LogoutButton />
      </div>
      <div style={{padding:24}}>
        <h2>工單列表</h2>
        <Button type="primary" onClick={() => navigate('/tickets/create')}>新增工單</Button>
        <Table columns={columns} dataSource={tickets} rowKey="id" style={{marginTop:16}} />
      </div>
    </>
  );

}
export default TicketList;
