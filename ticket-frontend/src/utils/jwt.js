import { jwtDecode } from "jwt-decode";

export function isTokenExpired(token) {
  if (!token) return true;
  try {
    const payload = jwtDecode(token);
    return payload.exp * 1000 < Date.now();
  } catch {
    return true;
  }
}