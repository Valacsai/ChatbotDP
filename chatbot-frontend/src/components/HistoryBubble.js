import "../pages/ChatPage.css";
import { useState } from "react";

const HistoryBubble = ({ history, onClick, onDelete, currentlyActive }) => {
  const [hovered, setHovered] = useState();

  const formatDate = (date) => {
    const dateObject = new Date(date);
    const formattedTime = dateObject.toLocaleString("de-DE", {
      hour: "2-digit",
      minute: "2-digit",
    });
    const formattedDate = dateObject.toLocaleString("de-DE", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
    return `${formattedTime} ${formattedDate}`;
  };

  return (
    <div
      style={{
        width: "inherit",
        background: hovered || currentlyActive ? "#555555" : "#757575",
        margin: "5px",
        padding: "15px",
        borderRadius: "10px",
        cursor: "pointer",
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
        onClick={() => onClick(history.id)}
      >
        <div>
          <div
            style={{
              fontSize: "15px",
            }}
          >
            History {history.id}
          </div>
          <div
            style={{
              fontSize: "14px",
            }}
          >
            Last Message: {history.history[history.history.length - 1]?.text}
          </div>
          <div
            style={{
              fontSize: "12px",
              color: "#223134",
            }}
          >
            Last Updated: {formatDate(history.last_updated)}
          </div>
        </div>
        <button
          hidden={!hovered}
          onClick={(event) => {
            event.stopPropagation();
            onDelete(history.id);
          }}
          style={{
            borderRadius: "10px",
            border: "none",
            height: "45px",
            cursor: "pointer",
            background: hovered ? "#3d3d3d" : "#262626",
            zIndex: 100,
          }}
        >
          <img
            src="delete.png"
            alt="delete_history"
            height="25px"
            width="25px"
            style={{ filter: "invert(100%)" }}
          />
        </button>
      </div>
    </div>
  );
};

export default HistoryBubble;
