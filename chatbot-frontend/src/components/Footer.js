const Footer = () => {
  return (
    <div
      style={{
        borderTop: "1px solid white",
        width: "inherit",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "17px",
        fontFamily: "inherit",
        padding: "10px",
        whiteSpace: "nowrap",
        background: "#616161",
      }}
    >
      <div style={{ textAlign: "center", color: "white", marginRight: "6px" }}>
        DP - Chatbot, Viktor Valacsai
      </div>
      <div style={{ textAlign: "center", color: "white" }}>
        ©2024 Slovenská technická univerzita
      </div>
    </div>
  );
};

export default Footer;
