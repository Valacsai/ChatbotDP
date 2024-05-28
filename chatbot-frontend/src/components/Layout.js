import Footer from "./Footer";

const Layout = (props) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <div style={{ flex: 1, width: "100%" }}>{props.children}</div>
      <Footer />
    </div>
  );
};

export default Layout;
