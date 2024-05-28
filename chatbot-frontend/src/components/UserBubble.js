const UserBubble = ({ text, timeStamp, username }) => {
  return (
    <div
      style={{
        maxWidth: "100%",
        margin: "10px",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
        }}
      >
        <div style={{ fontSize: "14px", color: "gray" }}>{timeStamp}</div>
        <div
          style={{
            fontSize: "16px",
            fontWeight: "bold",
            color: "white",
            marginLeft: "5px",
          }}
        >
          {username}
        </div>
        <img
          src="user_default_picture.png"
          alt="user"
          style={{
            width: "30px",
            height: "30px",
            marginLeft: "5px",
            background: "white",
            borderRadius: "50%",
          }}
        />
      </div>
      <div
        style={{
          padding: "15px",
          backgroundColor: "#e0e0e0",
          borderRadius: "20px 0px 20px 20px",
          marginRight: "22px",
          fontSize: "20px",
          maxWidth: "80%",
          margin: "10px",
          wordWrap: "break-word",
        }}
      >
        {text}
      </div>
    </div>
  );
};

export default UserBubble;
