import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import "./Global.css";
import Layout from "./components/Layout";

function App(props) {
  return (
    <div>
      <Router>
        <Layout {...props}>
          <Routes>
            <Route exact path="/" element={<ChatPage />} />
          </Routes>
        </Layout>
      </Router>
    </div>
  );
}

export default App;
