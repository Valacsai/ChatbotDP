import { useState } from "react";
import { startTrainBot } from "../service/BotService";
import Loading from "./Loading";

const SettingsModal = ({ show, onClose, onNameSave, clearBotData }) => {
  const [name, setName] = useState("");
  const [showLoading, setShowLoading] = useState(false);

  if (!show) return null;

  const handleSave = () => {
    onNameSave(name);
    onClose();
  };

  const trainBot = async () => {
    setShowLoading(true);
    try {
      await startTrainBot();
    } catch (error) {
      console.error("Training failed", error);
    } finally {
      setShowLoading(false);
    }
  };

  const handleModalContentClick = (e) => {
    e.stopPropagation();
  };

  return (
    <div
      style={{
        position: "fixed",
        top: "0",
        left: "0",
        right: "0",
        bottom: "0",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: "10",
      }}
      onClick={onClose}
    >
      <div
        style={{
          backgroundColor: "#f0f0f0",
          padding: "20px",
          borderRadius: "10px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "35vw",
          height: "50vh",
          position: "relative",
        }}
        onClick={handleModalContentClick}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
            width: "90%",
          }}
        >
          <div style={{ width: "1px" }} />
          <div style={{ fontSize: "24px" }}>Settings</div>
          <img
            src="cross.png"
            alt="close"
            onClick={onClose}
            style={{
              width: "20px",
              height: "20px",
              background: "inherit",
              cursor: "pointer",
            }}
          />
        </div>
        {showLoading ? (
          <Loading text={"This may take a few seconds."} />
        ) : (
          <>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                width: "90%",
                margin: "5px",
                alignItems: "center",
              }}
            >
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                style={{
                  padding: "10px",
                  fontSize: "18px",
                  borderRadius: "4px",
                  border: "1px solid #ccc",
                  width: "77%",
                }}
              />
              <button
                onClick={handleSave}
                style={{
                  padding: "10px",
                  fontSize: "18px",
                  borderRadius: "4px",
                  width: "90px",
                  marginLeft: "5px",
                  border: "none",
                  backgroundColor: "#3224ff",
                  color: "white",
                  cursor: "pointer",
                }}
              >
                Save
              </button>
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                width: "90%",
                margin: "5px",
                alignItems: "center",
              }}
            >
              <div style={{ padding: "5px", width: "80%" }}>
                Press the button for training the bot, and adding new data to
                the total data.
              </div>
              <button
                onClick={trainBot}
                style={{
                  padding: "10px",
                  fontSize: "18px",
                  borderRadius: "4px",
                  width: "90px",
                  marginLeft: "5px",
                  border: "none",
                  backgroundColor: "#3224ff",
                  color: "white",
                  cursor: "pointer",
                }}
              >
                Train
              </button>
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                width: "90%",
                alignItems: "center",
              }}
            >
              <div style={{ padding: "5px", width: "80%" }}>
                Clear all data from bot memory and storage.
              </div>
              <button
                onClick={clearBotData}
                style={{
                  padding: "10px",
                  fontSize: "18px",
                  borderRadius: "4px",
                  width: "90px",
                  marginLeft: "5px",
                  border: "none",
                  backgroundColor: "#3224ff",
                  color: "white",
                  cursor: "pointer",
                }}
              >
                Clear
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default SettingsModal;
