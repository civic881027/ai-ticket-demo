import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import TicketList from "./components/TicketList";
import TicketDetail from "./components/TicketDetail";
import TicketCreate from "./components/TicketCreate";
import Login from "./components/Login";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 非保護頁面 */}
        <Route path="/login" element={<Login />} />

        {/* 權限頁面都包在 ProtectedRoute 下 */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<TicketList />} />
          <Route path="/tickets" element={<TicketList />} />
          <Route path="/tickets/create" element={<TicketCreate />} />
          <Route path="/tickets/:id" element={<TicketDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
export default App;
