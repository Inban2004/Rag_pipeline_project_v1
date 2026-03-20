import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import ChatBot from "./components/ChatBot";

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
    <ChatBot />
  </BrowserRouter>
);

export default App;
