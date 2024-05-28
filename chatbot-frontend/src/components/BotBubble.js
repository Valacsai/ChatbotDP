import "../pages/ChatPage.css";

const BotBubble = ({ text, isLoading, timeStamp }) => {
  return (
    <div
      style={{
        maxWidth: "100%",
        margin: "10px",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          marginBottom: "8px",
        }}
      >
        <img
          src="chatbot_icon.png"
          alt="Chatbot"
          style={{
            width: "30px",
            height: "30px",
            marginRight: "5px",
            background: "white",
            borderRadius: "50%",
          }}
        />
        <div
          style={{
            fontSize: "16px",
            fontWeight: "bold",
            color: "white",
            marginRight: "5px",
          }}
        >
          Chatbot
        </div>
        <div style={{ fontSize: "14px", color: "gray" }}>{timeStamp}</div>
      </div>
      <div
        style={{
          display: "inline-block",
          maxWidth: "80%",
          padding: "15px",
          marginLeft: "20px",
          backgroundColor: "#ADD8E6",
          borderRadius: "0px 20px 20px 20px",
          fontSize: "20px",
          wordWrap: "break-word",
          color: "black",
          textAlign: "left",
        }}
      >
        {isLoading ? <div className="loading-animation" /> : text}
      </div>
    </div>
  );
};

export default BotBubble;
