import { Navigate, Outlet } from "react-router-dom";
import { isTokenExpired } from "../utils/jwt";


function ProtectedRoute() {
  const token = localStorage.getItem("token");
  // 判斷 token 是否過期
  if (!token || isTokenExpired(token)) {
    // 可以加個 localStorage.removeItem("token"); 清掉過期 token
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
}
export default ProtectedRoute;