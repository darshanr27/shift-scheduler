import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ShiftDetail from "./pages/ShiftDetail";
import axios from "axios";

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')
  if(!token) {
    return <Navigate to="/" />;
  }
  return children
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard/>
          </ProtectedRoute>
        } />
        <Route path="/shifts/:id" element={
          <ProtectedRoute>
            <ShiftDetail/>
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}



export default App;