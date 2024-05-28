import BotBubble from "../components/BotBubble";
import UserBubble from "../components/UserBubble";
import { useState, useRef, useEffect } from "react";
import { clearData, sendUserMessage } from "../service/BotService";
import "./ChatPage.css";
import SettingsModal from "../components/SettingsModal";
import { changeName, getUsername } from "../service/UserService";
import {
  addHistoryToDb,
  deleteHistoryFromDb,
  getAllHistoriesFromDb,
  getHistoryByIdFromDb,
  updateHistoryInDb,
} from "../service/HistoryService";
import HistoryBubble from "../components/HistoryBubble";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [username, setUsername] = useState();
  const [userProfileHovered, setUserProfileHovered] = useState(false);
  const [histories, setHistories] = useState([]);
  const [currentHistory, setCurrentHistory] = useState();
  const [addHistoryHover, setAddHistoryHover] = useState(false);
  const messagesEndRef = useRef(null);

  const sendMessage = () => {
    if (!newMessage.trim()) return;
    let message = {
      type: "user",
      text: newMessage,
      timestamp: getCurrentTimeFormatted(),
    };
    setNewMessage("");

    let updatedMessages = [...messages, message];
    setMessages(updatedMessages);
    let botMessages = updatedMessages.filter((m) => m.type === "bot");
    let lastBotMessage = "Empty";
    if (botMessages.length > 0) {
      lastBotMessage = botMessages[botMessages.length - 1];
    }
    sendUserMessage({
      message: {
        user: newMessage,
        lastBot:
          lastBotMessage == "Empty" ? lastBotMessage : lastBotMessage.text,
      },
    }).then((response) => {
      let botMessage = {
        type: "bot",
        text: response.data.response,
        timestamp: getCurrentTimeFormatted(),
        isLoading: false,
      };
      let currentMessages = [...updatedMessages, botMessage];
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      if (currentHistory == null) {
        addHistory(currentMessages);
      } else {
        updateHistory(currentMessages);
      }
    });
  };

  const getCurrentTimeFormatted = () => {
    const now = new Date();
    return now.toLocaleTimeString("sk-SK", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const handleScroll = (e) => {
    const isNearBottom =
      e.target.scrollHeight - e.target.scrollTop - e.target.clientHeight < 1;
    setShowScrollButton(!isNearBottom);
  };

  const getCurrentUsername = () => {
    getUsername().then((response) => {
      setUsername(response.data.username);
    });
  };

  const changeCurrentName = (name) => {
    changeName({ username: name }).then((response) => {
      setUsername(response.data.username);
    });
  };

  const getAllHistories = () => {
    getAllHistoriesFromDb().then((response) => {
      setHistories(response.data.histories);
    });
  };

  const getHistoryById = (id) => {
    getHistoryByIdFromDb(id).then((response) => {
      setCurrentHistory(response.data.history);
    });
  };

  const convertMessagesToHistory = (messages) => {
    return messages.map((h) => {
      return {
        type: h.type,
        timestamp: h.timestamp,
        text: h.text,
      };
    });
  };

  const convertHistoryToMessages = (history) => {
    return history.map((h) => {
      return {
        type: h.type,
        timestamp: h.timestamp,
        text: h.text,
      };
    });
  };

  const addNewHistoryClick = () => {
    setMessages([]);
    addHistoryToDb({ history: [] }).then((response) => {
      getAllHistories();
      getHistoryById(response.data.id);
    });
  };

  const addHistory = (messages) => {
    const history = convertMessagesToHistory(messages);
    addHistoryToDb({ history: history }).then((response) => {
      getAllHistories();
      getHistoryById(response.data.id);
    });
  };

  const updateHistory = (messages) => {
    const history = convertMessagesToHistory(messages);
    updateHistoryInDb({ id: currentHistory?.id, history: history }).then(() => {
      getAllHistories();
    });
  };

  const deleteHistory = (id) => {
    deleteHistoryFromDb({ id: id }).then(() => {
      getAllHistories();
      if (id === currentHistory?.id || currentHistory === null) {
        setCurrentHistory(null);
        setMessages([]);
      }
    });
  };

  const handleHistoryClick = (id) => {
    setCurrentHistory(histories.find((h) => h.id === id));
  };

  const clearBotData = () => {
    clearData().then(() => {
      getAllHistories();
      setCurrentHistory(null);
      setMessages([]);
    });
  };

  useEffect(() => {
    const current = messagesEndRef.current;
    if (current) {
      current.scrollTop = current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (currentHistory) {
      setMessages(convertHistoryToMessages(currentHistory.history));
    }
  }, [currentHistory]);

  useEffect(() => {
    getCurrentUsername();
    getAllHistories();
  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        height: "100vh",
      }}
    >
      <SettingsModal
        show={showSettings}
        onClose={() => setShowSettings(false)}
        onNameSave={(name) => changeCurrentName(name)}
        clearBotData={clearBotData}
      />
      <div
        style={{
          width: "20%",
          backgroundColor: "#616161",
          flexDirection: "column",
          display: "flex",
          justifyContent: "flex-start",
          height: "100vh",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "flex-start",
            paddingBottom: "3px",
          }}
        >
          <img
            src="chatbot_icon.png"
            alt="chatbotIcon"
            width={"80px"}
            style={{
              background: "white",
              borderRadius: "50px",
              margin: "5px 10px 5px 5px",
            }}
          />
          <div style={{ fontSize: "35px", fontWeight: "bold", color: "white" }}>
            Chat<span style={{ color: "#3224ff" }}>bot</span>
          </div>
        </div>
        <div
          className="hide-scrollbar"
          style={{
            display: "flex",
            flexDirection: "column",
            overflow: "auto",
            flex: 1,
            position: "relative",
          }}
        >
          {histories.map((history, index) => {
            return (
              <HistoryBubble
                key={index}
                history={history}
                onClick={handleHistoryClick}
                onDelete={deleteHistory}
                currentlyActive={currentHistory?.id === history.id}
              />
            );
          })}
          <button
            onClick={addNewHistoryClick}
            style={{
              borderRadius: "10px",
              margin: "5px",
              padding: "10px 5px 10px 5px",
              border: "none",
              cursor: "pointer",
              background: addHistoryHover ? "#3d3d3d" : "#262626",
            }}
            onMouseEnter={() => setAddHistoryHover(true)}
            onMouseLeave={() => setAddHistoryHover(false)}
          >
            <img
              src="plus.png"
              alt="add"
              height="25px"
              width="25px"
              style={{ filter: "invert(100%)" }}
            />
          </button>
        </div>
        <div
          style={{
            padding: "10px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            cursor: "pointer",
            backgroundColor: userProfileHovered ? "#3d3d3d" : "#262626",
            borderRadius: "10px 10px 0px 0px",
          }}
          onMouseEnter={() => setUserProfileHovered(true)}
          onMouseLeave={() => setUserProfileHovered(false)}
          onClick={() => setShowSettings(true)}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <img
              src="user_default_picture.png"
              alt="user"
              style={{
                width: "40px",
                height: "40px",
                marginLeft: "5px",
                background: "white",
                borderRadius: "50%",
              }}
            />
            <div
              style={{
                fontSize: "20px",
                marginLeft: "10px",
                color: "white",
                lineHeight: "25px",
              }}
            >
              {username}
            </div>
          </div>
          <img
            className="settings-image"
            src="settings.png"
            alt="settings"
            style={{ width: "25px", height: "25px" }}
          />
        </div>
      </div>
      <div
        style={{
          width: "80%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          backgroundImage: "linear-gradient(to bottom right, #4a4a4a, #262626)",
        }}
      >
        <div
          className="hide-scrollbar"
          style={{
            padding: "10px",
            overflow: "auto",
            flexGrow: 1,
            width: "80%",
            maxHeight: "auto",
          }}
          onScroll={handleScroll}
          ref={messagesEndRef}
        >
          {messages.map((message, index) => {
            const isUserMessage = message.type === "user";
            return (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: isUserMessage ? "flex-end" : "flex-start",
                  marginBottom: "10px",
                }}
              >
                {isUserMessage ? (
                  <UserBubble
                    text={message.text}
                    username={username}
                    timeStamp={message.timestamp}
                  />
                ) : message.isLoading ? (
                  <BotBubble isLoading={message.isLoading} />
                ) : (
                  <BotBubble
                    text={message.text}
                    timeStamp={message.timestamp}
                  />
                )}
              </div>
            );
          })}
          {showScrollButton && (
            <button
              onClick={() => {
                const scrollContainer = messagesEndRef.current;
                if (scrollContainer) {
                  scrollContainer.scrollTop = scrollContainer.scrollHeight;
                }
              }}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                position: "absolute",
                width: "40px",
                height: "40px",
                bottom: "140px",
                paddingTop: "3px",
                left: "60%",
                borderRadius: "50%",
                border: "none",
                cursor: "pointer",
                background: "#757575",
                transform: "translateX(-50%)",
              }}
            >
              <img
                src="arrow_down.png"
                alt="arrowDown"
                height="25px"
                width="25px"
                style={{ filter: "invert(100%)" }}
              />
            </button>
          )}
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            padding: "10px",
            marginBottom: "5px",
          }}
          onSubmit={sendMessage}
        >
          <div
            style={{
              position: "relative",
              flexGrow: 1,
              minWidth: "50vw",
            }}
          >
            <input
              type="text"
              style={{
                width: "100%",
                height: "40px",
                padding: "10px 0px 10px 10px",
                borderRadius: "15px",
                fontSize: "20px",
                backgroundColor: "inherit",
                border: "1px solid #757575",
                color: "white",
                outline: "none",
              }}
              onKeyPress={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type a message..."
            />
            <button
              type="button"
              onClick={sendMessage}
              style={{
                position: "absolute",
                top: "10px",
                right: "-2px",
                border: newMessage
                  ? "1px solid transparent"
                  : "1px solid black",
                borderRadius: "50px",
                padding: "8px 8px 8px 9px",
                background: newMessage ? "white" : "#757575",
                cursor: "pointer",
                display: "flex",
              }}
            >
              <img
                src={newMessage ? "send_white_fill.png" : "send_black_fill.png"}
                alt="send"
                height="25px"
              />
            </button>
          </div>
          <div
            style={{ color: "#757575", fontSize: "16px", marginTop: "10px" }}
          >
            Chatbot may not always respond correctly to all of your questions.
            Please be patient.
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
